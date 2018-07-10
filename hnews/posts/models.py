from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    - Post will be set to NULL if user is deleted.
    - Post can be voted gte 1
    """
    creator = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    upvotes = models.ManyToManyField(User, through='Upvote')
    title = models.CharField(max_length=256)


class Upvote(models.Model):
    """
    Remove Upvote when post is deleted.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        related_name='upvotes',
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'Comment',
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    content = models.TextField(null=True)
    upvotes = models.ManyToManyField(
        User,
        through='CommentUpvote',
    )


class CommentUpvote(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='comment_upvotes',
        on_delete=models.CASCADE,
    )
