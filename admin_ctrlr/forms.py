from django import forms
from .models import Test, QuestionMc, QuestionNa

class CreateTestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('title', 'test_time', 'test_period', 'auto_score', 'total_score',)


class CreateQuestionMcForm(forms.ModelForm):

    class Meta:
        model = QuestionMc
        fields = ('question_score', 'question_content', 'cor_ans', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5')


class CreateQuestionNaForm(forms.ModelForm):

    class Meta:
        model = QuestionNa
        fields = ('question_score', 'question_content', 'ans',)