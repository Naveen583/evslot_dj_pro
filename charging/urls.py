
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    
    # Admin
    path('login_admin/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    
    # Station Owner
    path('login2/', views.station_login, name='station_login'),
    path('station-forgot-password/', views.station_forgot_password, name='station_forgot_password'),
    path('reg_station/', views.station_register, name='station_register'),
    path('home/', views.station_home, name='station_home'),
    path('view/<str:sid>/', views.station_view_slots, name='station_view'),
    path('start_charge/<str:sid>/<int:rid>/', views.start_charge, name='start_charge'),
    path("finish_charge/<int:rid>/", views.finish_charge, name="finish_charge"),
            path('report/', views.station_report, name='station_report'),
            path('report/pdf/', views.report_pdf, name='report_pdf'),  # PDF download for reports
            path('station_logout/',views.station_logout,name='station_logout'),
            path('update_station_status/', views.update_station_status, name='update_station_status'),
            
            # User
            path('login/', views.user_login, name='user_login'),
            path('register/', views.user_register, name='user_register'),
            path('userhome/', views.user_home, name='user_home'),
            path('station/', views.user_station_selection, name='user_station_selection'),
            path('slot/<str:sid>/', views.user_view_station_slots, name='slot'),
            path('tariff/', views.tariff_view, name='tariff'),
            path('history/', views.user_history, name='history'),
            path('history/pdf/', views.history_pdf, name='history_pdf'),  # PDF download for history
            path('book/', views.book_slot, name='book_slot'),
            path('rebook/<int:rid>/', views.rebook, name='rebook'),
            path('booking-out/<int:rid>/', views.booking_out, name='booking_out'),
            path('payment/<int:rid>/', views.payment, name='payment'),
            path('select/', views.select_plan, name='select_plan'),
            path('verify_otp/<int:rid>/', views.verify_otp, name='verify_otp'),
            path('resend_otp/<int:rid>/', views.resend_otp, name='resend_otp'),
            path('user_logout/',views.user_logout,name='user_logout'),
            path('forgot-password/', views.forgot_password, name='forgot_password'),
            path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
            path('booking-qr/<int:rid>/', views.booking_qr, name='booking_qr'),
            path('upi-payment/<int:rid>/', views.upi_payment, name='upi_payment'),
            path('maps/', views.maps_view, name='maps_view'),
            path('charging-wait/<int:rid>/', views.charging_wait, name='charging_wait'),
            path('razorpay-payment/<int:rid>/', views.razorpay_payment, name='razorpay_payment'),
            path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
            path('api/booking_status/', views.booking_status_api, name='booking_status_api'),
            path('api/station_status/', views.station_status_api, name='station_status_api'),
            path('api/station_heartbeat/', views.station_heartbeat, name='station_heartbeat'),
            path('api/station/<str:sid>/slots/', views.station_slots_api, name='station_slots_api'),
        ]
