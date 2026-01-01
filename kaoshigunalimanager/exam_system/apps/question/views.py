import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied
from apps.question.serializers import QuestionSerializers, QuestionAddSerializers
from apps.question.models import Question
from apps.user.models import User
from utils.ResponseMessage import MyResponse, check_permission, check_auth
from django.db import transaction

class QuestionListView(APIView):
    # /api/question/list/?page=1&size=10&type=&category=&difficulty= HTTP/1.1" 200 16850
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

        question_list = Question.objects.filter(**filter_body).all().order_by("-update_time")
        page_list = question_list[offset:offset + page_size]
        ser_data = QuestionSerializers(instance=page_list, many=True).data
        response_data = {
            "list": ser_data,
            "total": len(question_list),
            "page": page,
            "size": page_size,
        }
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
        ser_data = self.get_serializer(instance=question).data
        # print(ser_data)
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
                return MyResponse.success("更新成功")
        except Exception as e:
            return MyResponse.failed(message=e)

    def destroy(self, request, *args, **kwargs):
        payload = self.get_payload()
        if isinstance(payload, MyResponse):
            return payload
        question = self.get_object()
        self.perform_destroy(question)
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
                return MyResponse.success(message='添加成功', data={"id": payload.get("id")})
        except Exception as e:
            print(e)
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
        # print(delete_count)
        if delete_count:
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
        questions: list[dict] = self.process_import_data(df)
        
        print(questions)
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
            with transaction.atomic():
                for question in questions:
                    question["creator"] = current_user
                    question_index = question.pop("index")
                    create_count = Question.objects.create(**question)
                    if not create_count:
                        failed_count += 1
                        failed_list.append({
                            "row": question_index,
                            "reason": f'{question.get("content")} 格式存在错误'
                        })
                        # return MyResponse.failed(message=f'{question.get("content")} 格式存在错误')
                    else:
                        success_count += 1
                
                response_data["success"] = success_count
                response_data["failed"] = failed_count
                response_data["failed_list"] = failed_list
                return MyResponse.success(message="题目导入成功", data=response_data) 
        except Exception as e:
            return MyResponse.failed(f"题目导入失败，{e}")
        
    
    def process_import_data(self, df):
        # 题目类型
        TYPE = {
            "单选题": "single",
            "单选": "single",
            "多选题": "multiple",
            "多选": "multiple",
            "判断题": "judge",
            "判断": "judge",    
            "填空题": "fill",
            "填空": "fill",
        }

        # 难度
        DIFFICULTY = {
            "easy": "easy",
            "简单": "easy",
            "medium": "medium",
            "中等": "medium",     
            "hard": "hard",
            "困难": "hard",
        }
            
        questions = []
        try:
            for index, row in df.iterrows():
                question = {}
                question["index"] = index
                question["type"] = TYPE.get(row["题目类型"])
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
                question["difficulty"] = DIFFICULTY.get(row["难度"])
                question["score"] = row["分值"]
                
                questions.append(question)
            
            return questions
        except Exception as e:
            return MyResponse.failed(message="格式存在错误，请下载导入模板，按模板的格式填写")