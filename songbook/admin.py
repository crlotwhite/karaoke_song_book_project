from django import forms

from django.contrib import admin
from django.template.response import TemplateResponse

from .models import (
    Song,
    SongGroup,
)

from utils.image_manager import delete_no_used_image


# Register your models here.
class SongForm(forms.ModelForm):
    lyrics = forms.CharField(required=False, widget=forms.Textarea)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = SongForm
    list_display = [
        'song_name_korean', 'singer', 'group',
    ]

    search_fields = [
        'song_name_korean', 'singer', 'group__group_name',
    ]

    def remove_unused_images(self, request, queryset):
        delete_no_used_image()
    remove_unused_images.short_description = '사용하지 않는 앨범아트 자동으로 삭제하기'

    def update_album_art_for_songs(self, request, queryset):
        from .views import AlbumArtUploadModelForm
        context = {
            'title': '앨범아트 일괄 업데이트',
            'song_list': queryset,
            'form': AlbumArtUploadModelForm(),
        }
        return TemplateResponse(request, 'admin/album_art_update.html', context)

    update_album_art_for_songs.short_description = '다수의 곡 앨범아트 일괄 업데이트'

    actions = [
        remove_unused_images,
        update_album_art_for_songs,
    ]


@admin.register(SongGroup)
class SongGroupAdmin(admin.ModelAdmin):
    list_display = [
        'group_name'
    ]
