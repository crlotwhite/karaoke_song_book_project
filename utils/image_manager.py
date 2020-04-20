import os

from karaoke_song_book_project.settings import MEDIA_ROOT
from songbook.models import Song


def delete_no_used_image():
    """사용되지 않은 이미지를 자동으로 필터링하고 삭제한다.
    """
    path = MEDIA_ROOT + '/img/album_arts/'
    all_img_file_list = os.listdir(path)
    all_song_img_list = Song.objects.all().values_list('album_art', flat=True)
    current_img_file_list = []
    for img_path in all_song_img_list:
        current_img_file_list.append(img_path[img_path.rfind('/')+1:])

    current_img_file_list = list(set(current_img_file_list))

    for img in all_img_file_list:
        if img in current_img_file_list:
            all_img_file_list.remove(img)

    for img in all_img_file_list:
        os.remove('{}{}'.format(path, img))
