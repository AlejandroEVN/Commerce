import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Item, Bid, Comment, Listing,Watchlist
from .forms import ListingForm, CommentForm, BidForm, CategorySearchForm


def index(request):
    active_listings = Listing.objects.filter(sold=False)
    closed_listings = Listing.objects.filter(sold=True)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "closed_listings": closed_listings,
        "nbar": "index"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "nbar": "register"
        })


@login_required
def add_listing(request):
    if request.method == "GET":
        form = ListingForm()
        return render(request, "auctions/add_listing.html", {
            "form": form,
            "nbar": "add_listing"
        })
    else:
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            item = Item(
                name=title, 
                description=description,
                initial_price=price, 
                current_price=price,
                image=image_url, 
                category=category)
            item.save()

            listing = Listing(user=request.user, item=item)
            listing.save()

            return HttpResponseRedirect(reverse("index"))


def listing(request, item_id, message=None):

    comment_form = CommentForm()
    bid_form = BidForm()

    listing = Listing.objects.get(id=item_id)

    if not request.user.is_anonymous:
        listing_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing)

    comments = Comment.objects.filter(listing__id=item_id).order_by("-date")
    bids = Bid.objects.filter(listing__id=item_id).order_by("-bid_amount")

    template_variables = {
        "listing": listing,
        "comment_form": comment_form,
        "bid_form": bid_form,
        "comments": comments,
        "bids": bids,
        "message": message
    }

    if request.user.is_anonymous:
        return render(
            request,
            "auctions/listing.html",
            template_variables
        )
    elif len(listing_in_watchlist) == 0:
        return render(
            request, 
            "auctions/listing.html", 
            template_variables)
    else:
        template_variables["in_watchlist"] = True
        return render(
            request, 
            "auctions/listing.html",
            template_variables)


@login_required
def add_to_watchlist(request, item_id):
    try:
        listing_to_add = Listing.objects.get(id=item_id)
        to_add = Watchlist(user=request.user, listing=listing_to_add)
        to_add.save()
    except IntegrityError:
        message = "This listing is already in your watchlist"
        return HttpResponseRedirect(
                reverse("listing_em", 
                    kwargs={
                        "item_id": item_id,
                        "message": message
                    }
                )
            )
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def remove_from_watchlist(request, item_id):
    try:
        listing_to_remove = Watchlist.objects.filter(user=request.user, listing__id=item_id)
        listing_to_remove.delete()
    except:
        message = "An error occurred ! Go back to the home page"
        return render(request, "auctions/error.html", {
            "message": message
        })
    return HttpResponseRedirect(reverse("index"))


@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    ordered_watchlist = watchlist.order_by("listing")
    return render(request, "auctions/watchlist.html", {
        "watched_listings": ordered_watchlist,
        "nbar": "watchlist"
    })


@login_required
def add_comment(request, item_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        listing = Listing.objects.get(id=item_id)

        content = form.cleaned_data["content"]

        comment_to_add = Comment(
            user=request.user,
            listing=listing,
            content=content
        )

        comment_to_add.save()

        return HttpResponseRedirect(
            reverse(
                "listing", 
                kwargs={"item_id":item_id}
            )
        )

    
@login_required
def add_bid(request, item_id):

    form = BidForm(request.POST)

    if form.is_valid():        

        bid = form.cleaned_data["bid_amount"]

        listing = Listing.objects.get(id=item_id)
        highest_bid = Bid.objects.filter(
            listing__id=item_id
        ).aggregate(
                Max("bid_amount")
        )["bid_amount__max"]

        if highest_bid is None:
            highest_bid = listing.item.initial_price

        if bid > highest_bid:

            updated_fields = {
                "current_price": bid
            }

            item_to_update = Item.objects.filter(id=listing.item.id)
            item_to_update.update(**updated_fields)
            
            submit_bid = Bid(bidder=request.user, listing=listing, bid_amount=bid)
            submit_bid.save()

            message = "Your bid was succesfully placed!"

            return HttpResponseRedirect(
                reverse("listing_em",
                    kwargs={
                        "item_id": item_id,
                        "message": message
                    }
                )
            )

        else:
            message = "You have to introduce a valid amount !"

            return HttpResponseRedirect(
                reverse("listing_em", 
                    kwargs={
                        "item_id": item_id,
                        "message": message
                    }
                )
            )

    else:
        message = "The amount introduced is not valid !"
        return HttpResponseRedirect(
            reverse("listing_em", 
                kwargs={
                    "item_id": item_id,
                    "message": message
                }
            )
        )


@login_required
def close_auction(request, item_id):
    try:
        highest_bid = Bid.objects.filter(
                listing__id=item_id
            ).aggregate(Max("bid_amount"))["bid_amount__max"]
        winner = Bid.objects.get(
            listing__id=item_id,
            bid_amount=highest_bid
        ).bidder

        update_data = {
            "sold": True,
            "winner": winner
        }

        won_listing = Listing.objects.filter(id=item_id)
        won_listing.update(**update_data)
    except ObjectDoesNotExist:
        message = "You can't close an item without any bids !"
        return render(request, "auctions/error.html", {
            "message": message
        })
    return HttpResponseRedirect(reverse("index"))


def categories_search(request):
    if request.method == "GET":
        category_form = CategorySearchForm()

        return render(request, "auctions/category_search.html", {
            "form": category_form,
            "nbar": "categories"
        })

    else:
        form = CategorySearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            listings_found = Listing.objects.filter(item__category=category)

            if len(listings_found) != 0:
                return render(request, "auctions/category_results.html", {
                    "listings": listings_found,
                    "nbar": "categories"
                })
            else:
                message = f"There are not listings in the category {category}"
                return render(request, "auctions/category_search.html", {
                    "form": form,
                    "nbar": "categories",
                    "message": message
                })