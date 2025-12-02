from django.db import models


class Comment(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    sku_id = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    user_image_url = models.CharField(max_length=255, blank=True, null=True)
    reference_name = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    reply_count = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'