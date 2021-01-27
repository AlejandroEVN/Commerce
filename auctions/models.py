from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=240)
    initial_price = models.DecimalField(max_digits=8, decimal_places=2)
    current_price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True,
        null=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.URLField(default=None)
    category = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}: {self.initial_price}"
    

class Listing(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="creator"
    )

    item = models.OneToOneField(
        Item, 
        on_delete=models.CASCADE
    )
    
    sold = models.BooleanField(default=False)

    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="winner",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.item.name}, price: {self.item.initial_price} by {self.user.username}"


class Bid(models.Model):
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    bid_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_amount} by {self.bidder} on {self.date}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: '{self.content}'"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.listing.item.name} on {self.user.username}'s watchlist"