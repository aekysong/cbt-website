from django.urls import path
from . import views

urlpatterns = [
    path('test_detail/<int:pk>/', views.test_detail, name='test_detail'),
    # path('test_detail/<int:pk>/delete_test', views.delete_test, name='delete_test'),
    path('create_test/', views.create_test, name='create_test'),
    path('test/<int:pk>/', views.test, name='test'),
    path('test_detail/(?P<pk>\d+)/Naquest/$', views.add_Naquest_to_test, name='add_Naquest_to_test'),
    path('test_detail/(?P<pk>\d+)/Mcquest/$', views.add_Mcquest_to_test, name='add_Mcquest_to_test'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('search/', views.search, name='search'),
    path('test_detail/<int:pk>/test_finish', views.test_check, name='test_check'), # pk값은 test_id
    path('test_detail/<int:pk>/Namodify/<int:qid>', views.Naquest_modify, name='Naquest_modify'),  # 테스트 변경
    path('test_detail/<int:pk>/Mcmodify/<int:qid>', views.Mcquest_modify, name='Mcquest_modify'),  # 테스트 변경
    path('test_attend/<int:pk>/', views.test_attend, name='test_attend'),
    path('user_detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('test_attend/<int:pk>/student/<int:sid>', views.student_answer, name='student_answer'),
    path('test_detail/<int:pk>/modify', views.test_modify, name='test_modify'),
    # path('test_detail/<int:pk>/check_answer/', views.check_answer, name='check_answer'),
    path('test_attend/<int:pk>/student/<int:sid>/hand_score', views.hand_score, name='hand_score'),
]


