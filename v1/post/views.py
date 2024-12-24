from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from v1.post.serializers import CreateSerializer, ListSerializer, UpdateSerializer, UserProfileSerializer, ImageProfileSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model
from v1.post.models import Post, Likes, Profile
from v1.post.permissions import IsOwnerOrReadOnly
User = get_user_model()


class UserProfileView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile Image not found"})
        
        serializer = ImageProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
            profile.save()
            serializer = ImageProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        profile.profile_image.delete()
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CreateView(CreateAPIView):
	serializer_class = CreateSerializer
	def perform_create(self,serializer):
		serializer.save(author=self.request.user)

class MyBlogsView(ListAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ListSerializer
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class UpdateView(RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class DeleteView(DestroyAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'message': 'Blog post deleted successfully.'}
        return response


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ListSerializer
    pagination_class = ListPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__username','category', 'blog_image']


class DetailView(RetrieveAPIView):
	lookup_field = 'pk'
	queryset = Post.objects.all()
	serializer_class = ListSerializer
      

class LikeView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        like_obj, created = Likes.objects.get_or_create(user=request.user, post=post)
        like_obj.is_liked = not like_obj.is_liked
        like_obj.save()

        if like_obj.is_liked:
            post.likes += 1
        else:
            post.likes -= 1
        post.save()

        return Response({
            "message": "Like toggled successfully.",
            "is_liked": like_obj.is_liked,
            "likes_count": post.likes
        }, status=status.HTTP_200_OK)


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        filter_by = request.GET.get('filter_by', 'title')

        if not query:
            return Response({"detail": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        if filter_by not in ['title', 'name']:
            return Response({"detail": "Invalid filter option."}, status=status.HTTP_400_BAD_REQUEST)

        if filter_by == 'title':
            # Search posts by title
            posts = Post.objects.filter(title__icontains=query)
            serializer = ListSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif filter_by == 'name':
            # Search users by name
            users = User.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query.split(' ')[0], last_name__icontains=query.split(' ')[-1])
            ).distinct()

            user_data = [
                {"full_name": f"{user.first_name} {user.last_name}".strip()} for user in users
            ]
            return Response(user_data, status=status.HTTP_200_OK)


# class ViewProfileView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, username):
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         user_serializer = UserProfileSerializer(user)
#         blogs = Post.objects.filter(author=user)
#         blog_serializer = ListSerializer(blogs, many=True, context={'request': request})

#         return Response({
#             "profile": user_serializer.data,
#             "blogs": blog_serializer.data,
#         }, status=status.HTTP_200_OK)

