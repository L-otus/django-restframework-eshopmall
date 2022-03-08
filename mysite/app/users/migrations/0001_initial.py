# Generated by Django 2.2.5 on 2021-06-24 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=64, verbose_name='优惠券名')),
                ('coupon_sub', models.CharField(max_length=64, verbose_name='优惠券描述')),
                ('coupon_invalid_time', models.DateField(verbose_name='失效时间')),
                ('coupon_active_time', models.DateField(verbose_name='生效时间')),
                ('coupon_create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('coupon_price', models.FloatField(max_length=64, verbose_name='金额')),
            ],
            options={
                'verbose_name': '03-优惠券',
                'verbose_name_plural': '03-优惠券',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, null=True, verbose_name='用户名')),
                ('wxopenid', models.CharField(default=None, max_length=32, unique=True, verbose_name='微信openid')),
                ('user_json', models.CharField(max_length=32, verbose_name='用户json')),
                ('login_time', models.DateTimeField(auto_now=True, verbose_name='登录时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后一次更新时间')),
                ('activation', models.BooleanField(default=True, verbose_name='激活状态')),
            ],
            options={
                'verbose_name': '01-用户表',
                'verbose_name_plural': '01-用户表',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=None, verbose_name='token_uuid')),
                ('create_time', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('user', models.OneToOneField(on_delete=False, to='users.User', verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '05-用户token',
                'verbose_name_plural': '05-用户token',
            },
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32, verbose_name='市')),
                ('province', models.CharField(max_length=32, verbose_name='省')),
                ('district', models.CharField(max_length=32, verbose_name='区')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '02-地址表',
                'verbose_name_plural': '02-地址表',
            },
        ),
        migrations.CreateModel(
            name='coupon_use',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, '未使用'), (2, '已使用'), (3, '已过期')], verbose_name='优惠券状态')),
                ('obtain_time', models.DateField(verbose_name='获得时间')),
                ('used_time', models.DateField(blank=True, null=True, verbose_name='使用时间')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coupon', verbose_name='优惠券')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='绑定用户')),
            ],
            options={
                'verbose_name': '04-优惠券使用',
                'verbose_name_plural': '04-优惠券使用',
                'unique_together': {('user', 'coupon')},
            },
        ),
    ]