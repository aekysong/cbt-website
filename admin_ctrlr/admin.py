from django.contrib import admin
from admin_ctrlr.models import Test, QuestionNa, QuestionMc, Score, TestedUser, StudentAns
from registration.models import Profile


# Register your models here.

admin.site.register(Test)
admin.site.register(QuestionNa)
admin.site.register(QuestionMc)
admin.site.register(Score)
admin.site.register(TestedUser)
admin.site.register(Profile)
admin.site.register(StudentAns)