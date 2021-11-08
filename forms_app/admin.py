from django.contrib import admin

# Register your models here.
from .models import Question, Form, Choice


class QuestionInline(admin.TabularInline):
    model = Question


class ChoiceInline(admin.TabularInline):
    model = Choice


class FormAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ["start_at"]
        return self.readonly_fields

    fields = ["title", "description", "start_at", "end_at"]
    inlines = [QuestionInline]
    pass


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    pass


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
