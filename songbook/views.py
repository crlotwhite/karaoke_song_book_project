from django.shortcuts import render

# Create your views here.
"""
1. 검색 화면 (/karaoke/search/?query=[검색어]&category=[분류]) GET으로 가져올 예정
    - 제목, 그룹, 가수 중 검색할 내용 선택
    - 검색 결과 아래에 출력
    - 제목 | 가수 | 분류 순으로 결과 리스트 출력
    - 제목 클릭시 상세 페이지 이동
2. 곡 정보 페이지 (/karaoke/song/[노래방번호])
    - 제목 및 다양한 정보를 보여준다.
    - 가사 검색하기를 통해 구글 검색 결과로 바로 이동한다.
    - 앨범아트는 필요할까? 저작권 물어보기
    (크롤링 해올 만한 곳을 찾아보기!!)
"""