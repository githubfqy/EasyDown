from django.urls import path,include
from blog import  views

app_name = 'blog'
urlpatterns =[
    path('login/',views.login,name = 'login'),
    path('reset/',views.reset_password,name = 'reset'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('category/<int:id>',views.category,name='category'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:id>/', views.tag_detail, name='tags_detail'),
    #path('articles/<int:id>/comments/', views.comment, name='comments'),
    path('info/', views.user_info, name='user_info'),
    path('info/<comment_id>',views.comment_del,name="comm_del"),
    path('forget/',views.forget_password,name="forget_pass"),
    path('forget/reset/',views.forget_set,name="forget_set"),
    path('app/',views.app,name = 'app'),
    path('contact/',views.contact,name ='contact'),
    path('search/',views.search,name='search'),
]