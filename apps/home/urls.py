from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve



from apps.home import views

urlpatterns = [
    # The home page
    path('', views.IndexView.as_view(), name='home'),

    path('sobre-nos', views.SobrenosView.as_view(), name='sobre-nos'),

    path('departamentos/', views.DepartamentosView.as_view(), name='departamentos'),

    path('graduacao/', views.GraduacaoViews.as_view(), name='graduacao'),

    path('departamentos/<str:sigla>', views.DepartamentoView.as_view(), name='docentes'),

    path('<str:sigla>/docente/<str:numero_lattes>', views.DocenteView.as_view(), name='docente'),
]
