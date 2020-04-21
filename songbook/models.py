from django.db import models

from .constants import VOCALOID_GROUP

"""
기본 스키마

Song
ID | Song_Name_Origin | Song_Name_Kor | Singer/Producer | Group (Anime Name or Vocaloid) | TJ | KY | DAM | UGA | JOYS

SongGroup
ID | Group_Name

"""


class SongGroup(models.Model):
    group_name = models.CharField(max_length=100, help_text='그룹 이름 (애니메이션 제목/보컬로이드)')

    def __str__(self):
        return self.group_name


class AlbumArtImage(models.Model):
    name = models.CharField(max_length=100, help_text='앨범 아트 이름')
    image = models.ImageField(help_text='앨범아트 이미지 파일', null=True, upload_to='img/album_arts')

    def __str__(self):
        return self.name


class Song(models.Model):
    song_name_origin = models.CharField(max_length=100, help_text='노래 제목 (일본어)')
    song_name_korean = models.CharField(max_length=100, help_text='노래 제목 (한국어)')
    singer = models.CharField(max_length=20, help_text='가수(프로듀서)')
    group = models.ForeignKey(SongGroup, help_text='그룹 (애니메이션 제목/보컬로이드)', on_delete=models.CASCADE)
    tj = models.CharField(max_length=8, help_text='TJ 노래방 번호', null=True)
    ky = models.CharField(max_length=8, help_text='KY 노래방 번호', null=True)
    dam = models.CharField(max_length=8, help_text='DAM 노래방 번호', null=True)
    uga = models.CharField(max_length=8, help_text='UGA 노래방 번호', null=True)
    joy = models.CharField(max_length=8, help_text='Joy Sounds 노래방 번호', null=True)
    lyrics = models.TextField(help_text='가사', null=True)
    album_art = models.ForeignKey(AlbumArtImage, help_text='앨범아트', on_delete=models.CASCADE, null=True)
    view_count = models.IntegerField(help_text='검색 횟수', default=0)

    def __str__(self):
        return self.song_name_korean


class VocaloidSongManager(models.Manager):
    def get_queryset(self):
        return super(VocaloidSongManager, self).get_queryset().filter(
            group=SongGroup.objects.get(group_name=VOCALOID_GROUP)
        )


class VocaloidSong(Song):
    object = VocaloidSongManager()

    class Meta:
        proxy = True
