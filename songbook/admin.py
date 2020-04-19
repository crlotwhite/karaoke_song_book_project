from django.contrib import admin
from .models import (
    Song,
    SongGroup,
)


# Register your models here.
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    list_display = [
        'song_name_korean', 'singer', 'group',
    ]


@admin.register(SongGroup)
class SongGroupAdmin(admin.ModelAdmin):
    list_display = [
        'group_name'
    ]
