import logging
import pandas as pd
import io
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.http import FileResponse
from urllib.parse import quote
from apps.question.serializers import QuestionListSerializers, QuestionSerializers, QuestionAddSerializers
from apps.question.models import Question
from apps.user.models import User
from utils.ResponseMessage import MyResponse, check_permission
from django.db import transaction
from utils.CacheConfig import (
    CACHE_KEY_QUESTION_LIST,
    CACHE_TIMEOUT_QUESTION_LIST,
    CACHE_KEY_QUESTION_DETAIL,
    CACHE_TIMEOUT_QUESTION_DETAIL,
    generate_cache_key,
    generate_filter_key, CACHE_KEY_SYSTEM_STATISTICS, CACHE_TIMEOUT_EMPTY_RESULT
)
from utils.CacheTools import cache_delete_pattern
from django.core.cache import cache


logger = logging.getLogger('apps')

# 题目类型映射常量
QUESTION_TYPE_MAP = {
    # 导入用
    "单选题": "single",
    "单选": "single",
    "多选题": "multiple",
    "多选": "multiple",
    "判断题": "judge",
    "判断": "judge",
    "填空题": "fill",
    "填空": "fill",
    # 导出用
    "single": "单选题",
    "multiple": "多选题",
    "judge": "判断题",
    "fill": "填空题",
}

# 难度映射常量
DIFFICULTY_MAP = {
    # 导入用
    "简单": "easy",
    "中等": "medium",
    "困难": "hard",
    # 导出用
    "easy": "简单",
    "medium": "中等",
    "hard": "困难",
}

class QuestionListView(APIView):

    def get(self, request):
        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        if payload.get("role") not in ["teacher", "admin"]:
            return MyResponse.other(code=403, message="只有教师和管理员可以访问题库")

        filter_body = {}
        request_data = request.GET
        for k, v in request_data.items():
            if k == "page" or k == "size":
                continue
            elif k == "content" and v:
                filter_body["content__icontains"] = v
            elif v:
                filter_body[k] = v

        page = int(request_data.get("page", 1))
        page_size = int(request_data.get("size", 10))
        offset = (page - 1) * page_size

        # 生成缓存键
        filters = generate_filter_key(filter_body)
        cache_key = generate_cache_key(
            CACHE_KEY_QUESTION_LIST, filter=filters, page=page, size=page_size
        )
        # 尝试从缓存获取
        cache_data = cache.get(cache_key)
        if cache_data:
           return MyResponse.success(data=cache_data)

        question_list = Question.objects.filter(**filter_body).all().order_by("-update_time")
        page_list = question_list[offset:offset + page_size]
        ser_data = QuestionSerializers(instance=page_list, many=True).data
        response_data = {
            "list": ser_data,
            "total": len(question_list),
            "page": page,
            "size": page_size,
        }
        # 这是缓存
        if not ser_data:
            cache.set(cache_key, response_data, CACHE_TIMEOUT_EMPTY_RESULT)
        else:
            cache.set(cache_key, response_data, CACHE_TIMEOUT_QUESTION_LIST)
        return MyResponse.success(data=response_data)


class QuestionInfoView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Question.objects
    serializer_class = QuestionSerializers
    lookup_field = "id"

    def get_payload(self):
        payload = self.request.user

        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        if payload.get("role") not in ["teacher", "admin"]:
            return MyResponse.other(code=403, message="只有教师和管理员可以访问题库")

    def retrieve(self, request, *args, **kwargs):
        payload = self.get_payload()
        if isinstance(payload, MyResponse):
            return payload
        question = self.get_object()

        # 设置 cache key
        cache_key = generate_cache_key(CACHE_KEY_QUESTION_DETAIL, id=question.id)
        # 获取 缓存数据
        cache_data = cache.get(cache_key)
        if cache_data:
            return MyResponse.success(data=cache_data)

        ser_data = self.get_serializer(instance=question).data
        cache.set(cache_key, ser_data, CACHE_TIMEOUT_QUESTION_DETAIL)
        return MyResponse.success(data=ser_data)

    def update(self, request, *args, **kwargs):
        payload = self.get_payload()
        if isinstance(payload, MyResponse):
            return payload

        question = self.get_object()
        request_data = request.data

        question_ser = QuestionAddSerializers(instance=question, data=request_data, partial=True)
        try:
            if question_ser.is_valid(raise_exception=True):
                question_ser.save()
                logger.info(f"题目 ID {question.id} 更新成功")
                cache.delete(generate_cache_key(CACHE_KEY_QUESTION_DETAIL, id=question.id))
                cache_delete_pattern("question:list:*")
                # 清除包含该题目的考试题目缓存
                cache_delete_pattern("exam:questions:*")
                cache_delete_pattern("class:ranking:*")
                cache_delete_pattern("class:trend:*")
                # 清除系统统计缓存
                cache.delete(CACHE_KEY_SYSTEM_STATISTICS)
                return MyResponse.success("更新成功")
        except Exception as e:
            logger.error(f"题目 ID {question.id} 更新失败: {e}")
            return MyResponse.failed(message=e)

    def destroy(self, request, *args, **kwargs):
        payload = self.get_payload()
        if isinstance(payload, MyResponse):
            return payload
        question = self.get_object()
        question_id = question.id
        self.perform_destroy(question)
        logger.info(f"题目 ID {question_id} 删除成功")
        cache.delete(generate_cache_key(CACHE_KEY_QUESTION_DETAIL, id=question_id))
        cache_delete_pattern("question:list:*")
        # 清除包含该题目的考试题目缓存
        cache_delete_pattern("exam:questions:*")
        cache_delete_pattern("class:ranking:*")
        cache_delete_pattern("class:trend:*")
        # 清除系统统计缓存
        cache.delete(CACHE_KEY_SYSTEM_STATISTICS)
        return MyResponse.success("删除成功")


class QuestionAddView(CreateAPIView):
    queryset = Question.objects
    serializer_class = QuestionAddSerializers

    def create(self, request, *args, **kwargs):
        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        if payload.get("role") not in ["teacher", "admin"]:
            return MyResponse.other(code=403, message="只有教师和管理员可以访问题库")
        request_data = request.data
        request_data["creator"] = payload.get("id")
        question_ser = self.get_serializer(data=request_data)
        try:
            if question_ser.is_valid(raise_exception=True):
                question_ser.save()
                logger.info(f"用户 {payload.get('username')} 添加题目成功")
                cache_delete_pattern("question:list:*")
                # 清除系统统计缓存
                cache.delete(CACHE_KEY_SYSTEM_STATISTICS)
                return MyResponse.success(message='添加成功', data={"id": payload.get("id")})
        except Exception as e:
            logger.error(f"用户 {payload.get('username')} 添加题目失败: {e}")
            return MyResponse.failed(message=e)


class QuestionDeleteListView(APIView):
    @check_permission
    def delete(self, request):
        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        if payload.get("role") not in ["teacher", "admin"]:
            return MyResponse.other(code=403, message="只有教师和管理员可以访问题库")

        ids = request.data.get("ids")
        if not ids:
            return MyResponse.other(code=404, message="请选择要删除的题目")

        delete_count = Question.objects.filter(id__in=ids).delete()
        if delete_count:
            logger.info(f"用户 {payload.get('username')} 批量删除题目成功，数量: {len(ids)}")
            cache.delete_many([generate_cache_key(CACHE_KEY_QUESTION_DETAIL, id=id) for id in ids])
            cache_delete_pattern("question:list:*")
            # 清除包含这些题目的考试题目缓存
            cache_delete_pattern("exam:questions:*")
            # 清除系统统计缓存
            cache.delete(CACHE_KEY_SYSTEM_STATISTICS)
            return MyResponse.success(message="批量删除成功")

        return MyResponse.other(code=404, message="请选择要删除的题目")



class QuestionImportView(APIView):
    # 添加文件解析器
    parser_classes = [MultiPartParser, FormParser]

    @check_permission
    def post(self, request):
        payload = request.user

        question_file = request.FILES.get("file")
        if not question_file:
            return MyResponse.failed("只能上传 .xlsx/.xls 文件，且不超过 10MB ")

        file_name = question_file.name.lower()
        if not ((file_name.endswith(".xlsx") or  file_name.endswith(".xls")) and question_file.size <= 10 * 1024 * 1024):
            return MyResponse.failed("只能上传 .xlsx/.xls 文件，且不超过 10MB ")

        df = pd.read_excel(question_file)
        questions = self.process_import_data(df)

        current_user = User.objects.get(id=payload.get("id"))
        response_data = {
            "total": len(questions),
            "success": 0,
            "failed": 0,
            "failed_list": []
        }
        try:
            success_count = 0
            failed_count = 0
            failed_list = []
            valid_questions = []

            with transaction.atomic():
                for question in questions:
                    question["creator"] = current_user
                    question_index = question.pop("index")

                    # 验证必填字段
                    if not all([question.get("type"), question.get("content"), question.get("answer")]):
                        failed_count += 1
                        failed_list.append({
                            "row": question_index,
                            "reason": f'{question.get("content", "未知")} 缺少必填字段'
                        })
                        continue

                    valid_questions.append(Question(**question))
                    success_count += 1

                # 批量创建题目
                if valid_questions:
                    Question.objects.bulk_create(valid_questions)

                response_data["success"] = success_count
                response_data["failed"] = failed_count
                response_data["failed_list"] = failed_list
                logger.info(f"用户 {current_user.username} 导入题目成功，成功: {success_count}，失败: {failed_count}")
                # 清除题目列表缓存
                cache_delete_pattern("question:list:*")
                # 清除系统统计缓存
                cache.delete(CACHE_KEY_SYSTEM_STATISTICS)
                return MyResponse.success(message="题目导入成功", data=response_data)
        except Exception as e:
            logger.error(f"用户 {payload.get('username')} 导入题目失败: {e}")
            return MyResponse.failed(f"题目导入失败，{e}")


    def process_import_data(self, df):
        questions = []
        try:
            for index, row in df.iterrows():
                question = {}
                question["index"] = index
                question["type"] = QUESTION_TYPE_MAP.get(row["题目类型"])
                question["category"] = row["题目分类"]
                question["content"] = row["题目内容"]
                question["options"] = None
                if question["type"] == "fill":
                    question["options"] = None
                elif question["type"] == "judge":
                    question["options"] = {"A": "正确", "B": "错误"}
                else:
                    question["options"] = {"A": row["选项A"], "B": row["选项B"], "C": row["选项C"], "D": row["选项D"]}
                question["answer"] = row["正确答案"]
                question["analysis"] = row["题目解析"]
                question["difficulty"] = DIFFICULTY_MAP.get(row["难度"])
                question["score"] = row["分值"]

                questions.append(question)

            return questions
        except Exception as e:
            return MyResponse.failed(message="格式存在错误，请下载导入模板，按模板的格式填写")


class QuestionExportView(APIView):
    @check_permission
    def post(self, request):
        ids = request.data.get("ids")
        questions = Question.objects.filter(id__in=ids)
        if not questions:
            return MyResponse.failed(message="请选择要导出的题目")
        ser_question_data = QuestionListSerializers(instance=questions, many=True).data

        try:
            # 使用内存流生成文件
            excel_buffer = self.export_to_excel(ser_question_data)

            logger.info(f"用户 {request.user.get('username')} 导出题目成功，数量: {len(ids)}")

            # 返回文件供前端下载
            filename = f"题目导出_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            encoded_filename = quote(filename)

            response = FileResponse(
                excel_buffer,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            return response
        except Exception as e:
            logger.error(f"用户 {request.user.get('username')} 导出题目失败: {e}")
            return MyResponse.failed(f"到处文件是发生错误，{e}")


    def export_to_excel(self, questions):
        frame = {
            "题目类型": [],
            "题目分类": [],
            "题目内容": [],
            "选项A": [],
            "选项B": [],
            "选项C": [],
            "选项D": [],
            "正确答案": [],
            "题目解析": [],
            "难度": [],
            "分值": [],
        }

        for question in questions:
            frame['题目类型'].append(QUESTION_TYPE_MAP.get(question["type"]))
            frame['题目分类'].append(question["category"])
            frame['题目内容'].append(question["content"])

            if question.get("options") and question["type"] != 'judge':
                frame['选项A'].append(question.get("options").get("A"))
                frame['选项B'].append(question.get("options").get("B"))
                frame['选项C'].append(question.get("options").get("C"))
                frame['选项D'].append(question.get("options").get("D"))
            else:
                frame['选项A'].append(None)
                frame['选项B'].append(None)
                frame['选项C'].append(None)
                frame['选项D'].append(None)

            frame['正确答案'].append(question["answer"])
            frame['题目解析'].append(question["analysis"])
            frame['难度'].append(DIFFICULTY_MAP.get(question["difficulty"]))
            frame['分值'].append(question["score"])

        # 创建 DataFrame
        df = pd.DataFrame(frame)

        # 使用内存流代替临时文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='题目列表', index=False)

        # 重置指针到开头
        output.seek(0)
        return output