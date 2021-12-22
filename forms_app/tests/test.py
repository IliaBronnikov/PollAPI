import json
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT)
from rest_framework.test import APIRequestFactory

from forms_app.serializers import FormSerializer


@pytest.mark.django_db
def test_get_actual_forms():
    factory = APIRequestFactory()
    request = factory.get("forms")

    context = {
        "request": Request(request)
    }
    forms_serializer = FormSerializer()

    data = {
        "title": forms_serializer.title,
        "description": forms_serializer.description,
        "start_at": forms_serializer.start_at,
        "end_at": forms_serializer.end_at
    }

    response = client