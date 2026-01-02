from rest_framework.views import APIView
from django.db.models import Max, Min, Avg, Count, Case, When, FloatField
from django.utils import timezone
from apps.exam.models import ExamRecord, Exam

from utils.ResponseMessage import check_auth, check_permission, MyResponse
from datetime import timedelta

class ScoreTrendView(APIView):
    @check_auth
    def get(self, request):
        payload = request.user
        if payload.get("role") != "student":
            return MyResponse.success()
        user_id = payload.get("id")

        days = int(request.GET.get("days"))
        timeago = timezone.now() - timedelta(days=days)
        exam_records = ExamRecord.objects.filter(user_id=user_id, status="graded", exam__end_time__gte=timeago).select_related('exam')
        if not exam_records:
            return MyResponse.failed(message="暂无考试成绩记录") 
        try:
            stats = exam_records.aggregate(
                total_exams=Count("id"),
                average_score=Avg("score"),
                highest_score=Max("score"),
                lowest_score=Min("score"),
                pass_rate=Avg(
                    Case(
                        When(is_passed=1, then=1.0),
                        When(is_passed=0, then=0.0),
                        default=None,
                        output_field=FloatField()
                    )
                )
            )
        except Exception as e:
            return MyResponse.failed(message=f"获取成绩记录发生错误，{e}")
        
        trend_list = []
        for exam_record in exam_records:
            trend_list.append({
                "date": exam_record.submit_time.strftime("%Y-%m-%d %H:%M:%S") if exam_record.submit_time else None,
                "exam_title": exam_record.exam.title,
                "score": exam_record.score
            })
            
        response_data = {
            "total_exams": stats.get("total_exams"),
            "average_score": stats.get("average_score"),
            "highest_score": stats.get("highest_score"),
            "lowest_score": stats.get("lowest_score"),
            "pass_rate": stats.get("pass_rate"),
            "trend": trend_list
        }
        # print(response_data)
        
        
        return MyResponse.success(data=response_data)