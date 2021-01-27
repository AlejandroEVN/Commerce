from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<str:item_id>", views.listing, name="listing"),
    path("listing/<str:item_id>/<str:message>", views.listing, name="listing_em"),
    path("add_to_watchlist/<str:item_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<str:item_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_comment/<str:item_id>", views.add_comment, name="add_comment"),
    path("add_bid/<str:item_id>", views.add_bid, name="add_bid"),
    path("close_auction/<str:item_id>", views.close_auction, name="close_auction"),
    path("categories/search", views.categories_search, name="category_search")
]
