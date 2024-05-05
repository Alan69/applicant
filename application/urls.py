from django.urls import path
from . import views

urlpatterns = [
    # path('', views.application_view, name='application'),
    path('',views.ApplicationFormView.as_view(), name='application'),
    path('get_faculties/', views.get_faculties, name='get_faculties'),
    path('get_educ_groups/', views.get_groups, name='get_groups'),
    path('get_educs/', views.get_educs, name='get_educs'),
    path('get_subject1/', views.get_subject1, name='get_subject1'),
    path('get_regions/', views.get_regions, name='get_regions'),
    path('applicationedit/<int:pk>/',views.ApplicationUpdateView.as_view(), name='applicationedit'),
    path('generate_word/', views.generate_word, name="generate_word"),
    path('get_dogovor/', views.get_dogovor, name="get_dogovor"),
]