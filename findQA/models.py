from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2, primary_key=True)

    class Meta:
        ordering = ('name',)


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    class Meta:
        ordering = ('device_id',)


class Tester(models.Model):
    tester_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country, db_column='country_code', on_delete=models.PROTECT)

    class Meta:
        ordering = ('tester_id',)


class Bug(models.Model):
    bug_id = models.AutoField(primary_key=True)
    tester = models.ForeignKey(Tester, db_column='tester_id', on_delete=models.PROTECT)
    device = models.ForeignKey(Device, db_column='device_id', on_delete=models.PROTECT)

    class Meta:
        ordering = ('bug_id',)


class Tester_Device(models.Model):
    tester = models.ForeignKey(Tester, db_column='tester_id', on_delete=models.PROTECT)
    device = models.ForeignKey(Device, db_column='device_id', on_delete=models.PROTECT)

    class Meta:
        ordering = ('tester', 'device')

