from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from django.urls import path
from django.contrib.auth.views import *
from django.urls import reverse_lazy
from django.core.mail import EmailMessage

from .views import index, by_rubric, add_rub, add_and_save, BbDetailView, BbEditView, CarEditView, BbDeleteView, \
    profile_view, \
    by_logged_user, update_profile, profile_ads_view, user_reg, search_ads, BbCreateView, CarDetailView, \
    add_car_by_brand

urlpatterns = [
    path('add/', add_rub, name='add'),
    path('add_<int:rubric_id>/', add_and_save, name='add_by_rub'),
    path('add_<int:rubric_id>_<int:carbrand_id>/', add_car_by_brand, name='add_car_by_brand'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail_car/<int:pk>/', CarDetailView.as_view(), name='detail_car'),
    path('car_edit/<int:pk>/', CarEditView.as_view(), name='car_edit'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/uinfo/', profile_ads_view, name='profile_ads_view'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('search/', search_ads, name='search_ads'),
    path('accounts/registrate/', user_reg, name='user_registrate'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/profile/update/', update_profile, name='update_profile'),
    path('accounts/profile/ads/', by_logged_user, name='by_logged_user'),
    path('accounts/password_change/',  # смена пароля
         PasswordChangeView.as_view(
             template_name='registration/change_password.html'),
         name='password_change'),
    path('accounts/password_change/done/',  # уведомление об успешной смене пароля
         PasswordChangeDoneView.as_view(
             template_name='registration/password_changed.html'),
         name='password_change_done'),
    path('accounts/password_reset/',  # отправка пиьсма для сброса пароля
         PasswordResetView.as_view(
             template_name='registration/reset_password.html',
             subject_template_name='registration/reset_subject.txt',
             email_template_name='registration/reset_email.txt'),
         name='password_reset'),
    path('accounts/password_reset/done/',  # уведомление об отправке письма для сброса паролдя
         PasswordResetDoneView.as_view(
             template_name='registration/email_sent.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',  # сброс пароля
         PasswordResetConfirmView.as_view(
             template_name='registration/confirm_password.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',  # уведомление об успешном сбросе пароля
         PasswordResetCompleteView.as_view(
             template_name='registration/password_confirmed.html'),
         name='password_reset_complete'),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
