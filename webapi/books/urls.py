from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
import views


urlpatterns = [

    url(r'^$', views.web_api_root),

    url(r'^books/$', views.BookList.as_view(), name='book-list'),
    url(r'^books/(?P<pk>[0-9]+)/$', views.BookDetail.as_view(), name='book-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    url(r'^books/(?P<pk>[0-9]+)/highlight/$', views.BookHighlight.as_view(), name='book-highlight'),

    # Login and logout views for the browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)