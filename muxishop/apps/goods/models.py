# -*- coding: utf-8 -*-
import decimal
import json
from django.db import models
from muxishop.settings import IMAGE_URL

class Goods(models.Model):
    type_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sku_id = models.CharField(max_length=255, blank=True, null=True)
    target_url = models.CharField(max_length=255, blank=True, null=True)
    jd_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    spu_id = models.CharField(max_length=255, blank=True, null=True)
    mk_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vender_id = models.IntegerField(blank=True, null=True)
    find = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        result = {
            'type_id': self.type_id,
            'name': self.name,
            'sku_id': self.sku_id,
            'target_url': self.target_url,
            'jd_price': self.jd_price,
            'p_price': self.p_price,
            'image': IMAGE_URL + self.image,
            'shop_name': self.shop_name,
            'shop_id': self.shop_id,
            'spu_id': self.spu_id,
            'mk_price': self.mk_price,
            'vender_id': self.vender_id,
            'find': self.find
        }
        return json.dumps(result, cls=DecimalEncoder, ensure_ascii=False)

    class Meta:
        db_table = 'goods'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)