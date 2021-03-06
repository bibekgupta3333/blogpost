# Generated by Django 3.0.8 on 2020-07-16 14:54

import accounts.models
import accounts.validators
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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=14, null=True, validators=[accounts.validators.validate_phone_number])),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to=accounts.models.image_path)),
                ('profession', models.CharField(blank=True, max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
