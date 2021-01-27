from django.contrib import admin
from .models import User, Bid, Item, Listing, Comment, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Watchlist)