from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hnews.posts.models import Post


class Command(BaseCommand):
    help = 'Create data for dev'

    def handle(self, *args, **kwargs):
        jean, _ = User.objects.get_or_create(
            username='jean',
            email='jean@example.com',
        )
        jean.set_password('admin@1234')
        jean.save()
        jack, _ = User.objects.get_or_create(
            username='jack',
            email='jack@example.com',
        )
        jack.set_password('admin@1234')
        jack.save()
        james, _ = User.objects.get_or_create(
            username='james',
            email='james@example.com',
        )
        james.set_password('admin@1234')
        james.save()

        microsoft, _ = Post.objects.get_or_create(
            title='Microsoft Is Said to Have Agreed to Acquire GitHub',
            url='https://www.bloomberg.com/news/articles/2018-06-03/microsoft-is-said-to-have-agreed-to-acquire-coding-site-github?',
            creator=jean,
        )
        gitlab, _ = Post.objects.get_or_create(
            title='GitLab sees huge spike in project imports',
            url='https://monitor.gitlab.net/dashboard/db/github-importer?orgId=1',
            creator=jack,
        )
        facebook, _ = Post.objects.get_or_create(
            title='Facebook Gave Device Makers Deep Access to Data on Users and Friends',
            url='https://www.nytimes.com/interactive/2018/06/03/technology/facebook-device-partners-users-friends-data.html',
            creator=james,
        )
