# Generated by Django 3.1.2 on 2020-10-24 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlRedirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_original', models.URLField(verbose_name='Исходный URL')),
                ('url_new', models.SlugField(blank=True, unique=True, verbose_name='Короткий URL')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Правило редиректа',
                'verbose_name_plural': 'Правила редиректа',
                'ordering': ('user', '-pk'),
            },
        ),
    ]
