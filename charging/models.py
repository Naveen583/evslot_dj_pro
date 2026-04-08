from django.db import models

class EVAdmin(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'ev_admin'
        managed = True


class EVRegister(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=40)
    account = models.CharField(max_length=20)
    card = models.CharField(max_length=20)
    bank = models.CharField(max_length=20)
    amount = models.FloatField(default=10000)
    uname = models.CharField(max_length=20, primary_key=True)
    passw = models.CharField(max_length=128)
    latitude = models.CharField(max_length=20, blank=True)
    longitude = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'ev_register'
        managed = True


class EVStation(models.Model):
    name = models.CharField(max_length=20)
    stype = models.CharField(max_length=20)
    numcharger = models.IntegerField(default=0)
    area = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    lat = models.CharField(max_length=20)
    lon = models.CharField(max_length=20)
    uname = models.CharField(max_length=20, primary_key=True)
    passw = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    landmark = models.CharField(max_length=30)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=40)
    distance = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'ev_station'
        managed = True


class EVBooking(models.Model):
    uname = models.ForeignKey(EVRegister, on_delete=models.CASCADE, db_column='uname',to_field='uname')
    station = models.ForeignKey(EVStation, on_delete=models.CASCADE, db_column='station', to_field='uname')
    carno = models.CharField(max_length=20)
    reserve = models.CharField(max_length=20)
    slot = models.IntegerField()
    cimage = models.CharField(max_length=20)
    mins = models.IntegerField(default=0)
    plan = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rtime = models.CharField(max_length=20)
    etime = models.CharField(max_length=20)
    rdate = models.CharField(max_length=15)
    edate = models.CharField(max_length=15)
    otp = models.CharField(max_length=10)
    charge = models.FloatField(default=0.0)
    chargetime = models.IntegerField(default=0)
    chargemin = models.IntegerField(default=0)
    chargesec = models.IntegerField(default=0)
    chargest = models.IntegerField(default=0)
    paymode = models.CharField(max_length=20)
    payst = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    btime1 = models.CharField(max_length=20)
    btime2 = models.CharField(max_length=20)
    alertst = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(default=0)
    end_time = models.DateTimeField(null=True, blank=True)
    smsst = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'ev_booking'
        managed = True
