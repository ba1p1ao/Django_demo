from logging import raiseExceptions
from reprlib import aRepr

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied
from apps.question.serializers import QuestionSerializers, QuestionAddSerializers
from apps.question.models import Question
from utils.ResponseMessage import MyResponse


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
