from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    re_path(r'^invoice/(?P<payment_id>[0-9a-f-]+)/$', views.view_invoice, name='view_invoice'),
    path('invoices/', views.view_invoices, name='view_invoices'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'), 
    path('scan_qrcode_camera/', views.scan_qrcode_camera, name='scan_qrcode_camera'), 
    path('profile/', views.profile, name='profile'),  # New profile URL
    # Add more URLs as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
