from django.urls import path
from v1.post.views import (
    UserProfileView,
    ProfileImageView,
    CreateView,
    MyBlogsView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView,
    LikeView,
    SearchView,
)

app_name = 'post'

urlpatterns = [
    path('profile-image/', ProfileImageView.as_view(), name='profile_image'),  # View my profile image
    path('profile/', UserProfileView.as_view(), name='profile'),  # View my profile
    path('view/', ListView.as_view(), name='list'),  # List all posts
    path('create/', CreateView.as_view(), name='create'),  # Create a new post
    path('my-blogs/', MyBlogsView.as_view(), name='my_blogs'),  # List all posts by me
    path('detail/<int:pk>/', DetailView.as_view(), name='detail'),  # View a specific post
    path('update/<int:pk>/', UpdateView.as_view(), name='update'),  # Update a specific post
    path('delete/<int:pk>/', DeleteView.as_view(), name='delete'),  # Delete a specific post
    path('like/<int:post_id>/', LikeView.as_view(), name='like'),  # Like a specific post
    path('search/', SearchView.as_view(), name='search'),  # Search for a post
]   