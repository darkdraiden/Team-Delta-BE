from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', primary_key=True, max_length=100)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'