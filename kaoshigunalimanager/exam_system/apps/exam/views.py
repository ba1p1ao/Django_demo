from rest_framework.views import APIView
from rest_framework import viewsets, generics
from django.db import transaction
from django.db.models import Count, Avg, Case, When, FloatField, Q, Max, Min
from apps.exam.models import Exam, ExamRecord, ExamQuestion, AnswerRecord
from apps.user.models import User
from apps.question.models import Question
from apps.exam.serializers import AnswersSerializer, ExamRecordListSerializer, ExamRecordDetailSerializer, ExamSerializer, ExamInfoSerializer, ExamRecordAddSerializer, GroupedExamSerializer
from apps.question.serializers import QuestionListSerializers
from utils.ResponseMessage import MyResponse, check_permission, check_auth # 添加认证的装饰器
from datetime import datetime
from django.utils import timezone




class ExamListView(APIView):

    @check_permission
    def get(self, request):
        payload = request.user
        filter_body = {}
        request_data = request.GET

        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif k == "title" and v:
                filter_body["title__icontains"] = v
            elif v:
                filter_body[k] = v

        # 添加用户权限过滤
        filter_body["creator"] = payload.get("id")

        try:
            page = int(request_data.get("page", 1))
            page_size = int(request_data.get("size", 10))
        except (ValueError, TypeError):
            return MyResponse.failed("页码或每页数量格式错误")

        # 验证分页参数
        if page < 1 or page_size < 1:
            return MyResponse.failed("页码和每页数量必须大于0")

        offset = (page - 1) * page_size

        try:
            exam_queryset = Exam.objects.filter(**filter_body).order_by("-update_time")
            total = exam_queryset.count()
            page_list = exam_queryset[offset:offset + page_size]

            exam_ser_data = ExamSerializer(instance=page_list, many=True).data

            response_data = {
                "list": exam_ser_data,
                "total": total,
                "page": page,
                "size": page_size,
            }
            return MyResponse.success(data=response_data)

        except Exception as e:
            return MyResponse.failed(f"获取试卷列表失败: {str(e)}")


class ExamAddView(APIView):
    @check_permission
    def post(self, request):
        payload = request.user
        request_data = request.data

        # 验证必填字段
        required_fields = ['title', 'duration', 'total_score', 'pass_score']
        for field in required_fields:
            if not request_data.get(field):
                return MyResponse.failed(f"缺少必填字段: {field}")

        # 验证 question_ids
        question_ids = request_data.get("question_ids")
        if not question_ids or not isinstance(question_ids, list):
            return MyResponse.failed("请提供有效的题目ID列表")

        try:
            user = User.objects.get(id=payload.get("id"))
        except User.DoesNotExist:
            return MyResponse.failed("用户不存在")

        # 处理日期时间（格式：YYYY-MM-DD HH:MM:SS）
        start_time = None
        end_time = None
        start_time_str = request_data.get("start_time")
        end_time_str = request_data.get("end_time")

        if start_time_str:
            try:
                naive_start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                start_time = timezone.make_aware(naive_start_time)
            except ValueError:
                return MyResponse.failed("开始时间格式错误，请使用: YYYY-MM-DD HH:MM:SS")

        if end_time_str:
            try:
                naive_end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                end_time = timezone.make_aware(naive_end_time)
            except ValueError:
                return MyResponse.failed("结束时间格式错误，请使用: YYYY-MM-DD HH:MM:SS")

        # 使用事务确保数据一致性
        try:
            with transaction.atomic():
                # 添加试卷
                exam_data = {
                    'title': request_data.get("title"),
                    'description': request_data.get("description"),
                    'duration': request_data.get("duration"),
                    'total_score': request_data.get("total_score"),
                    'pass_score': request_data.get("pass_score"),
                    'start_time': start_time,
                    'end_time': end_time,
                    'is_random': request_data.get("is_random", 0),
                    'creator': user,
                }
                exam = Exam.objects.create(**exam_data)
                
                # 验证题目是否存在
                db_questions = Question.objects.filter(id__in=question_ids)
                if db_questions.count() != len(question_ids):
                    return MyResponse.failed("部分题目ID不存在")

                # 添加试卷题目
                for index, question in enumerate(db_questions, 1):
                    ExamQuestion.objects.create(
                        exam=exam, question=question, sort_order=index
                    )

                return MyResponse.success(message="试卷添加成功", data={"id": exam.id})

        except Exception as e:
            return MyResponse.failed(f"添加试卷失败: {str(e)}")


class ExamModelViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects
    serializer_class = ExamSerializer
    
    @check_auth
    def get(self, request, pk):
        payload = request.user
        
        try:
            exam = self.get_queryset().get(id=pk)
        except Exam.DoesNotExist:
            return MyResponse.failed(message="试卷不存在")
        
        try:
            exam_info = ExamInfoSerializer(instance=exam).data
        except Exception as e:
            return MyResponse.failed(message="试卷获取失败")
        
        # print(exam_info)
     
        return MyResponse.success(data=exam_info)
    
    
    @check_permission
    def put(self, request, pk):
        payload = request.user
        try:
            exam = self.get_queryset().get(id=pk, creator_id=payload.get("id"))
        except Exam.DoesNotExist:
            return MyResponse.failed(message="试卷不存在")


        request_data = request.data.copy()
        question_ids = request_data.get("question_ids")

        # 移除 question_ids 和不允许修改的字段
        request_data.pop("question_ids", None)
        request_data.pop("id", None)
        request_data.pop("creator", None)
        request_data.pop("create_time", None)
        request_data.pop("update_time", None)

        # 处理日期时间
        start_time_str = request_data.get("start_time")
        end_time_str = request_data.get("end_time")

        if start_time_str:
            try:
                naive_start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                request_data["start_time"] = timezone.make_aware(naive_start_time)
            except ValueError:
                return MyResponse.failed("开始时间格式错误，请使用: YYYY-MM-DD HH:MM:SS")

        if end_time_str:
            try:
                naive_end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                request_data["end_time"] = timezone.make_aware(naive_end_time)
            except ValueError:
                return MyResponse.failed("结束时间格式错误，请使用: YYYY-MM-DD HH:MM:SS")

        if not question_ids or not isinstance(question_ids, list):
            return MyResponse.failed("请提供有效的题目ID列表")

        try:
            with transaction.atomic():
                # 更新试卷信息
                for key, value in request_data.items():
                    if hasattr(exam, key):
                        setattr(exam, key, value)
                exam.save()

                # 获取原试卷的题目id
                old_questions = ExamQuestion.objects.filter(exam=exam).values("question_id")
                old_question_ids = [question.get("question_id") for question in old_questions]

                # 排序方便快速查找不同的qid
                old_question_ids.sort()
                question_ids.sort()
                add_qids = []
                del_qids = []

                # 找出需要添加和删除的题目
                for cur_qid in question_ids:
                    if cur_qid not in old_question_ids:
                        add_qids.append(cur_qid)

                for cur_qid in old_question_ids:
                    if cur_qid not in question_ids:
                        del_qids.append(cur_qid)

                # 删除题目
                if del_qids:
                    ExamQuestion.objects.filter(exam=exam, question_id__in=del_qids).delete()

                # 添加题目
                if add_qids:
                    add_questions = Question.objects.filter(id__in=add_qids)
                    if add_questions.count() != len(add_qids):
                        return MyResponse.failed("部分题目ID不存在")

                    # 获取当前最大排序
                    max_sort_obj = ExamQuestion.objects.filter(exam=exam).order_by('-sort_order').first()
                    start_sort = max_sort_obj.sort_order if max_sort_obj else 0

                    for index, question in enumerate(add_questions, 1):
                        ExamQuestion.objects.create(
                            exam=exam,
                            question=question,
                            sort_order=start_sort + index
                        )

                return MyResponse.success("修改成功")

        except Exception as e:
            return MyResponse.failed(f"修改试卷失败: {str(e)}")


    @check_permission
    def delete(self, request, pk):
        payload = request.user

        try:
            exam = self.get_queryset().get(id=pk, creator_id=payload.get("id"))
        except Exam.DoesNotExist:
            return MyResponse.failed(message="试卷不存在")

        # 检查试卷状态
        if exam.status != "closed":
            return MyResponse.failed(message="无法删除正在发布的试卷")

        # 检查是否有考试记录
        if ExamRecord.objects.filter(exam=exam).exists():
            return MyResponse.failed(message="该试卷已有考试记录，无法删除")

        try:
            with transaction.atomic():
                # 先删除关联的题目
                ExamQuestion.objects.filter(exam=exam).delete()

                # 再删除试卷
                exam.delete()

                return MyResponse.success("删除成功")

        except Exception as e:
            return MyResponse.failed(f"删除试卷失败: {str(e)}")
        
        

class ExamPublishView(APIView):
    @check_permission
    def put(self, request, pk):
        payload = request.user
        update_count = Exam.objects.filter(id=pk, creator_id=payload.get("id")).update(status="published")
        if not update_count:
            return MyResponse.failed(message="修改试卷失败")
        return MyResponse.success(message="修改成功")
    


class ExamCloseView(APIView):
    @check_permission
    def put(self, request, pk):
        payload = request.user
        update_count = Exam.objects.filter(id=pk, creator_id=payload.get("id")).update(status="closed")
        if not update_count:
            return MyResponse.failed(message="修改试卷失败")
        return MyResponse.success(message="修改成功")
    

class ExamAvailableView(generics.ListAPIView):
    queryset = Exam.objects
    serializer_class = ExamSerializer
    @check_auth
    def list(self, request, *args, **kwargs):
        payload = request.user
        exam_list = self.get_queryset().filter(status="published")
        if not exam_list:
            return MyResponse.success("没有考试内容")

        # 判断试卷的时间是否结束
        valid_exam_list = []
        # 前端做了限制，所以后端直接返回全部数据即可
        # 判断用户是否为管理员如果是则返回所有试卷，如果是学生则返回有效的试卷
        # if payload.get("role") not in ["teacher", "admin"]:
        #     current_time = timezone.localtime()
        #     for exam in exam_list:
        #         if exam.end_time > current_time:
        #             valid_exam_list.append(exam)
        # else:
        valid_exam_list = exam_list
        exam_ser_data = self.get_serializer(instance=valid_exam_list, many=True).data
        return MyResponse.success(data=exam_ser_data)
              


class ExamStartView(generics.CreateAPIView):
    queryset = ExamRecord.objects
    serializer_class = ExamRecordAddSerializer
    @check_auth
    def post(self, request):
        payload = request.user

        exam_id = request.data.get("exam_id")
        user_id = payload.get("id")
        exam = Exam.objects.filter(id=exam_id, status="published").first()
        if not exam:
            return MyResponse.failed(message="该试卷不存在，请联系老师或管理员")

        user = User.objects.filter(id=user_id).first()

        # 检查是否允许重复作答
        if exam.allow_retake == 0:
            # 不允许重复作答，检查是否已完成考试
            completed_record = ExamRecord.objects.filter(
                exam_id=exam_id,
                user_id=user_id,
                status__in=["submitted", "graded"]
            ).first()
            if completed_record:
                return MyResponse.failed("您已完成该考试，不能重复作答")
            
        # 判断该学生是否开始进行该试卷的考试
        exam_record = ExamRecord.objects.filter(exam_id=exam_id, user_id=user_id, status="in_progress").first()
        if exam_record:
            current_time = timezone.localtime()
            exam_end_time = exam.end_time
            if current_time >= exam_end_time:
                return MyResponse.failed("该试卷已经结束，无法进行考试")
            else:
                # 使用 timezone.localtime 将 UTC 时间转换为本地时间
                start_time_local = timezone.localtime(exam_record.start_time)
                response_data = {
                    "id": exam_record.id,
                    "exam_id": exam_id,
                    "user_id": user_id,
                    "status": exam_record.status,
                    "start_time": start_time_local.strftime("%Y-%m-%d %H:%M:%S"),
                    "duration": exam.duration,  # 考试时长（分钟）
                }
                return MyResponse.success(data=response_data)

        db_data = {
            "exam": exam.id,  # 传入 ID 而不是对象
            "user": user.id,  # 传入 ID 而不是对象
            "status": "in_progress",
            "start_time": timezone.now()
        }
        exam_record_ser = self.get_serializer(data=db_data)
        try:
            if exam_record_ser.is_valid(raise_exception=True):
                exam_record = exam_record_ser.save()
                # 使用 timezone.localtime 将 UTC 时间转换为本地时间
                start_time_local = timezone.localtime(exam_record.start_time)
                response_data = {
                    "id": exam_record.id,
                    "exam_id": exam_id,
                    "user_id": user_id,
                    "status": exam_record.status,
                    "start_time": start_time_local.strftime("%Y-%m-%d %H:%M:%S"),
                    "duration": exam.duration,  # 考试时长（分钟）
                }
                return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(message=f"{e}")

        return MyResponse.failed()
        
        
    
class ExamQuestionsView(APIView):
    @check_auth
    def get(self, request, exam_id):
        payload = request.user

        exam = Exam.objects.filter(id=exam_id, status="published").first()
        if not exam:
            return MyResponse.failed(message="该试卷不存在，请联系老师或管理员")

        exam_questions = ExamQuestion.objects.filter(exam_id=exam_id)
        if not exam_questions:
            return MyResponse.failed(message="该试卷没有题目，请联系老师或管理员")

        try:
            questions = [eq.question for eq in exam_questions]
            ser_question_data = QuestionListSerializers(instance=questions, many=True).data

            # 获取当前用户的考试记录ID（如果有进行中的考试）
            exam_record = ExamRecord.objects.filter(
                exam_id=exam_id,
                user_id=payload.get("id"),
                status="in_progress"
            ).first()

            # 如果有进行中的考试，获取已保存的答案
            saved_answers = {}
            if exam_record:
                answer_records = AnswerRecord.objects.filter(exam_record=exam_record)
                for ar in answer_records:
                    saved_answers[ar.question_id] = ar.user_answer

            # 将已保存的答案添加到返回数据中
            response_data = {
                "questions": ser_question_data,
                "exam_record_id": exam_record.id if exam_record else None,
                "saved_answers": saved_answers
            }

            return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(message="该试卷发生错误，请联系老师或管理员")

class ExamAnswerView(APIView):
    """保存答案"""
    @check_auth
    def post(self, request):
        payload = request.user
        request_data = request.data
        exam_record_id = request_data.get("exam_record_id")
        question_id = request_data.get("question_id")
        user_answer = request_data.get("user_answer")

        if not all([exam_record_id, question_id]):
            return MyResponse.failed(message="缺少必填字段")

        try:
            exam_record = ExamRecord.objects.get(id=exam_record_id, user_id=payload.get("id"))
        except ExamRecord.DoesNotExist:
            return MyResponse.failed(message="考试记录不存在")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return MyResponse.failed(message="题目不存在")

        try:
            with transaction.atomic():
                # 判断是否存在答题记录
                answer_record = AnswerRecord.objects.filter(
                    exam_record_id=exam_record_id,
                    question_id=question_id
                ).first()

                if answer_record:
                    answer_record.user_answer = user_answer
                    answer_record.save()
                else:
                    AnswerRecord.objects.create(
                        exam_record_id=exam_record_id,
                        question_id=question_id,
                        user_answer=user_answer
                    )

                return MyResponse.success(message="答案保存成功")

        except Exception as e:
            return MyResponse.failed(message=f"保存答案失败: {str(e)}")


class ExamSubmitView(APIView):
    """提交试卷"""
    @check_auth
    def post(self, request):
        payload = request.user
        exam_record_id = request.data.get("exam_record_id")

        if not exam_record_id:
            return MyResponse.failed(message="缺少必填字段")

        try:
            exam_record = ExamRecord.objects.get(
                id=exam_record_id,
                user_id=payload.get("id"),
                status="in_progress"
            )
        except ExamRecord.DoesNotExist:
            return MyResponse.failed(message="考试记录不存在或已完成")

        try:
            with transaction.atomic():
                # 获取试卷的所有题目
                exam_questions = ExamQuestion.objects.filter(exam=exam_record.exam)
                questions = [eq.question for eq in exam_questions]

                total_score = 0

                # 计算得分 - 从数据库获取已保存的答案
                for question in questions:
                    answer_record = AnswerRecord.objects.filter(
                        exam_record=exam_record,
                        question=question
                    ).first()

                    if answer_record and answer_record.user_answer:
                        # 判断答案是否正确
                        is_correct = self.check_answer(question, answer_record.user_answer)

                        if is_correct:
                            answer_record.is_correct = 1
                            answer_record.score = question.score
                            total_score += question.score
                        else:
                            answer_record.is_correct = 0
                            answer_record.score = 0

                        answer_record.save()

                # 更新考试记录
                exam_record.score = total_score
                exam_record.is_passed = 1 if total_score >= exam_record.exam.pass_score else 0
                exam_record.status = "graded"
                exam_record.submit_time = timezone.localtime()
                exam_record.save()

                return MyResponse.success(
                    message="试卷提交成功",
                    data={
                        "id": exam_record.id,
                        "score": total_score,
                        "is_passed": exam_record.is_passed,
                        "status": exam_record.status,
                        "submit_time": exam_record.submit_time.strftime("%Y-%m-%d %H:%M:%S") if exam_record.submit_time else None
                    }
                )
        except Exception as e:
            return MyResponse.failed(message=f"提交试卷失败: {str(e)}")

    def check_answer(self, question, user_answer):
        """检查答案是否正确"""
        correct_answer = question.answer.strip().upper()
        user_answer = user_answer.strip().upper()

        if question.type == "single":
            return correct_answer == user_answer
        elif question.type == "multiple":
            # 多选题：答案完全匹配（顺序可能不同）
            correct_answer = correct_answer.replace("[", "").replace("]", "").replace('"', "")
            correct_set = set(correct_answer.split(","))
            user_set = set(user_answer.split(","))
            return correct_set == user_set
        elif question.type == "judge":
            return correct_answer == user_answer
        elif question.type == "fill":
            # 填空题：完全匹配
            return correct_answer == user_answer

        return False

class ExamRecordListView(APIView):
    @check_auth
    def get(self, request):
        payload = request.user
        request_data = request.GET
        
        # 参数验证
        try:
            page = int(request_data.get("page", 1))
            page_size = int(request_data.get("size", 10))
        except (ValueError, TypeError):
            return MyResponse.failed(message="页码和每页数量必须是整数")
        
        filter_body = {}
        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif k == "title" and v:
                # 需要关联 exam 表查询
                continue
            elif v:
                filter_body[k] = v

        # 添加userid, 排除老师和管理员
        user_role = payload.get("role") if isinstance(payload, dict) else getattr(payload, 'role', None)
        user_id = payload.get("id") if isinstance(payload, dict) else getattr(payload, 'id', None)
        
        if user_role not in ["teacher", "admin"]:
            filter_body["user_id"] = user_id
        
        offset = (page - 1) * page_size

        try:
            exam_records = ExamRecord.objects.filter(**filter_body).select_related('exam').order_by("-update_time")
            
            # 如果有 title 参数，进行额外的过滤
            title = request_data.get("title", "")
            if title:
                exam_records = exam_records.filter(exam__title__icontains=title)
            
            total = exam_records.count()
            page_list = exam_records[offset:offset + page_size]
            ser_exam_record_data = ExamRecordListSerializer(instance=page_list, many=True).data
            response_data = {
                "list": ser_exam_record_data,
                "total": total,
                "page": page,
                "size": page_size
            }
            return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(f"获取考试记录列表失败: {str(e)}") 

        

class ExamRecordDetailView(APIView):
    @check_auth
    def get(self, request, pk):
        payload = request.user
        user_role = payload.get("role") if isinstance(payload, dict) else getattr(payload, 'role', None)
        user_id = payload.get("id") if isinstance(payload, dict) else getattr(payload, 'id', None)
        
        try:
            # 老师和管理员可以查看所有考试记录，学生只能查看自己的
            if user_role in ["teacher", "admin"]:
                exam_record = ExamRecord.objects.get(id=pk)
            else:
                exam_record = ExamRecord.objects.get(id=pk, user_id=user_id)
        except ExamRecord.DoesNotExist:
            return MyResponse.failed("考试记录不存在")
            
        ser_answer_record_data = ExamRecordDetailSerializer(instance=exam_record).data
        return MyResponse.success(data=ser_answer_record_data)

class ExamRecordStatisticsView(APIView):
    @check_permission
    def get(self, request, exam_id):
        # 检查考试是否存在
        exam = Exam.objects.filter(id=exam_id).first()
        if not exam:
            return MyResponse.failed("考试不存在")
        
        # 获取已提交且已阅卷的记录
        exam_records = ExamRecord.objects.filter(
            exam_id=exam_id,
            status='graded'
        )
        
        # 如果没有记录，返回默认值
        if not exam_records.exists():
            return MyResponse.success(data={
                "total_participants": 0,
                "average_score": None,
                "pass_rate": None,
                "max_score": None,
                "min_score": None,
                "question_stats": []
            })
        
        # 统计考试记录数据
        stats = exam_records.aggregate(
            total_participants=Count('user_id', distinct=True),
            average_score=Avg('score'),
            pass_rate=Avg(
                Case(
                    When(is_passed=1, then=1.0),
                    When(is_passed=0, then=0.0),
                    default=None,
                    output_field=FloatField()
                )
            ),
            max_score=Max('score'),
            min_score=Min('score')
        )
        
        # 一次性统计所有题目的正确率（优化查询）
        question_stats = AnswerRecord.objects.filter(
            exam_record__exam_id=exam_id,
            exam_record__status='graded'
        ).values('question_id').annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=1)),
            correct_rate=Avg(
                Case(
                    When(is_correct=1, then=1.0),
                    When(is_correct=0, then=0.0),
                    default=None,
                    output_field=FloatField()
                )
            )
        ).order_by('question_id')
        
        # 格式化题目统计数据
        question_stats_list = [
            {
                "question_id": q['question_id'],
                "correct_rate": round(q['correct_rate'], 2) if q['correct_rate'] else 0
            }
            for q in question_stats
        ]
        
        # 组装返回数据
        response_data = {
            "total_participants": stats['total_participants'],
            "average_score": round(stats['average_score'], 2) if stats['average_score'] else None,
            "pass_rate": round(stats['pass_rate'], 2) if stats['pass_rate'] else None,
            "max_score": stats['max_score'],
            "min_score": stats['min_score'],
            "question_stats": question_stats_list
        }
        
        return MyResponse.success(data=response_data)
       

class GroupedExamRecordListView(APIView):
    @check_permission
    def get(self, request):
        # 获取查询参数，添加错误处理
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('size', 10))
        except (ValueError, TypeError):
            return MyResponse.failed(message="页码和每页数量必须是整数")
        
        if page < 1 or page_size < 1:
            return MyResponse.failed(message="页码和每页数量必须大于0")
        
        title = request.GET.get('title', '')
        status = request.GET.get('status', '')
        
        # 获取学生筛选参数
        student_username = request.GET.get('student_username', '')
        student_nickname = request.GET.get('student_nickname', '')
        student_status = request.GET.get('student_status', '')
        student_is_passed = request.GET.get('student_is_passed', '')
        
        # 构建查询条件
        queryset = Exam.objects.all()
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        if status:
            queryset = queryset.filter(status=status)
        else:
            # 默认只显示已发布和已关闭的考试
            queryset = queryset.filter(status__in=['published', 'closed'])
        
        # 使用 annotate 添加统计字段，避免 N+1 查询
        queryset = queryset.annotate(
            participant_count=Count(
                'examrecord__user_id',
                filter=Q(examrecord__status='graded'),
                distinct=True  # 去重，统计实际参加人数
            ),
            average_score=Avg('examrecord__score', filter=Q(examrecord__status='graded')),
            pass_rate=Avg(
                Case(
                    When(examrecord__is_passed=1, then=1.0),
                    When(examrecord__is_passed=0, then=0.0),
                    default=None,
                    output_field=FloatField()
                ),
                filter=Q(examrecord__status='graded')
            )
        )
        
        total = queryset.count()
        offset = (page - 1) * page_size
        exams = queryset.order_by('-create_time')[offset:offset + page_size]
        
        try:
            # 传递学生筛选参数到序列化器
            group_exam_data = GroupedExamSerializer(
                instance=exams, 
                many=True,
                context={
                    'student_username': student_username,
                    'student_nickname': student_nickname,
                    'student_status': student_status,
                    'student_is_passed': student_is_passed
                }
            ).data
            response_data = {
                "list": group_exam_data,
                "total": total,
                "page": page,
                "size": page_size,
            }
            return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(message=f"获取考试信息错误，{e}")


class SystemStatisticsView(APIView):
    @check_auth
    def get(self, request):
        # 统计题目总数
        question_count = Question.objects.count()

        # 统计试卷总数
        exam_count = Exam.objects.count()

        # 统计考试记录总数
        record_count = ExamRecord.objects.count()

        # 统计用户总数
        user_count = User.objects.count()

        response_data = {
            "question_count": question_count,
            "exam_count": exam_count,
            "record_count": record_count,
            "user_count": user_count
        }

        return MyResponse.success(data=response_data)


class ExamRankingView(APIView):
    @check_auth
    def get(self, request, exam_id):
        payload = request.user
        
        page = int(request.GET.get("page"))
        page_size = int(request.GET.get("size"))
        offset = (page - 1) * page_size
        # 获取当前试卷
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return MyResponse.failed(message="试卷不存在")
        
        response_data = {
            "exam_id": exam_id,
            "exam_title": exam.title,
            "list": []
        }
        class_id = request.GET.get("class_id")
        cur_class_students = User.objects.filter(role="student")
        # print(cur_class_students)
        if class_id:
            cur_class_students = User.objects.filter(role="student", userclass__class_info_id=class_id)

        # print(cur_class_students)
        # exam_record = exam_record.annotate(
        #     max_score=Max("score"),
        # ).values("user_id", "max_score")
        # print(exam_record)
        user_score_list = cur_class_students.annotate(
            max_score=Max("examrecord__score", filter=Q(examrecord__exam_id=exam_id)),
        ).values("id", "username", "nickname", "max_score").order_by("-max_score")
                
        response_data["total_participants"] = user_score_list.count()
        # print(user_score_list)
        try:
            for index, user_score in enumerate(user_score_list, 1):
                exam_record_best = ExamRecord.objects.filter(
                    exam_id=exam_id, 
                    user_id=user_score["id"],
                    score=user_score["max_score"]
                ).values("is_passed", "submit_time").first()
                if not exam_record_best:
                    continue
                rank_list_dict = {}          
                rank_list_dict["rank"] = index
                rank_list_dict["user_id"] = user_score["id"]
                rank_list_dict["username"] = user_score["username"]
                rank_list_dict["nickname"] = user_score["nickname"]
                rank_list_dict["score"] = user_score["max_score"]
    
                # 获取学生最高成绩的考试记录

                rank_list_dict["is_passed"] = exam_record_best["is_passed"]
                rank_list_dict["submit_time"] = exam_record_best["submit_time"].strftime("%Y-%m-%d %H:%M:%S")
                if user_score["id"] == payload.get("id"):
                    response_data["my_rank"] = index
                    response_data["my_score"] = user_score["max_score"]
                
                response_data["list"].append(rank_list_dict)

            response_data["list"] = response_data["list"][offset:offset + page_size]
            return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(message="排名信息获取失败")
            
        
