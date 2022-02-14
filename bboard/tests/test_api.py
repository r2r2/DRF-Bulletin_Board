import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from bboard import views
from bboard.models import Post, User, Category, Comment
from bboard.serializers import PostListSerializer, CommentSerializer


class PostsApiTestCase(APITestCase):
    """Testing Post model api"""

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='test_username', email='test1@mail.ru')
        self.user2 = User.objects.create(username='test_username2', email='test2@mail.ru')
        self.category1 = Category.objects.create(name='ДД')
        self.category2 = Category.objects.create(name='Танки')
        self.post_1 = Post.objects.create(title='Test title',
                                          text='test text',
                                          category=self.category1,
                                          owner=self.user1)
        self.post_2 = Post.objects.create(title='Test title2',
                                          text='test text2',
                                          category=self.category2,
                                          owner=self.user2)
        self.token = Token.objects.create(user=self.user1)
        self.token.save()
        self.factory = APIRequestFactory()

    def test_token_auth(self):
        request = self.factory.get('/posts', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(request, user=self.user1)
        view = views.PostViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        url = reverse('posts-list')
        response = self.client.get(url)
        serializer_data = PostListSerializer([self.post_1, self.post_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter(self):
        url = reverse('posts-list')
        response = self.client.get(url, data={'post_id': self.post_1.id})
        serializer_data = PostListSerializer([self.post_1, self.post_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts-list')
        data = {
            'id': 3,
            'title': 'Test title3',
            'text': 'test text3',
            'category': 1,
            'upload': None,
            'owner': 'test1@mail.ru',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json',
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Post.objects.all().count())
        self.assertEqual(self.user1, Post.objects.last().owner)

    def test_delete(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts-detail', args=(self.post_1.id,))
        data = {
            'title': 'Test title',
            'text': 'test text',
            'category': 'ДД',
            'owner': 'test1@mail.ru'
        }
        json_data = json.dumps(data)
        self.client.delete(url, data=json_data, content_type='application/json',
                           HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertEqual(1, Post.objects.all().count())

    def test_update(self):
        url = reverse('posts-detail', args=(self.post_1.id,))
        data = {
            'id': 1,
            'title': 'Test title',
            'text': 'test text',
            'category': 2,
            'upload': None,
            'owner': 'test1@mail.ru',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json',
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual(2, self.post_1.category.id)


class PrivateApiTestCase(APITestCase):
    """Testing private page api"""

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='test_username', email='test1@mail.ru')
        self.user2 = User.objects.create(username='test_username2', email='test2@mail.ru')
        self.category1 = Category.objects.create(name='ДД')
        self.post_1 = Post.objects.create(title='Test title',
                                          text='test text',
                                          category=self.category1,
                                          owner=self.user1)
        self.comment = Comment.objects.create(owner=self.user1,
                                              text='test comment',
                                              post=self.post_1,
                                              accepted=False)
        self.token = Token.objects.create(user=self.user1)
        self.token.save()

    def test_get(self):
        url = reverse('private-list')
        response = self.client.get(url, data={'post_id': self.post_1.id},
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))
        user_comments = Comment.objects.filter(post__owner=self.user1)
        serializer_data = CommentSerializer(user_comments, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_not_owner(self):
        """Should provide empty list"""
        url = reverse('private-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        user_comments = Comment.objects.filter(post__owner=self.user2)
        serializer_data = CommentSerializer(user_comments, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(serializer_data, response.data)
