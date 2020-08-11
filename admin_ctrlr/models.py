import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.


# 2. 시험정보 : 시험 ID, 시험명 , 출제자(교수자 ID), 응시시간 , 응시기간 , 생성일시 , 자동 수동채점여부 , 평균 , 총배점
# 3. 시험문항정보 : 시험 ID, 문항 ID, 배점 , 문제 , 보기 1, 보기 2, 보기 3, 보기 4, 보기 5, 정답
# 4. 응시자정보 : 시험 ID, 학습자 ID, 응시일시 (or null)
# 5. 성적정보 : 시험 ID, 응시자 ID, 문항 ID, O/X 여부 , 작성답 점수


class Test(models.Model):
    title = models.CharField(max_length=200)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_time = models.DateField(default=None)

    SHORT = datetime.timedelta(hours=1)
    MEDIUM = datetime.timedelta(hours=3)
    LONG = datetime.timedelta(hours=5)
    period_choices = ((SHORT, '1 hour'), (MEDIUM, '3 hour'), (LONG, '5 hour'),)
    test_period = models.DurationField(choices=period_choices, default=MEDIUM)

    created_date = models.DateTimeField(default=timezone.now)
    auto_score = models.BooleanField(default=True)
    total_score = models.IntegerField(null=True)

    # average = models.IntegerField()
    # full_score = models.IntegerField()

    def __str__(self):
        return self.title


class QuestionNa(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='Naquests')
    question_score = models.IntegerField()
    question_content = models.TextField()
    ans = models.CharField(max_length=200, null=True)
    # std_ans = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = (('test', 'question_content'),)

    def __str__(self):
        return self.question_content


class StudentAns(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    questionNa = models.ForeignKey('QuestionNa', on_delete=models.CASCADE, null=True)
    questionMc = models.ForeignKey('QuestionMc', on_delete=models.CASCADE, null=True)
    qtype_choices = [('NA', 'narrative'), ('MC', 'multi_choices'),]
    qtype = models.CharField(max_length=20, choices=qtype_choices, default='NA')
    qna_ans = models.CharField(max_length=200, null=True)
    multiple_choices = [('ONE', 'choice_one'), ('TWO', 'choice_two'), ('THR', 'choice_three'), ('FOU', 'choice_four'),
                        ('FIV', 'choice_five')]
    qmc_ans = models.CharField(
        max_length=20,
        choices=multiple_choices,
        default='ONE')


class QuestionMc(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='Mcquests')
    question_score = models.IntegerField()
    question_content = models.TextField()
    multiple_choices = [('ONE', 'choice_one'), ('TWO', 'choice_two'), ('THR', 'choice_three'), ('FOU', 'choice_four'),
                        ('FIV', 'choice_five')]
    cor_ans = models.CharField(
        max_length=20,
        choices=multiple_choices,
        default='ONE')
    ans1 = models.CharField(max_length=20, default='보기를 입력하세요')
    ans2 = models.CharField(max_length=20, default='보기를 입력하세요')
    ans3 = models.CharField(max_length=20, default='보기를 입력하세요')
    ans4 = models.CharField(max_length=20, default='보기를 입력하세요')
    ans5 = models.CharField(max_length=20, default='보기를 입력하세요')
    # std_ans = models.CharField(
    #     max_length=20,
    #     choices=multiple_choices,
    #     default='ONE')
    # ox = models.BooleanField(default=False)

    class Meta:
        unique_together = (('test', 'question_content'),)

    def __str__(self):
        return self.question_content


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    questionNa = models.ForeignKey('QuestionNa', on_delete=models.CASCADE, null=True)
    questionMc = models.ForeignKey('QuestionMc', on_delete=models.CASCADE, null=True)
    ox = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'test', 'questionNa'), ('user', 'test', 'questionMc'),)


class TestedUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    test_taken_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'test'),)


class TestUserList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'test'),)