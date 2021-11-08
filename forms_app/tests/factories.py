import factory
import datetime
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyDate
from forms_app.models import (
    Form,
    Question,
    Choice,
    Answer,
    TextAnswer,
    UserSingleAnswer,
    UserMultipleAnswer,
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    password = FuzzyText()


class FormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Form

    title = FuzzyText()
    description = FuzzyText()
    start_at = FuzzyDate(start_date=datetime.date(year=2000, month=1, day=1))
    end_at = FuzzyDate(start_date=start_at + datetime.date(year=2000, month=1, day=1))


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question_text = FuzzyText()
    form = factory.SubFactory(FormFactory)
    question_type = factory.fuzzy.FuzzyChoice(
        ["Text answer", "Single possible answer", "Multiple possible answers"]
    )


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    choice_text = FuzzyText()
    question = factory.SubFactory(QuestionFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    user = factory.SubFactory(UserFactory)


class TextAnswerFactory(AnswerFactory):
    class Meta:
        model = TextAnswer

    answer_text = FuzzyText()


class UserSingleAnswerFactory(AnswerFactory):
    class Meta:
        model = UserSingleAnswer

    choice = factory.SubFactory(ChoiceFactory)


class UserMultipleAnswerFactory(AnswerFactory):
    class Meta:
        model = UserMultipleAnswer

    @factory.post_generation
    def choices(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for choice in extracted:
                self.choices.add(choice)
