from django.db.models import signals
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from bboard.models import Category, User, Post, Comment
from bboard.serializers import PostListSerializer, CommentSerializer


@freeze_time("1955-11-12")
class PostSerializerTestCase(TestCase):
    """Testing Post model serializer"""

    def setUp(self) -> None:
        self.current_date_time = timezone.now()
        self.user1 = User.objects.create_user(username='test_username1', email='test1@mail.ru')
        self.user2 = User.objects.create_user(username='test_username2', email='test2@mail.ru')
        self.category1 = Category.objects.create(name='ДД')
        self.category2 = Category.objects.create(name='Танки')
        self.post_1 = Post.objects.create(title='Test title',
                                          text='test text',
                                          category=self.category1,
                                          owner=self.user1,
                                          created=self.current_date_time
                                          )
        self.post_2 = Post.objects.create(title='Test title2',
                                          text='test text2',
                                          category=self.category2,
                                          owner=self.user2,
                                          created=self.current_date_time
                                          )

    def test_ok(self):
        from rest_framework.fields import DateTimeField

        data = PostListSerializer([self.post_1, self.post_2], many=True).data
        expected_data = [
            {
                'id': self.user1.id,
                'title': 'Test title',
                'text': 'test text',
                'category': 1,
                'owner': 'test_username1',
                'created': DateTimeField().to_representation(self.current_date_time),
                'upload': None,
            },
            {
                'id': self.user2.id,
                'title': 'Test title2',
                'text': 'test text2',
                'category': 2,
                'owner': 'test_username2',
                'created': DateTimeField().to_representation(self.current_date_time),
                'upload': None,
            },
        ]
        self.assertEqual(expected_data, data)


@freeze_time("1955-11-12")
class CommentSerializerTestCase(TestCase):
    """Testing Comment serializer"""

    def setUp(self) -> None:
        # disable signals
        signals.post_save.receivers = []

        self.current_date_time = timezone.now()
        self.user1 = User.objects.create_user(username='test_username1', email='test1@mail.ru')
        self.category1 = Category.objects.create(name='ДД')
        self.post_1 = Post.objects.create(title='Test title',
                                          text='test text',
                                          category=self.category1,
                                          owner=self.user1,
                                          created=self.current_date_time
                                          )
        self.comment_1 = Comment.objects.create(owner=self.user1,
                                                text='test text1',
                                                post=self.post_1,
                                                created=self.current_date_time,
                                                accepted=False
                                                )

    def test_ok(self):
        from rest_framework.fields import DateTimeField
        data = CommentSerializer(self.comment_1).data
        expected_data = [
            {
                'id': self.comment_1.id,
                'text': 'test text1',
                'created': DateTimeField().to_representation(self.current_date_time),
                'accepted': False,
                'owner': self.user1.id,
                'post': self.post_1.id,
            },
        ]
        self.assertEqual(data, *expected_data)
