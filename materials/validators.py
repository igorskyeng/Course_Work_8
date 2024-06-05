from rest_framework.serializers import ValidationError
import re


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_url = dict(value).get(self.field)

        if "youtube.com" not in tmp_url:
            raise ValidationError('Разрешены только ссылка на "Youtube.com"')
