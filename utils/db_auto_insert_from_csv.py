import csv

from songbook.constants import VOCALOID_GROUP
from songbook.models import (
    Song,
    SongGroup,
)


def get_csv_data(file_name: str):
    """csv 파일을 읽고 리스트로 묶어준다.

    :param file_name: 입력받을 파일 명 (경로 포함되기도 한다.)
    :return:
        (list): csv 파일에 담겨있는 정보가 Wrapping된 리스트
    """
    csvfile = open(file_name, 'r', encoding='utf-8-sig')
    reader = csv.reader(csvfile)

    csv_data_list = []
    for row in reader:
        csv_data_list.append(row)

    csvfile.close()
    return csv_data_list


def remove_hidden_mark(song_number: str):
    """ 기기에 대한 정보가 담긴 마크를 제거하고 정수로 변환해준다.

    :param song_number: 노래 번호
    :return:노래 번호
    """

    # 미수록곡 early exit
    if (song_number is None) or (song_number == ''):
        return None

    if song_number[-1] in 'ⓗⓢⓕⓛ':
        return song_number[:-1]
    else:
        return song_number


def xxx_filter(song_number: str):
    # 나무위키에서 수록되지 않은 곡의 경우 XXX로 표시한다.
    return None if song_number == 'XXX' else song_number


def origin_song_name_validation(origin: str, korean: str):
    """원어 제목의 괄호를 삭제하고 원어제목이 비어있는 경우 (숫자 또는 영어)
    한국어 제목을 넣어준다.

    :param origin: 원어 제목
    :param korean: 한국어 제목
    :return: 원어 제목
    """
    if origin == '':
        return korean

    result = origin.replace('(', '')
    return result.replace(')', '')


def korean_song_name_validation(korean: str, origin: str):
    """영어여서 한국어로 비어있는 곡 제목을 수정한다.

    :param korean: 한국어 제목
    :param origin: 원어 제목
    :return: 한국어 제목
    """
    if korean == '':
        return origin

    return korean


def two_line_validater(csv_file_name: str, contry: str):
    """

    :param csv_file_name: 파일 이름
    :param contry: 국가
    :return: 없음

    로직 메모
    ====================
    1. 복사한다.
    2. 다음 줄을 읽는다.
    3-1. 다음 줄의 1번째 칸이 빈줄이 아닐 경우
        - 빈줄을 추가한다.
        - 이전줄의 곡 제목을 복사한다.
    3-2. 다음 줄의 1번째 칸이 비어있다.
        - 다음을 넘어간다.
    4. 사용 보컬로이드 항목을 삭제한다.
    5-1. 한국 데이터의 경우 TJ, KY, 곡 제목, 작곡가,
                              ,   , 일본제목,       ,
    5-2. 일본 데이터의 경우 DAM, UGA, JOYS, 곡 제목,        ,
                               ,    ,     , 한국제목, 작곡가,
    5. 위에 맞게 수정하고 입력
    ===================

    """

    # 결과로 출력할 파일 생성
    result_csv_file = open('result.csv', 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(result_csv_file)

    # 가져오려는 파일의 정보를 리스트로 가져옴
    csv_data_list = get_csv_data(csv_file_name)
    last_index = len(csv_data_list)

    # 데이터 형식 맞추기
    column_count = 4 if contry == 'KOR' else 5

    for index in range(0, last_index):
        current_row = csv_data_list[index]
        # 첫 칸이 비어있을 경우 다음 차례로
        if not bool(current_row[0]):
            continue

        next_index = index + 1
        if next_index < last_index:
            next_row = csv_data_list[next_index]
        else:
            next_row = ['a' for _ in range(column_count)]

        # 다음 줄이 빈 줄이 아닌 경우
        if bool(next_row[0]):
            next_row = ['' for _ in range(column_count)]
            title_index = 3 if contry == 'KOR' else 4

            # 영어 제목을 그대로 복사한다.
            next_row[title_index] = current_row[title_index]

        # 파일에 입력한다.
        result_row = current_row + next_row
        writer.writerow(result_row)

    result_csv_file.close()


def create_bulk_list(csv_file_name: str, contry: str):
    """지정된 형식에 맞게 들어온 데이터를 가공한다.

        한국 데이터의 경우 TJ, KY, 곡 제목, 작곡가,
                             ,   , 일본제목,       ,
        일본 데이터의 경우 DAM, UGA, JOYS, 곡 제목,        ,
                              ,    ,     , 한국제목, 작곡가,


        다음과 같은 형식으로 변경한다.
        {
            'tj':
            'ky':
            'dam':
            'uga':
            'joy':
            'song_name_origin':
            'song_name_korean':
            'singer':
            'group':
            'lyrics':
        }

        :param csvfile:
        :return:
    """

    VOCALOID_GROUP_FOREIGN_KEY = SongGroup.objects.get(group_name=VOCALOID_GROUP)

    csv_data_list = get_csv_data(csv_file_name)
    bulk_list = []
    for row in csv_data_list:
        if contry == 'KOR':
            field_dict = {
                'tj': remove_hidden_mark(xxx_filter(row[0])),
                'ky': remove_hidden_mark(xxx_filter(row[1])),
                'song_name_origin': origin_song_name_validation(row[6], row[2]),
                'song_name_korean': row[2],
                'singer': row[3],
                'group': VOCALOID_GROUP_FOREIGN_KEY,
                'lyrics': None,
            }
        else:
            field_dict = {
                'dam': remove_hidden_mark(xxx_filter(row[0])),
                'uga': remove_hidden_mark(xxx_filter(row[1])),
                'joy': remove_hidden_mark(xxx_filter(row[2])),
                'song_name_origin': row[3],
                'song_name_korean': korean_song_name_validation(row[8], row[3]),
                'singer': row[9],
                'group': VOCALOID_GROUP_FOREIGN_KEY,
                'lyrics': None,
            }
        bulk_list.append(field_dict)

    return bulk_list


def classify_exist_song(bulk_list):
    exist = []
    non_exist = []

    exist_song_name_list = [song.song_name_korean for song in Song.objects.all()]

    for bulk_data_dict in bulk_list:
        if bulk_data_dict['song_name_korean'] in exist_song_name_list:
            exist.append(bulk_data_dict)
        else:
            non_exist.append(bulk_data_dict)

    return {'for_create': non_exist, 'for_update': exist}


def auto_inserter_from_csv(csv_file_name: str, contry: str):
    bulk_list_for_create = []

    non_classified_bulk_list = create_bulk_list(csv_file_name, contry)

    classified_bulk_data_dict = classify_exist_song(non_classified_bulk_list)

    for field_data_dict in classified_bulk_data_dict['for_create']:
        bulk_list_for_create.append(Song(**field_data_dict))
    Song.objects.bulk_create(bulk_list_for_create, ignore_conflicts=True)

    for field_data_dict in classified_bulk_data_dict['for_update']:
        song_name_korean = field_data_dict['song_name_korean']
        Song.objects.filter(song_name_korean=song_name_korean).update(**field_data_dict)
