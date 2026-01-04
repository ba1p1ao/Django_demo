from rest_framework.views import APIView
from django.db.models import Max, Min, Avg, Count, Case, When, FloatField
from django.utils import timezone
from apps.exam.models import ExamRecord, Exam
from apps.classes.models import Class, UserClass
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


class StudentClassView(APIView):
    @check_auth
    def get(self, request):
        payload = request.user
        user_id = payload.get("id")
        
        # 获取学生所在的班级
        class_info = Class.objects.filter(userclass__user_id=user_id).first()
        if not class_info:
            return MyResponse.failed(message="您还未加入班级")
        
        # 获取当前班级所有学生
        students = UserClass.objects.filter(class_info_id=class_info.id, user__role="student")
        student_count = students.count()
        
        # 获取当前学生的加入时间
        try:
            current_student = students.get(user_id=user_id)
            join_time = current_student.join_time.strftime("%Y-%m-%d %H:%M:%S")
        except UserClass.DoesNotExist:
            join_time = None
        
        # 获取班主任姓名
        head_teacher_name = class_info.head_teacher.username if class_info.head_teacher else None
        
        response_data = {
            "id": class_info.id,
            "name": class_info.name,
            "grade": class_info.grade,
            "head_teacher_name": head_teacher_name,
            "student_count": student_count,
            "join_time": join_time,
        }

        return MyResponse.success(data=response_data)