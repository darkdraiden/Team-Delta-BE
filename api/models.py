from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

class TravelPlan(models.Model):
    travel_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rate = models.IntegerField()
    start_date = models.CharField(max_length=255)
    about = models.TextField()

    class Meta:
        managed = False
        db_table = 'travel_plan'

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_price = models.IntegerField()
    travel = models.ForeignKey('TravelPlan', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    member_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'booking'