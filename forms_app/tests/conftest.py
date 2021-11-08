from pytest_factoryboy import register

from forms_app.tests.factories import (
    UserFactory,
    FormFactory,
    QuestionFactory,
    ChoiceFactory,
    AnswerFactory,
    TextAnswerFactory,
    UserSingleAnswerFactory,
    UserMultipleAnswerFactory,
)

register(UserFactory)
register(FormFactory)
register(QuestionFactory)
register(UserFactory)
