# from unittest import skipIf
#
# from django.http import HttpResponse
# from rest_framework.generics import GenericAPIView
# from rest_framework.viewsets import ViewSetMixin, ModelViewSet
# from rest_framework.mixins import *
# from apps.comment.models import Comment
# from apps.comment.serializers import CommentSerializer
# from utils.ResponseMessage import CommentResponse
# from utils.JWTAuth import JWTHeaderQueryParamAuthentication
#
# class CommentGenericAPIView(
#     # ViewSetMixin, # 实现路由分发， 可以在一个类视图里面实现多个方法
#     # GenericAPIView,
#     # RetrieveModelMixin,
#     # CreateModelMixin,
#     # UpdateModelMixin,
#     # DestroyModelMixin,
#     # ListModelMixin
#
#     # 通过查看 rest_framework.viewsets 的源码得知，viewsets 的继承树
#     # 所以直接使用 ModelViewSet，可以包含上面的所有方法
#     ModelViewSet
# ):
#     queryset = Comment.objects
#     serializer_class = CommentSerializer
#     authentication_classes = [JWTHeaderQueryParamAuthentication]
#
#     def getOne(self, request, pk):
#         return self.retrieve(request, pk=pk)
#
#     def getAll(self, request):
#         return self.list(request)
#
#     def add(self, request):
#         return self.create(request)
#
#     def deleteOne(self, request, pk):
#         return self.destroy(request, pk=pk)
#
#     # 方法名不能与self中的调用的方法名相同，不然会重写父类的方法
#     def updateOne(self, request, pk):
#         return self.update(request, pk=pk)
#
#     def getCommentCountData(self, request):
#         sku_id = request.GET.get("sku_id")
#         comment_count = Comment.objects.filter(sku_id=sku_id).count()
#         return CommentResponse.success(comment_count)
#
#     def getGoodsCommentData(self, request):
#         sku_id = request.GET.get("sku_id")
#         page = request.GET.get("page", 1)
#         page_size = 15
#         page_start = (int(page) - 1) * page_size
#         page_end = int(page) * page_size
#         comment_data = Comment.objects.filter(sku_id=sku_id).all()[page_start:page_end]
#         response_data = CommentSerializer(instance=comment_data, many=True).data
#         # print(response_data)
#         return  CommentResponse.success(response_data)
#


from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from utils.ResponseMessage import CommentResponse
from utils.JWTAuth import JWTHeaderQueryParamAuthentication


# ========== 自定义分页器 ==========
class CommentPagination(PageNumberPagination):
    """评论分页器"""
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


# ========== 标准 CRUD 视图 ==========
class CommentViewSet(viewsets.ModelViewSet):
    """评论的增删改查"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTHeaderQueryParamAuthentication]

    def create(self, request, *args, **kwargs):
        """创建评论"""
        # 添加用户信息
        if request.user.get("status"):
            request.data['email'] = request.user.get("payload").get("email")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CommentResponse.success(serializer.data)

    def list(self, request, *args, **kwargs):
        """获取评论列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 使用自定义分页响应格式
            return CommentResponse.success({
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return CommentResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取单个评论"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CommentResponse.success(serializer.data)

    def update(self, request, *args, **kwargs):
        """更新评论"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CommentResponse.success(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除评论"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return CommentResponse.success("删除成功")


# ========== 自定义业务视图 ==========

class CommentCountView(APIView):
    """获取商品评论数量"""

    def get(self, request):
        sku_id = request.query_params.get('sku_id')

        if not sku_id:
            return CommentResponse.failed("缺少 sku_id 参数")

        comment_count = Comment.objects.filter(sku_id=sku_id).count()
        return CommentResponse.success(comment_count)


class CommentListView(generics.ListAPIView):
    """获取商品评论列表（带分页）"""
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        sku_id = self.request.query_params.get('sku_id')

        if not sku_id:
            return Comment.objects.none()

        return Comment.objects.filter(sku_id=sku_id).order_by('-create_time')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 使用自定义分页响应格式
            return CommentResponse.success({
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return CommentResponse.success(serializer.data)