# Generated by Django 5.0.1 on 2024-01-24 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined')], max_length=10)),
                ('party_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.party')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]
