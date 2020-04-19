from django.http import JsonResponse
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
)


from .models import Song

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


def test(request):
    return render(request, 'main.html', context={'selected_menu': 1})


class MainView(TemplateView):
    template_name = 'main.html'


class HowtoView(TemplateView):
    template_name = ''


class SearchView(ListView):
    model = Song
    paginate_by = 20
    template_name = 'search.html'


def song_detail_view(request, pk):
    song = Song.objects.get(pk=pk)

    json_dict = {
        "song_name_origin": song.song_name_origin,
        "song_name_korean": song.song_name_korean,
        "singer": song.singer,
        "group": song.group.group_name,
        "tj": song.tj,
        "ky": song.ky,
        "dam": song.dam,
        "uga": song.uga,
        "joy": song.joy,
    }

    return JsonResponse(json_dict)






