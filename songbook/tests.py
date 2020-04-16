from django.test import TestCase

from .models import Song


# Create your tests here.
class TestSong(TestCase):
    def setUp(self) -> None:
        # Song.objects.create()
        pass

    def test_is_vocaloid(self):
        # 애니송과 보카로를 잘 구별하는가.
        pass
