from django.http import JsonResponse
from django.utils.timezone import localtime
from django.views import View
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Form, Question
from .serializers import (
    FormSerializer,
    FormExtendedSerializer,
    AnswerSerializer,
)
from .services import create_user_answer, get_forms_question_user


class FormViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        now = localtime()
        queryset = Form.objects.all().filter(start_at__lte=now, end_at__gte=now)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FormSerializer
        return FormExtendedSerializer


class AnswerCreateAPIView(CreateAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        now = localtime()
        queryset = Question.objects.all().filter(
            form__start_at__lte=now, form__end_at__gte=now
        )
        return queryset

    def create(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user_answer(
            question=question,
            user_id=serializer.validated_data["user_id"],
            answer_text=serializer.validated_data.get("answer_text"),
            choice_id=serializer.validated_data.get("choice_id"),
            choice_ids=serializer.validated_data.get("choice_ids"),
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserFormsAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        user_data = get_forms_question_user(pk)
        return JsonResponse(user_data, status=201)
