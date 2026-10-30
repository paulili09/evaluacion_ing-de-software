from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('soluciones/', views.solutions, name='solutions'),
	path('proceso/', views.process, name='process'),
	path('nosotros/', views.about, name='about'),
	path('impacto/', views.impact, name='impact'),
	path('recursos/', views.resources, name='resources'),
	path('contacto/', views.contact, name='contact'),
	path('informes/', views.reports, name='reports'),
]
