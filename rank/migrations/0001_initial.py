# Generated by Django 3.0 on 2019-12-18 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved_num', models.IntegerField()),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('user_url', models.CharField(max_length=100, verbose_name='/')),
            ],
        ),
    ]
