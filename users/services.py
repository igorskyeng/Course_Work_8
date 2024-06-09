import stripe
from django.core.mail import send_mail

from config.settings import SKRIPE_KEY, EMAIL_HOST_USER
from materials.models import Course

stripe.api_key = SKRIPE_KEY


def create_stripe_session(serializer):
    course_name = serializer.paid_course.course_name

    stripe_product = stripe.Product.create(name=course_name)

    stripe_price = stripe.Price.create(currency="rub",
                                       unit_amount=serializer.paid_course.amount * 100,
                                       recurring={"interval": "month"},
                                       product_data=stripe_product.id)

    stripe_session = stripe.checkout.Session.create(succes_ul="http://127.0.0.1:8000",
                                                    line_items=[{"price": stripe_price.id, "quantity": 1}],
                                                    mode="payment",
                                                    customer_email=serializer.user.email)

    return stripe_session
