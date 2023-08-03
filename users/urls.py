from django.urls import path
from .views import home, profile, RegisterView, viewFiles, addFile
from .views import addCustomer

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('profile/addcustomer', addCustomer, name='addcustomer'),
    path('customer/<str:name>', viewFiles, name='view-files'),
    path('customer/<str:name>/add', addFile, name='add-file')
]
