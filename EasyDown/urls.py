from django.contrib import admin
from django.urls import path,include
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register,name = 'register'),
    path('login/', views.login, name='login'),
    path('blog/',include('blog.urls')),
    path('home/', views.home_unlog,name="home_unlog"),
    path('home/unlog',views.log_out,name="log_out"),
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]