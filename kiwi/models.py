from django.db import models

# Create your models here.
class FileInfo(models.Model):
    #FIXME: find out  more specific max-length
    #for CharField, max_legnth is required
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=500)
    size = models.IntegerField(default=0)
    icon = models.CharField(max_length=500)
    source = models.CharField(max_length=50)
    lastEditTime = models.DateTimeField('last edit time')
    #thumbnail = models.CharField(max_length=500)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name