from rest_framework.views import APIView
from django.db.models import Count, Max, Min
from apps.question.models import Question
from apps.user.models import User
from apps.exam.models import AnswerRecord, ExamRecord
from utils.ResponseMessage import check_auth, MyResponse


class MistakeListWithStatisticsView(APIView):
    @check_auth
    def get(self, request):
        payload = request.user

        user_id = payload.get("id")
        # 判断用户是否存在
        try:
            student = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return MyResponse.failed(message="学生信息不存在")

        request_data = request.GET

        page = int(request_data.get("page", 1))
        page_size = int(request_data.get("size", 10))
        offset = (page - 1) * page_size
        # 构建筛选条件
        filter_body = {}
        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif v:
                filter_body[f"question__{k}__icontains"] = v

        # 构建响应数据
        response_data = {
            "list": [],
            "page": page,
            "size": page_size,
            "total": 0,
            "statistics": {
                "total_mistakes": 0,
                "unique_questions": 0,
                "type_distribution": {},
                "category_distribution": {},
                "recent_mistakes": [],
            },
        }
        # 获取学生参加的考试id
        exam_record_ids = ExamRecord.objects.filter(
            user_id=user_id, status="graded"
        ).values_list("id", flat=True).distinct()
        # print(exam_record_ids)
        if not exam_record_ids:
            return MyResponse.success(message="暂时没有错误题目信息", data=response_data)

        # 获取符合条件的，学生错误的题目
        answer_records = AnswerRecord.objects.filter(
            **filter_body,
            exam_record_id__in=exam_record_ids,
            is_correct=0
        ).select_related("question", "exam_record__exam")

        if not answer_records.exists():
            return MyResponse.success(message="暂时没有错误题目信息", data=response_data)

        # 获取学生每一个题目的错误次数和最后一次错误时间
        mistake_stats = answer_records.values("question_id").annotate(
            mistake_count=Count("question_id"),
            last_mistake_time=Max("create_time"),
        ).order_by("-last_mistake_time")

        total = mistake_stats.count()
        # 分页
        mistake_stats_page = mistake_stats[offset:offset + page_size]
        # 学生参加的考试中的错误题目的id
        question_ids = [ms["question_id"] for ms in mistake_stats_page]
        # print(question_ids)

        # 获取错误题目的，题目信息
        correct_questions = Question.objects.filter(id__in=question_ids)
        question_map = {q.id: q for q in correct_questions}
        # print(correct_questions)

        # 获取最后一次答题记录（用于获取用户答案和考试标题）
        last_answer_records = {}
        for record in answer_records:
            qid = record.question_id
            if qid not in last_answer_records or record.create_time > last_answer_records[qid].create_time:
                last_answer_records[qid] = record

        # 构建相应数据中的错误题目
        response_list = []
        for ms in mistake_stats_page:
            qid = ms["question_id"]
            question = question_map.get(qid)
            last_record = last_answer_records.get(qid)
            if not question or not last_record:
                continue
            data = {
                "id": len(response_list) + 1,
                "question_id": question.id,
                "type": question.type,
                "category": question.category,
                "content": question.content,
                "options": question.options,
                "user_answer": last_record.user_answer,
                "correct_answer": question.answer,
                "analysis": question.analysis,
                "mistake_count": ms["mistake_count"],
                "last_mistake_time": ms["last_mistake_time"].strftime("%Y-%m-%d %H:%M:%S"),
                "exam_title": last_record.exam_record.exam.title if last_record.exam_record else ""
            }
            response_list.append(data)

        response_data["list"] = response_list
        response_data["total"] = total

        # 获取统计信息
        statistics = {
            "total_mistakes": answer_records.count(),
            "unique_questions": total,
            "type_distribution": {},
            "category_distribution": {},
            "recent_mistakes": []
        }

        for ms in mistake_stats:
            qid = ms["question_id"]
            question = question_map.get(qid)

            # 跳过已删除的题目
            if not question:
                continue

            statistics["type_distribution"][question.type] = statistics["type_distribution"].get(question.type, 0) + 1
            statistics["category_distribution"][question.category] = statistics["category_distribution"].get(question.category, 0) + 1
            statistics["recent_mistakes"].append({
                "question_id": ms["question_id"],
                "mistake_count": ms["mistake_count"],
                "last_mistake_time": ms["last_mistake_time"].strftime("%Y-%m-%d %H:%M:%S"),
            })

        response_data["statistics"] = statistics
        return MyResponse.success(data=response_data)
