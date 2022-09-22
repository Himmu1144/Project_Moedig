from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
 

urlpatterns = [
    path('',views.home,name='home'),
    path('order/',views.order,name='order'),
    path('pricing/',views.pricing,name='pricing'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('loginSignup/',views.loginSignup,name='loginSignup'),
    path('logout/',views.handleLogout,name='handleLogout'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('upload/',views.upload,name='upload'),
    path('delete/<slug>',views.delete,name='delete'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.success,name='success'),
    path('employee/',views.employee,name='employee'),
    path('employeeDashboard',views.employeeDashboard,name='employeeDashboard'),
    path('employeeDashboard/<id>',views.employeeview,name='employeeview'),
    path('adminDashboard/',views.adminDashboard,name='adminDashboard'),
    path('adminDashboard/<id>',views.adminview,name='adminview'),
    path('password_reset_request/',views.password_reset_request,name='password_reset'),

    # Built In Urls
    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name='web_moedig/password_reset/password_reset_view.html'),name='password_reset'),
    path('reset_password_done/',auth_views.PasswordResetDoneView.as_view(template_name='web_moedig/password_reset/password_reset_done.html') , name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='web_moedig/password_reset/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='web_moedig/password_reset/password_reset_complete.html'),name="password_reset_complete"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)