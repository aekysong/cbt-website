from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 1. 이용자정보 : ID, PW, 이름 , 등급 (학습자 , 교수자 , 관리자 )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_choices = [('ST', 'student'), ('MGR', 'manager'), ('PRF', 'professor')]
    type = models.CharField(
        max_length=20,
        choices=type_choices,
        default='ST')
    accept = models.BooleanField(default=False)
    accept_date = models.DateTimeField(default=timezone.now)

    def acceptance(self):
        if self.type != 'professor':
            self.accept == True
        else:
            self.accept = False

    def __str__(self):
        return self.user.username
