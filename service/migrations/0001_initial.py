# Generated by Django 3.0.6 on 2020-05-09 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('tel', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('size', models.CharField(max_length=128, verbose_name='Размер и тип бумаги')),
                ('date_order', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Общая стоимость')),
                ('accept_conditions', models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')),
                ('is_payed', models.BooleanField(default=False, verbose_name='Оплачено')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date_order'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(upload_to='photos/%d/%m/%Y', verbose_name='Фотография')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='service.Order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]