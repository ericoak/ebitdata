from django.db import models

# Create your models here.

class Script(models.Model):
    uni_id = models.CharField(max_length=6, unique=True, primary_key=True)
    name = models.TextField()
    desc = models.TextField()
    last_run = models.DateTimeField(auto_now=True)
    last_run_comp = models.BooleanField(default=False)
    def __str__(self):
        return self.uni_id + " - " + self.name
