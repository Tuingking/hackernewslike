from urllib.parse import urlparse
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize


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

    def how_long_ago(self):
        how_long = timezone.now() - self.creation_date
        if how_long < timedelta(minutes=1):
            return f'{how_long.seconds} second{pluralize(how_long.seconds)} ago'
        elif how_long < timedelta(hours=1):
            minutes = int(how_long.total_seconds()) // 60
            return f'{minutes} minute{pluralize(minutes)} ago'
        elif how_long < timedelta(days=1):
            hours = int(how_long.total_seconds()) // 3600
            return f'{hours} hour{pluralize(hours)} ago'
        else:
            return f'{how_long.days} day{pluralize(how_long.days)} ago'

    def get_domain_name(self):
        name = urlparse(self.url).hostname
        if name.startswith('www.'):
            return name[len('www.'):]
        else:
            return name


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
