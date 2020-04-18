import csv


def get_csv_data(file_name: str):
    """csv 파일을 읽고 리스트로 묶어준다.

    :param file_name: 입력받을 파일 명 (경로 포함되기도 한다.)
    :return:
        (list): csv 파일에 담겨있는 정보가 Wrapping된 리스트
    """
    csvfile = open(f'{file_name}', 'r', encoding='utf-8')
    reader = csv.reader(csvfile)

    csv_data_list = []
    for row in reader:
        csv_data_list.append(row)

    csvfile.close()
    return csv_data_list


def remove_hidden_mark(song_number: str) -> int:
    """ 기기에 대한 정보가 담긴 마크를 제거하고 정수로 변환해준다.

    :param song_number: 노래 번호
    :return:
        (int): 노래 번호
    """
    song_number_str = str(song_number)
    if song_number_str[-1] in 'ⓗⓢⓕⓛ':
        return int(song_number_str[:-1])
    else:
        return int(song_number_str)


def xxx_filter(song_number: str) -> str:
    # 나무위키에서 수록되지 않은 곡의 경우 XXX로 표시한다.
    return song_number if song_number != 'XXX' else ''


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
    result_csv_file = open('result.csv', 'w', encoding='utf-8', newline='')
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
        next_row = csv_data_list[next_index]

        # 다음 줄이 빈 줄이 아닌 경우
        if bool(next_row[0]):
            next_row = ['' for _ in range(column_count)]
            title_index = 3 if contry == 'KOR' else 4

            # 영어 제목을 그대로 복사한다.
            next_row[title_index] = current_row[title_index]

        # 파일에 입력한다.
        writer.writerow(current_row)
        writer.writerow(next_row)

    result_csv_file.close()


def auto_inserter_from_csv(csvfile: str):
    pass