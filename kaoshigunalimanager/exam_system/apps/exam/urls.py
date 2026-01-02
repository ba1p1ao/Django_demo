from django.urls import path
from apps.exam import views


urlpatterns = [
    # 试卷管理
    path("list/", views.ExamListView.as_view()),
    path("add/", views.ExamAddView.as_view()),
    path("available/", views.ExamAvailableView.as_view()),
    path("<int:pk>/", views.ExamModelViewSet.as_view({
        "get": "get",
        "put": "put",
        "delete": "delete",
    })),
    path("<int:pk>/publish/", views.ExamPublishView.as_view()),
    path("<int:pk>/close/", views.ExamCloseView.as_view()),

    # 考试相关
    path("start/", views.ExamStartView.as_view()),
    path("<int:exam_id>/questions/", views.ExamQuestionsView.as_view()),
    path("answer/", views.ExamAnswerView.as_view()),
    path("submit/", views.ExamSubmitView.as_view()),

    # 考试记录
    path("record/list/", views.ExamRecordListView.as_view()),
    path("record/<int:pk>/", views.ExamRecordDetailView.as_view()),
    path("<int:exam_id>/statistics/", views.ExamRecordStatisticsView.as_view()),
    # 考试列表分组
    path("grouped-records/", views.GroupedExamRecordListView.as_view()),

    # 统计数据
    path("statistics/", views.SystemStatisticsView.as_view()),

    # 考试排名
    path("<int:exam_id>/ranking/", views.ExamRankingView.as_view()),
]