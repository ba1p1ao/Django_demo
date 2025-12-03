from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSetMixin, ModelViewSet
from rest_framework.mixins import *
from apps.comment import models
from apps.comment.serializers import CommentSerializer


class CommentGenericAPIView(
    # ViewSetMixin, # 实现路由分发， 可以在一个类视图里面实现多个方法
    # GenericAPIView,
    # RetrieveModelMixin,
    # CreateModelMixin,
    # UpdateModelMixin,
    # DestroyModelMixin,
    # ListModelMixin


    # 通过查看 rest_framework.viewsets 的源码得知，viewsets 的继承树
    # 所以直接使用 ModelViewSet，可以包含上面的所有方法
    ModelViewSet
):
    queryset = models.Comment.objects
    serializer_class = CommentSerializer

    def getOne(self, request, pk):
        return self.retrieve(request, pk=pk)

    def getAll(self, request):
        return self.list(request)

    def add(self, request):
        return self.create(request)

    def deleteOne(self, request, pk):
        return self.destroy(request, pk=pk)

    # 方法名不能与self中的调用的方法名相同，不然会重写父类的方法
    def updateOne(self, request, pk):
        return self.update(request, pk=pk)
