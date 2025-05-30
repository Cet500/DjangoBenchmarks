# Generated by Django 5.2 on 2025-04-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.CharField(max_length=100, verbose_name='ID теста')),
                ('test_name', models.CharField(max_length=100, verbose_name='Название')),
                ('parameters', models.CharField(max_length=200, verbose_name='Параметры')),
                ('execution_time', models.FloatField(verbose_name='Время выполнения')),
                ('python_version', models.CharField(max_length=50, verbose_name='Версия Python')),
                ('django_version', models.CharField(max_length=50, verbose_name='Версия Django')),
                ('os', models.CharField(max_length=100, verbose_name='OS')),
                ('cpu', models.CharField(max_length=150, verbose_name='CPU')),
                ('memory', models.IntegerField(verbose_name='RAM')),
                ('gpu', models.CharField(max_length=150, verbose_name='GPU')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
