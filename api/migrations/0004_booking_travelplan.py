# Generated by Django 5.0.1 on 2024-01-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.IntegerField(primary_key=True, serialize=False)),
                ('booking_price', models.IntegerField()),
                ('member_count', models.IntegerField()),
            ],
            options={
                'db_table': 'booking',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TravelPlan',
            fields=[
                ('travel_id', models.IntegerField(primary_key=True, serialize=False)),
                ('destination', models.CharField(max_length=255)),
                ('rate', models.IntegerField()),
                ('start_date', models.CharField(max_length=255)),
                ('about', models.TextField()),
            ],
            options={
                'db_table': 'travel_plan',
                'managed': False,
            },
        ),
    ]
