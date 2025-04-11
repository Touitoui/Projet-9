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
import ticket.views
import review.views
import user.views

urlpatterns = [
    path('', ticket.views.home),
    path('login/', user.views.login_page, name='login'),
    path('logout/', user.views.logout_user, name='logout'),
    path('signup', user.views.signup_page, name='signup'),
    path('admin/', admin.site.urls),
    path('ticket/create/', ticket.views.ticket_upload, name='create_ticket'),
    path('ticket/<int:id>/update/', ticket.views.ticket_update, name='update_ticket'),
    path('ticket/<int:id>/delete/', ticket.views.ticket_delete, name='delete_ticket'),
    path('review/add/', review.views.review_upload, name='create_review'),
    path('review/<int:id>/update/', review.views.review_update, name='update_review'),
    path('review/<int:id>/delete/', review.views.review_delete, name='delete_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
