from django.contrib.auth.models import User
from django.db import models


class Form(models.Model):
    class Meta:
        verbose_name = "опрос"
        verbose_name_plural = "опросы"

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"

    TEXT = "text"
    SINGLE = "single"
    MULTIPLE = "multiple"
    QUESTION_TYPE_CHOICES = (
        (TEXT, "Text answer"),
        (SINGLE, "Single possible answer"),
        (MULTIPLE, "Multiple possible answers"),
    )

    question_text = models.CharField(max_length=200)
    form = models.ForeignKey(
        Form, related_name="questions", verbose_name="опрос", on_delete=models.CASCADE
    )
    question_type = models.CharField(
        max_length=10, choices=QUESTION_TYPE_CHOICES, default=TEXT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"

    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(
        Question,
        related_name="choices",
        verbose_name="вопрос",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    class Meta:
        abstract = True

    question = models.ForeignKey(
        Question, verbose_name="вопрос", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, verbose_name="пользователь", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class TextAnswer(Answer):
    class Meta:
        verbose_name = "ответ текстом"
        verbose_name_plural = "ответы текстом"

    answer_text = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.id)


class UserSingleAnswer(Answer):
    class Meta:
        verbose_name = "ответ с выбором одного варианта"
        verbose_name_plural = "ответы с выбором одного варианта"

    choice = models.ForeignKey(Choice, verbose_name="выбор", on_delete=models.CASCADE)

    def __str__(self):
        return self.choice.choice_text


class UserMultipleAnswer(Answer):
    class Meta:
        verbose_name = "ответ с выбором нескольких вариантов"
        verbose_name_plural = "ответы с выбором нескольких вариантов"

    choices = models.ManyToManyField(Choice)

    def get_choices(self):
        return ",".join([str(choice) for choice in self.choices.all()])

    def __str__(self):
        return str(self.id)
