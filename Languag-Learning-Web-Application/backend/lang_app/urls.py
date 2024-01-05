"""
URL configuration for lang_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_/Users/tiffanycheng/lang-appapp.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path
from login.views import UserLoginView, UserRegisterView
from lang_chat.views import ChatView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve


#GoogleLogin, UserRedirectView,

urlpatterns = [
    # only these 4 are usable
    path('admin/', admin.site.urls),
    path("login/", UserLoginView.as_view(), name='login'),
    path("register/", UserRegisterView.as_view(), name='register'),
    path("chat/", ChatView.as_view(), name='chat'),
    
    # i'm currently working on this, so that each chat differs by the chat_id in the link
    path('chat/<int:chat_id>/', ChatView.as_view(), name='chat'),
    path("api-auth/", include("rest_framework.urls")),
    path("dj_rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/', include('myapi.urls')),
    re_path(r'^$', serve, kwargs={'path': 'index.html'}),  
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
""" path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("dj-rest-auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"), """