from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonsTest(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(email="igorskyeng@sky.pro")
        self.course = Course.objects.create(course_name='Tests',
                                            description='Tests',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(lesson_name='Tests',
                                            description='Tests',
                                            course=self.course,
                                            owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            "lesson_name": "test10",
            "description": "1232311",
            "link_to_the_video": "http://3.youtube.com",
            "course": 1
        }

        resource = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEquals(
            resource.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lessons(self):
        resource = self.client.get(
            '/lesson/',
        )

        self.assertEquals(
            resource.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            resource.json(),
            {
                'count': 1, 'next': None, 'previous': None, 'results':
                [{
                    'id': 6, 'lesson_name': 'Tests', 'preview': None, 'description': 'Tests',
                    'link_to_the_video': None, 'course': 5, 'owner': 5
                }]
            }

        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            f'/lesson/{self.lesson.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {
                'id': 4, 'lesson_name': 'Tests', 'preview': None, 'description': 'Tests',
                'link_to_the_video': None, 'course': 3, 'owner': 3
            }

        )

    def test_lesson_update(self):
        data = {
            "lesson_name": "update",
            "description": "Tests",
            "link_to_the_video": "http://3.youtube.com",
            "course": 4
        }

        response = self.client.patch(
            f'/lesson/update/{self.lesson.pk}/',
            data=data
        )

        new_data = response.json()

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            new_data.get('lesson_name'),
            "update"
        )

        self.assertEquals(
            self.lesson.description,
            new_data.get('description')
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            f'/lesson/delete/{self.lesson.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEquals(
            Lesson.objects.all().count(),
            0
        )


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="igorskyeng@sky.pro")
        self.course = Course.objects.create(course_name='Tests',
                                            description='Tests',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        data = {
            "course": self.course.pk
        }

        response = self.client.post(
            '/course/subscribe/',
            data=data
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data,
            {'message': 'Подписка включена'}
        )

    def test_unsubscribe(self):
        data = {
            "course": self.course.pk
        }

        Subscription.objects.create(course=self.course, user=self.user)

        response = self.client.post(
            '/course/subscribe/',
            data=data
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data,
            {'message': 'Подписка отключена'}
        )
