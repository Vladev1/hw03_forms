from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title="Заголовок тестовой задачи",
            slug="Тестовый Слаг",
            description="Описание тестовой группы"
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Описание тестового поста"
        )

    def test_name_group_have_correct_object_names(self):
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовочек',
            'slug': 'Слаг адрес',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                response = group._meta.get_field(field).verbose_name
                self.assertEqual(response, expected_value)

    def test_post_have_correct_object_names(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Мысли великих'
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                response = post._meta.get_field(field).verbose_name
                self.assertEqual(response, expected)

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        self.assertEqual(post.text[:15], str(post))
