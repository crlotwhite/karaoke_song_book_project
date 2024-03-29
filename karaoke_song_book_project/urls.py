"""karaoke_song_book_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from karaoke_song_book_project import settings
from songbook.views import (
    MainView,
    SearchView,
    song_detail_view,
    update_album_art_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main_page'),
    path('search/', SearchView.as_view(), name='search_page'),
    path('song/<int:pk>/', song_detail_view, name='detail_page'),
    path('updatealbumart/', update_album_art_view, name='update_album_art'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
