from django.db import models

# Create your models here.

#Dimension Table
class Week(models.Model):
    week_num = models.IntegerField()
    year = models.IntegerField()
    week_name = models.TextField()
    def __str__(self):
        return self.week_name

#Dimension Table
class Environment(models.Model):
    env = models.TextField()
    service = models.TextField()
    sev = models.IntegerField()
    def __str__(self):
        return self.env + self.service + str(self.sev)

#Dimension Table
class Month(models.Model):
    month_num = models.IntegerField()
    month_name = models.TextField()
    month_code = models.CharField(max_length=3)
    year = models.IntegerField()
    def __str__(self):
        return self.month_name + " " + str(self.year)

#Fact Table
class Uptime_Week(models.Model):
    week_num = models.ForeignKey(Week)
    env = models.ForeignKey(Environment)
    uptime = models.DecimalField(decimal_places=4, max_digits=5)
    duration = models.DecimalField(decimal_places=5, max_digits=12)
    mttr = models.DecimalField(decimal_places=5, max_digits=12)
    count = models.IntegerField()
    def __str__(self):
        return self.env.env + " " + self.week_num.week_name
