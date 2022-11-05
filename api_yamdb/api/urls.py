from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'


router_v1 = routers.DefaultRouter()
router_v1.register('users', views.UsersViewSet, basename='users')
router_v1.register(
    'categories', views.CategoriesViewSet, basename='categories'
)
router_v1.register('genres', views.GenresViewSet, basename='genres')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

v1_auth = [
    path('signup/', views.sign_up, name='signup'),
    path('token/', views.obtain_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(v1_auth)),
]
