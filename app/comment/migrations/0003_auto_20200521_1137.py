# Generated by Django 2.2.9 on 2020-05-21 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20200507_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='root_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replys', to='comment.Comment'),
        ),
    ]