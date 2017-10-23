from django.db import models

# Create your models here.

from scripts.models import Script

class Log(models.Model):
    script = models.ForeignKey(Script)
    run_time = models.DateTimeField(auto_now_add=True)
    comp = models.BooleanField()
    def __str__(self):
        return str(self.script.uni_id) + ': ' + str(self.comp)
