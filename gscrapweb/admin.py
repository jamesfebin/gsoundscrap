from django.contrib import admin
from models import Tracks
# Register your models here.


class TracksAdmin(admin.ModelAdmin):
      list_display    = ['type', 'author', 'author_link', 'link','title']

admin.site.register(Tracks, TracksAdmin)
