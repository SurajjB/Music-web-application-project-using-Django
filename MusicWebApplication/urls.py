from django.conf import settings
from MusicWebApplication import views
from django.contrib import admin
from django.urls import path,  include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#Django Admin site customization
admin.site.site_title = "Music Web Application Admin"
admin.site.site_header = "Music Web Application Data Management"
admin.site.index_title = "Welcome to Music Web Application Data Management"

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('changePassword/<token>/', views.changePassword, name='changePassword'),
    path('home', views.home, name='home'),
    path('search', views.search, name='search'),
    path('aboutSong/<str:slug>', views.aboutSong, name='aboutSong'),
    path('addASongToMusicApp', views.addASongToMusicApp, name='addASongToMusicApp'),
    path('contact', views.contact, name='contact')
]

#To add url paths for media files in templates.
#if settings.DEBUG:
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
