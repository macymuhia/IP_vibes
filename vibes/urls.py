from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("login/profile/",
         views.profile, name="profile"),
    path('login/profile/edit/',
         views.edit_profile, name='edit_profile'),
    path('account_activation_sent/', views.account_activation_sent,
         name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
