from django.db import models


class Order(models.Model):
    last_name = models.CharField(max_length=128, verbose_name="Фамилия")
    first_name = models.CharField(max_length=128, verbose_name="Имя")
    tel = models.CharField(max_length=12, verbose_name="Номер телефона")
    size = models.CharField(max_length=128, verbose_name="Размер и тип бумаги")
    date_order = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    quantity = models.PositiveIntegerField(verbose_name="Количество заказанных")
    total_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Общая стоимость')
    accept_conditions = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")
    is_payed = models.BooleanField(default=False, verbose_name="Оплачено")

    @property
    def quantity_upload_photos(self):
        return self.photos.all().count()

    def __str__(self):
        return "{} - {}".format(self.last_name, self.date_order)

    class Meta:
        ordering = ['-date_order']
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Photo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='photos', verbose_name='Заказ')
    photos = models.ImageField(upload_to='photos/%d/', verbose_name="Фотография")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
