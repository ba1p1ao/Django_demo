from django.db import models


class Software(models.Model):
    name = models.CharField(max_length=255, verbose_name="软件名称")
    version = models.CharField(max_length=50, verbose_name="版本号")
    website = models.CharField(max_length=500, verbose_name="官方网站")

    # upload_to 用于设置保存上传文件的存储子路径，跟着 settings.py 中存储上传文件配置项 MEDIA_ROOT 的后部分路径
    # ImageField 是 FileField 的子类，FileField 内部实现了基于日期时间格式生成目录的功能，所以支持使用%日期符号来自动创建目录的。
    # 而且，当同一目录下文件同名了，FileField会自动把后面重复的文件名追加补充随机字符串防止重名。
    picture = models.ImageField(upload_to="picture/%Y/%m/%d/", verbose_name="缩略图")
    downloads = models.FileField(max_length=255, upload_to="soft/%Y/%m/%d/", verbose_name="下载地址")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_software"
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}--{self.version}"


