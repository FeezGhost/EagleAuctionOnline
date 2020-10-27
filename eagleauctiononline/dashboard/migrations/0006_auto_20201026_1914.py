# Generated by Django 3.1.2 on 2020-10-26 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_customer_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='bids',
        ),
        migrations.AddField(
            model_name='auction',
            name='bids',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.bids'),
        ),
    ]
