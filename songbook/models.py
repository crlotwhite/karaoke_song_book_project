from django.db import models

"""
기본 스키마

Song
ID | Song_Name_Origin | Song_Name_Kor | Singer/Producer | Group (Anime Name or Vocaloid) | TJ | KY | DAM | UGA | JOYS

SongGroup
ID | Group_Name

"""


class SongGroup(models.Model):
    group_name = models.CharField(max_length=100, help_text='그룹 이름 (애니메이션 제목/보컬로이드)')


class Song(models.Model):
    song_name_origin = models.CharField(max_length=100, help_text='노래 제목 (일본어)')
    song_name_korean = models.CharField(max_length=100, help_text='노래 제목 (한국어)')
    singer = models.CharField(max_length=20, help_text='가수(프로듀서)')
    group = models.ForeignKey(SongGroup, help_text='그룹 (애니메이션 제목/보컬로이드)')
    tj = models.IntegerField(help_text='TJ 노래방 번호')
    ky = models.IntegerField(help_text='KY 노래방 번호')
    dam = models.IntegerField(help_text='DAM 노래방 번호')
    uga = models.IntegerField(help_text='UGA 노래방 번호')
    joy = models. IntegerField(help_text='Joy Sounds 노래방 번호')
