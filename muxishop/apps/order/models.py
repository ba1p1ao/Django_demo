from django.db import models


class Order(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    trade_no = models.CharField(max_length=155, blank=True, null=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address_id = models.IntegerField(blank=True, null=True)
    pay_status = models.CharField(max_length=155, blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    ali_trade_no = models.CharField(max_length=255, blank=True, null=True)
    is_delete = models.PositiveIntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'order'


class OrderGoods(models.Model):
    trade_no = models.CharField(max_length=255, blank=True, null=True)
    sku_id = models.CharField(max_length=255, blank=True, null=True)
    goods_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'order_goods'