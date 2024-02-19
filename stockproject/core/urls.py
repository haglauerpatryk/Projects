from django.urls import path
from .views import IndexView, TablesView, ChartsView, FavouriteView, ContactView

urlpatterns = [
    path("",           IndexView.as_view(),     name="index"),
    path("tables/",    TablesView.as_view(),    name="tables"),
    path("charts/",    ChartsView.as_view(),    name="charts"),
    path("favourite/", FavouriteView.as_view(), name="favourite"),
    path("contact/",   ContactView.as_view(),   name="contact"),
]