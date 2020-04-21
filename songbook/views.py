from django import forms

from django.db.models import Q
from django.http import (
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
)
from django.urls import reverse
from django.shortcuts import (
    render,
)
from django.views.generic import (
    ListView,
    TemplateView,
)

from .models import (
    Song,
    SongGroup,
    AlbumArtImage,
)

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

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context.update({'selected_menu': 1})
        return context


class HowtoView(TemplateView):
    template_name = ''


class SearchView(ListView):
    model = Song
    paginate_by = 20
    template_name = 'search.html'
    object_list = Song.objects.order_by('pk').all()

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({'selected_menu': 2})
        return context

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        query_string = request.GET.get('query')
        if category and query_string:
            if category == 'title':
                filtered_song_list = Song.objects.filter(
                    Q(song_name_origin__contains=query_string) | Q(song_name_korean__contains=query_string)
                ).all()
            elif category == 'singer':
                filtered_song_list = Song.objects.filter(singer__contains=query_string).all()
            elif category == 'group':
                filtered_song_group_name = SongGroup.objects.filter(group_name__contains=query_string).all()
                filtered_song_list = Song.objects.filter(group__in=filtered_song_group_name).all()
            else:
                filtered_song_group_name = SongGroup.objects.filter(group_name__contains=query_string).all()
                filtered_song_list = Song.objects.filter(
                    Q(song_name_origin__contains=query_string)
                    | Q(song_name_korean__contains=query_string)
                    | Q(singer__contains=query_string)
                    | Q(group__in=filtered_song_group_name)
                ).all()

            self.object_list = filtered_song_list

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


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
    song.view_count = song.view_count + 1
    song.save()

    return JsonResponse(json_dict)


class AlbumArtUploadModelForm(forms.ModelForm):
    class Meta:
        model = AlbumArtImage
        fields = ['name', 'image', ]


def update_album_art_view(request):
    """Form으로 입력한 이미지를 일괄 저장 한다.
    저장 완료후 Song 어드민으로 이동한다.
    """
    if request.method == 'POST':
        form = AlbumArtUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            song_list = request.POST.get('song_list').split(' ')
            for song_pk in song_list:
                try:
                    song_pk_int = int(song_pk)
                except ValueError:
                    continue

                song = Song.objects.get(pk=song_pk_int)
                song.album_art = form.instance
                song.save()

            return HttpResponseRedirect(reverse('admin:songbook_song_changelist'))
    return HttpResponseForbidden('allowed only via POST')

