from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('signin/',views.signin),
    path('signup/', views.signup),
    path('travelplan/', views.travelplan),
    path('settravelplan/', views.settravelplan),
    path('updatetravelplan/', views.updatetravelplan),
    path('deletetravelplan/<int:travel_id>/', views.deletetravelplan),
    path('getbooking/', views.getbooking),
    path('book/', views.booking),
    path('updatebooking/', views.updatebooking),
    path('getbookingof/', views.getbookingof),
    path('logout/', views.logout),
    path('checkUser/', views.checkUser),
    path('deletebooking/<int:booking_id>/', views.deletebooking),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)