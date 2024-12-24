from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
	title = models.CharField(max_length=100)
	content = models.TextField(max_length=20000)
	published = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	likes = models.IntegerField(default=0)
	blog_image = models.ImageField(upload_to='blog_images/')
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('-published', '-pk')


class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
	is_liked = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user.username} likes {self.post.title if self.post else 'None'}"
	


