# Generated by Django 4.0.4 on 2022-05-27 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_user_address2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bans',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_banned',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_developer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_moderator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_owner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_reseller',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='products',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='zipcode',
        ),
    ]