# Generated by Django 3.2.3 on 2021-05-24 09:50

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
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(auto_now=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=255)),
                ('status', models.CharField(choices=[('CR', 'Create'), ('CF', 'Confirm'), ('PA', 'Packing'), ('SH', 'Shipping'), ('PS', 'Pause'), ('DO', 'Done')], default='CR', max_length=2)),
                ('list_computer', models.JSONField()),
                ('user_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
