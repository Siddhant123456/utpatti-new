from django.urls import path
from . import views


urlpatterns = [
    path('place-bid/' , views.place_bid , name = "place_bid"),
    path('create-bid/<int:id>/', views.create_bid , name = "create_bid"),
    path('active_bids/', views.active_bids , name = "active_bids"),
    path('view_bids/', views.view_bids , name = "view_bids"),
]
