from typing import Union, Optional

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from forms_app.models import (
    TextAnswer,
    Question,
    UserMultipleAnswer,
    UserSingleAnswer,
    Choice,
)


def create_user_answer(
    question: Question,
    user_id: int,
    answer_text: Optional[str],
    choice_id: Optional[int],
    choice_ids: Optional[list[int]],
) -> Union[TextAnswer, UserSingleAnswer, UserMultipleAnswer]:
    validate_user(user_id)
    validate_user_answer(question, answer_text, choice_id, choice_ids)
    return create_answer_instance(question, user_id, answer_text, choice_id, choice_ids)


def validate_user(user_id: int):
    try:
        User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise ValidationError("User doesn't exist.")


def validate_user_answer(
    question: Question,
    answer_text: Optional[str],
    choice_id: Optional[int],
    choice_ids: Optional[list[int]],
) -> None:
    if question.question_type == question.TEXT and not answer_text:
        raise ValidationError("Answer text must be provided.")
    if question.question_type == question.SINGLE:
        if not choice_id:
            raise ValidationError("Choice id must be provided.")
        elif not Choice.objects.filter(question=question, pk=choice_id).exists():
            raise ValidationError("Choice id does not exist.")
    if question.question_type == question.MULTIPLE:
        if not choice_ids:
            raise ValidationError("Choice ids must be provided.")
        for choice_id in choice_ids:
            if not Choice.objects.filter(question=question, pk=choice_id).exists():
                raise ValidationError("Some of choices do not exist.")


def create_answer_instance(
    question: Question,
    user_id: int,
    answer_text: Optional[str],
    choice_id: Optional[int],
    choice_ids: Optional[list[int]],
) -> Union[TextAnswer, UserSingleAnswer, UserMultipleAnswer]:
    if question.question_type == question.TEXT:
        return TextAnswer.objects.create(
            question=question, user_id=user_id, answer_text=answer_text
        )
    if question.question_type == question.SINGLE:
        return UserSingleAnswer.objects.create(
            question=question, user_id=user_id, choice_id=choice_id
        )
    if question.question_type == question.MULTIPLE:
        choices = Choice.objects.filter(pk__in=choice_ids)
        for choice in choices:
            user_multiple_answer = UserMultipleAnswer.objects.create(
                question=question, user_id=user_id
            )
            user_multiple_answer.choices.add(choice)
        return user_multiple_answer


def get_forms_question_user(user_id: int) -> dict:
    forms_set = set()
    answers = []
    data_lst = []
    try:
        answers.append(TextAnswer.objects.get(user_id=user_id))
    except:
        pass
    try:
        answers.append(UserSingleAnswer.objects.get(user_id=user_id))
    except:
        pass
    try:
        answers.append(UserMultipleAnswer.objects.filter(user_id=user_id))
    except:
        pass
    for answer in answers:
        question_answer = None
        try:
            if answer.question.question_type == "text":
                question_answer = answer.answer_text
            if answer.question.question_type == "single":
                question_answer = answer.choice.choice_text
            form_id = answer.question.form.title
            question_id = answer.question.question_text
        except AttributeError:
            question_answer = []
            for answer_item in answer:
                question_answer.append(answer_item.get_choices())
                form_id = answer_item.question.form.title  # 1
                question_id = answer_item.question.question_text
        data_lst.append(
            {
                "form": form_id,
                "question": question_id,
                "question_answer": question_answer,
            }
        )
        forms_set.add(form_id)
    forms = []
    for form in forms_set:
        questions = []
        for data in data_lst:
            if data["form"] == form:
                questions.append(
                    {"question": data["question"], "answer": data["question_answer"]}
                )
        forms.append({"form_title": form, "questions": questions})
    return {"user_id": user_id, "forms": forms}
