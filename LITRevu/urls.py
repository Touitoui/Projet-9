"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import app.views
import user.views

urlpatterns = [
    path('', app.views.home),
    path('posts/', app.views.my_posts, name='posts'),
    path('login/', user.views.login_page, name='login'),
    path('logout/', user.views.logout_user, name='logout'),
    path('signup', user.views.signup_page, name='signup'),
    path('admin/', admin.site.urls),
    path('ticket/create/', app.views.ticket_upload, name='create_ticket'),
    path('ticket/<int:id>/update/', app.views.ticket_update, name='update_ticket'),
    path('ticket/<int:id>/delete/', app.views.ticket_delete, name='delete_ticket'),
    path('ticket/<int:id>/add_review/', app.views.add_review, name='add_review'),
    path('review/review_upload/', app.views.new_review_upload, name='new_review_upload'),
    path('review/<int:id>/update/', app.views.review_update, name='update_review'),
    path('review/<int:id>/delete/', app.views.review_delete, name='delete_review'),
    path('follow_user/', app.views.follow_user, name='follow_user'),
    path('unfollow_user/<int:id>/', app.views.unfollow_user, name='unfollow_user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
