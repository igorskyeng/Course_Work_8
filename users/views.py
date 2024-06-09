from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from users.models import User, Payments

from users.serliazers import PaymentsSerializers, UserSerializers
from users.services import create_stripe_session


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user

        if payment.payment_method == "Перевод":
            payment.payment_id = create_stripe_session(payment).id
            payment.payment_link = create_stripe_session(payment).url

        payment.save()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
