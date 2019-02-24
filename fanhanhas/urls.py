from django.urls import path

from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('report', views.report, name='report'),
    path('recording', views.index, name='index'),
    path('report_generator', views.report_generator, name='report_generator')
]