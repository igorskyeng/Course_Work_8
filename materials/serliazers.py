from rest_framework import serializers

from materials.services import convert_currencies
from materials.models import Lesson, Course, Subscription
from materials.validators import URLValidator


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='link_to_the_video')]


class CourseSerializers(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializers(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()
    usd_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_number_of_lessons(instance):
        return instance.lesson_set.all().count()

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()

    def get_usd_price(self, instance):
        return convert_currencies(instance.amount)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
