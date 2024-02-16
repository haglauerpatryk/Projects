from django.urls import path
from . import views

urlpatterns = [
    path("",          views.index,    name="index"),
    path("tables/",   views.tables,   name="tables"),
    path("charts/",   views.charts,   name="charts"),
    path("favorite/", views.favorite, name="favorite"),
    path("contact/",  views.contact,  name="contact"),
]