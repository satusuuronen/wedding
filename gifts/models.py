from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Gift(models.Model):
    title = models.CharField(max_length=200)
    number = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.TimeField(auto_now_add=True)
    date_modified = models.TimeField(auto_now=True) 
    description = models.TextField(blank=True)
    booker = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.title

class GiftAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    '''
    class Media:
        css = {
            "all": ("css/bootstrap.min.css",)
        }
        '''

admin.site.register(Gift, GiftAdmin)

