from rest_framework import serializers
from apps.comment import models


class CommentSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(required=False, format='%Y-%m-%d %X')
    class Meta:
        model = models.Comment
        fields = "__all__"
