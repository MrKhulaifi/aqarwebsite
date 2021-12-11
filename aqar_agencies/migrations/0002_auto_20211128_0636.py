# Generated by Django 3.2.7 on 2021-11-28 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aqar_agencies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='agency',
            name='verification',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aqar_agencies.area'),
        ),
    ]
