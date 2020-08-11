from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count

from .forms import CreateTestForm, CreateQuestionNaForm, CreateQuestionMcForm
from admin_ctrlr.models import Test, QuestionNa, QuestionMc, Score, TestedUser, StudentAns, TestUserList
from django.contrib.auth.models import User
from registration.models import Profile


def home(request):
    tests = Test.objects.all()

    # sorting
    sort = request.GET.get('sort', '')
    if sort == 'date':
        tests = Test.objects.all().order_by('test_time')
        return render(request, 'home.html', {'tests': tests})
    elif sort == 'title':
        tests = Test.objects.all().order_by('title')
        return render(request, 'home.html', {'tests': tests})

    return render(request, 'home.html', {'tests': tests})


def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    testlist = TestUserList.objects.filter(test=test)
    testlist_users = []
    for i in range(len(testlist)):
        testlist_users.append(testlist[i].user)

    # 문항별 오답비율
    qmc_score_ox = Score.objects.values('questionMc_id').filter(test=test).annotate(Count('questionMc_id'))
    qmc_score_x = Score.objects.values('questionMc_id').filter(test=test, ox=False).annotate(Count('questionMc_id'))
    qmc_ratio_dict = {}
    for qmc_s_ox in qmc_score_ox:
        if qmc_s_ox['questionMc_id'] != None:
            for qmc_s_x in qmc_score_x:
                if qmc_s_x['questionMc_id'] == qmc_s_ox['questionMc_id']:
                    qmc_ratio_dict.setdefault(qmc_s_ox['questionMc_id'],
                                              (int(qmc_s_x['questionMc_id__count']) / int(
                                                  qmc_s_ox['questionMc_id__count'])))
    qna_score_ox = Score.objects.values('questionNa_id').filter(test=test).annotate(Count('questionNa_id'))
    qna_score_x = Score.objects.values('questionNa_id').filter(test=test, ox=False).annotate(Count('questionNa_id'))
    qna_ratio_dict = {}
    for qna_s_ox in qna_score_ox:
        if qna_s_ox['questionNa_id'] != None:
            for qna_s_x in qna_score_x:
                if qna_s_x['questionNa_id'] == qna_s_ox['questionNa_id']:
                    qna_ratio_dict.setdefault(qna_s_ox['questionNa_id'],
                                              (int(qna_s_x['questionNa_id__count']) / int(
                                                  qna_s_ox['questionNa_id__count'])))


    # calculate average
    score = Score.objects.filter(test=test)
    std_num = TestedUser.objects.filter(test=test).count()
    count = 0
    for s in score:
        if s.ox:
            if s.questionMc != None:
                count = int(s.questionMc.question_score) + count
            elif s.questionNa != None:
                count = int(s.questionNa.question_score) + count
    if std_num > 0:
        average = round(count/std_num)
    else:
        average = 0

    flag = False

    if request.method == "POST" and request.user.is_active:
        if 'delete_test' in request.POST:
            test.delete()
            return redirect(home)
        if 'start_test' in request.POST:
            print(timezone.now().date(), test.test_time)
            if timezone.now().date() == test.test_time:
                if request.user in testlist_users:
                    if TestedUser.objects.filter(test=test, user=request.user).count() > 0:
                        return render(request, "test_detail.html",
                                      {'test': test, "message": "이미 응시한 시험입니다", 'testlist': testlist,
                                       'average': average})
                    else:
                        tested_user = TestedUser.objects.create(user=request.user, test=test)
                        tested_user.save()
                        return redirect('test', pk=test.pk)
                else:
                    message = "응시자가 아닙니다"
                    return render(request, 'test_detail.html', {'test': test, 'testlist': testlist,
                                                                'message': message, 'average': average})
            else:
                message = "시험 응시 가능 시간이 아닙니다"
                return render(request, 'test_detail.html', {'test': test, 'testlist': testlist,
                                                            'message': message, 'average': average})
        if 'copy_test' in request.POST:
            new_test = Test.objects.create(title=test.title, professor=test.professor, test_time=test.test_time,
                                           test_period=test.test_period, created_date=timezone.now(),
                                           auto_score=test.auto_score, total_score=test.total_score)
            return redirect('home')
    return render(request, 'test_detail.html', {'test': test, 'testlist': testlist, 'qna_ratio_dict': qna_ratio_dict,
                                                'qmc_ratio_dict': qmc_ratio_dict, 'average': average})


# def test(request, pk):
#     test = get_object_or_404(Test, pk=pk)
#     timelimit = test.get_test_period_display()[:1]
#     questnas = QuestionNa.objects.filter(test=test)
#     questmcs = QuestionMc.objects.filter(test=test)
#     if request.method == "POST":
#         print(request.POST)
#         na_std_ans = request.POST.getlist('na_std_ans')  # get the inputs of same name from html
#         mc_std_ans = request.POST.getlist('mc_std_ans')
#         for i in range(len(na_std_ans)):
#             std_ans = StudentAns.objects.create(user=request.user, test=test, qtype='NA',
#                                                 questionNa=questnas[i], qna_ans=na_std_ans[i])
#             std_ans.save()  # save student answer for quesiton na
#             score = Score.objects.create(user=request.user, test=test, questionNa=questnas[i])
#             score.save()  # for auto scoring
#         for i in range(len(mc_std_ans)):
#             std_ans = StudentAns.objects.create(user=request.user, test=test, qtype='MC',
#                                                 questionMc=questmcs[i], qmc_ans=mc_std_ans[i])
#             std_ans.save()  # save student answer for quesiton mc
#             score = Score.objects.create(user=request.user, test=test, questionMc=questmcs[i])
#             score.save()  # for auto scoring
#         return redirect('test_detail', pk=pk)
#     return render(request, 'test.html', {'test': test, 'questnas': questnas, 'questmcs': questmcs,
#                                          'timelimit': timelimit, 'messages': messages})

def test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    timelimit = test.get_test_period_display()[:1]
    questnas = QuestionNa.objects.filter(test=test)
    questmcs = QuestionMc.objects.filter(test=test)
    if request.method == "POST":
        na_std_ans = request.POST.getlist('na_std_ans')  # get the inputs of same name from html
        mc_std_ans = request.POST.getlist('mc_std_ans')
        for i in range(len(na_std_ans)):
            print(request.POST)
            std_ans = StudentAns.objects.create(user=request.user, test=test, qtype='NA',
                                                questionNa=questnas[i], qna_ans=na_std_ans[i])
            std_ans.save()  # save student answer for quesiton na

            if test.auto_score == True:
                if na_std_ans[i] == questnas[i].ans:
                    ox = True
                else:
                    ox = False
                score = Score.objects.create(ox=ox, user=request.user, test=test, questionNa=questnas[i])
                score.save()  # for auto scoring
        for i in range(len(mc_std_ans)):
            print(request.POST)
            std_ans = StudentAns.objects.create(user=request.user, test=test, qtype='MC',
                                                questionMc=questmcs[i], qmc_ans=mc_std_ans[i])
            std_ans.save()  # save student answer for quesiton mc

            if test.auto_score == True:
                if mc_std_ans[i] == questmcs[i].cor_ans:
                    ox = True
                else:
                    ox = False
                score = Score.objects.create(ox=ox, user=request.user, test=test, questionMc=questmcs[i])
                score.save()  # for auto scoring

        return redirect('test_detail', pk=pk)
    return render(request, 'test.html', {'test': test, 'questnas': questnas, 'questmcs': questmcs,
                                         'timelimit': timelimit, 'messages': messages})


def create_test(request):
    stds1 = Profile.objects.filter(type="student")
    stds2 = Profile.objects.filter(type="ST")
    if request.method == "POST":
        print(request.POST)
        form = CreateTestForm(request.POST)
        testlist = request.POST.getlist('testlist')
        if form.is_valid():
            test = form.save(commit=False)
            test.professor_id = request.user.id
            test.save()
            for i in range(len(testlist)):
                user = User.objects.get(username=testlist[i])
                testlist_user = TestUserList.objects.create(user=user, test=test)
                testlist_user.save()
            return redirect('home')
    else:
        form = CreateTestForm()
    return render(request, 'create_test.html', {'form': form, 'stds1': stds1, 'stds2': stds2})


def add_Naquest_to_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = CreateQuestionNaForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.test = test
            quest.save()
            return redirect('test_detail', pk=test.pk)
    else:
        form = CreateQuestionNaForm()
    return render(request, 'add_Naquest_to_test.html', {'form': form})


def add_Mcquest_to_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = CreateQuestionMcForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.test = test
            quest.save()
            return redirect('test_detail', pk=test.pk)
    else:
        form = CreateQuestionMcForm()
    return render(request, 'add_Mcquest_to_test.html', {'form': form})


def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


def search(request):
    qs = Test.objects.all()

    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q:  # q가 있으면
        qs = qs.filter(title__icontains=q)  # 제목에 q가 포함되어 있는 레코드만 필터링

    return render(request, 'search.html', {
        'qs': qs,
        'q': q,
    })


def test_check(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "GET":
        question = QuestionNa.objects.filter(test_id=pk)
        count = 0
        for a in question:
            if a.std_ans == a.ans:
                count = count + a.question_score

        return render(request, 'test_check.html', {'test': test, 'question': question, 'count': count})


def Naquest_modify(request, pk, qid):
    test = get_object_or_404(Test, pk=pk)
    mod_question = QuestionNa.objects.filter(id=qid).first()
    if request.method == "GET":
        questions = QuestionNa.objects.filter(test_id=qid)
        form = CreateQuestionNaForm(instance=mod_question)
        return render(request, 'Naquest_update.html',
                      {'test': test, 'question': questions, 'form': form})
    elif request.method == "POST":
        form = CreateQuestionNaForm(request.POST, instance=mod_question)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.save()
            return redirect('test_detail', pk=pk)
        return redirect('home')


def Mcquest_modify(request, pk, qid):
    test = get_object_or_404(Test, pk=pk)
    mod_question = QuestionMc.objects.filter(id=qid).first()
    if request.method == "GET":
        questions = QuestionMc.objects.filter(test_id=qid)
        form = CreateQuestionMcForm(instance=mod_question)
        return render(request, 'Mcquest_update.html',
                      {'test': test, 'question': questions, 'form': form})
    elif request.method == "POST":
        form = CreateQuestionMcForm(request.POST, instance=mod_question)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.save()
            return redirect('test_detail', pk=pk)
        return redirect('home')


def test_attend(request, pk):
    test = Test.objects.get(pk=pk)
    tested_users = TestedUser.objects.filter(test=test)
    testUserList = TestUserList.objects.filter(test=test)

    already = []
    for i in range(len(tested_users)):
        already.append(tested_users[i].user.username)

    return render(request, 'test_attend.html',
                  {'tested_users': tested_users, 'testUserList': testUserList,
                   'test': test, 'already': already})


def user_detail(request, pk):
    subuser = User.objects.get(pk=pk)
    if request.method == "POST" and (request.user.profile.type == 'manager' or request.user.profile.type == 'MGR'):
        print(request.POST)
        if 'delete_user' in request.POST:
            subuser.delete()
            return redirect(manage_users)
        if 'accept_prof' in request.POST:
            subuser.profile.accept = True
            subuser.profile.accept_date = timezone.now()
            subuser.save()
            subuser.profile.save()
            return redirect('user_detail', pk=subuser.pk)
    return render(request, 'user_detail.html', {'subuser': subuser})


def student_answer(request, pk, sid):
    test = Test.objects.get(pk=pk)
    std = User.objects.get(pk=sid)
    std_ans = StudentAns.objects.filter(test=test, user=std)
    score = Score.objects.filter(test=test, user=std)
    count = 0

    numcount = Score.objects.filter(test=test, user=std).count()

    for s in score:
        if s.ox:
            if s.questionMc != None:
                count = int(s.questionMc.question_score) + count
            elif s.questionNa != None:
                count = int(s.questionNa.question_score) + count

    return render(request, 'student_answer.html',
                  {'std': std, 'std_ans': std_ans, 'test': test, 'score': score, 'count': count,
                   'numcount': numcount})


def check_answer(request, pk):
    test = Test.objects.get(pk=pk)
    std_ans = StudentAns.objects.filter(test=test, user=request.user)
    return render(request, 'check_answer.html', {'std_ans': std_ans})


def test_modify(request, pk):
    test = get_object_or_404(Test, pk=pk)
    stds1 = Profile.objects.filter(type="student")
    stds2 = Profile.objects.filter(type="ST")
    if request.method == "POST":
        form = CreateTestForm(request.POST, instance=test)
        testlist = request.POST.getlist('testlist')
        if form.is_valid():
            test = form.save(commit=False)
            test.save()
            for i in range(len(testlist)):
                user = User.objects.get(username=testlist[i])
                testlist_user = TestUserList.objects.create(user=user, test=test)
                testlist_user.save()
            return redirect('test_detail', pk=test.pk)
    else:
        form = CreateTestForm(instance=test)
    return render(request, 'test_modify.html', {'test': test, 'form': form, 'stds1': stds1, 'stds2': stds2})


def hand_score(request, pk, sid):
    test = Test.objects.get(pk=pk)
    std = User.objects.get(pk=sid)
    std_ans = StudentAns.objects.filter(test=test, user=std)
    score = Score.objects.filter(test=test, user=std)
    questnas = QuestionNa.objects.filter(test=test)
    questmcs = QuestionMc.objects.filter(test=test)

    if request.method == "POST":
        print(request.POST)
        na_correct = request.POST.getlist('na_correct')
        mc_correct = request.POST.getlist('mc_correct')
        for i in range(len(na_correct)):
            if na_correct[i] == 'O':
                na_score = Score.objects.create(ox=True, test=test, user=std, questionNa=questnas[i])
                na_score.save()
            else:
                na_score = Score.objects.create(ox=False, test=test, user=std, questionNa=questnas[i])
                na_score.save()

        for i in range(len(mc_correct)):
            if mc_correct[i] == 'O':
                mc_score = Score.objects.create(ox=True, test=test, user=std, questionMc=questmcs[i])
                mc_score.save()
            else:
                na_score = Score.objects.create(ox=False, test=test, user=std, questionMc=questmcs[i])
                na_score.save()
        return redirect('student_answer', pk=test.pk, sid=std.id)

    return render(request, 'hand_score.html', {'std': std, 'std_ans': std_ans,
                                               'test': test, 'score': score})