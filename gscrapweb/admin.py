from django.contrib import admin
from models import Track
# Register your models here..


class TracksAdmin(admin.ModelAdmin):
      list_display    = ['track_type','thumbnail', 'author', 'author_link', 'link','title','user_id']

admin.site.register(Track, TracksAdmin)
