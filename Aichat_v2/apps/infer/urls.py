#encoding: utf-8
from django.urls import path
from . import views

app_name = 'infer'

urlpatterns = [
    path('',views.index,name='index'),
    path('add_args/',views.add_args,name='add_args'),
    path('add_infers/',views.add_infers,name='add_infers'),
    path('add_args2/',views.add_args2,name='add_args2'),
    path('delete_infers/',views.delete_infers,name='delete_infers'),
    path('begain_infers/',views.begain_infers,name='begain_infers'),
    path('download/',views.download,name='download'),
]