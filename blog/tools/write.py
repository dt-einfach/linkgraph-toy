from django.contrib.auth.models import User

from ..models import Writer


def get_writer_obj(user: User) -> Writer:
    return Writer.objects.get_or_create(
        user=user,
        defaults={'name': user.username},
    )[0]
