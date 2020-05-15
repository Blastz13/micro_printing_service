# Generated by Django 3.0.2 on 2020-05-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20200510_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Коментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Количество заказанных'),
        ),
    ]
