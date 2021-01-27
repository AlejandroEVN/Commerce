from django import forms

CATEGORY_CHOICES = [
        ("none", "None"),
        ("toys", "Toys"),
        ("fashion", "Fashion"),
        ("electronics", "Electronics"),
        ("home", "Home"),
        ("books", "Books"),
        ("games", "Games")
    ]    

class ListingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    title = forms.CharField(
        required=True, 
        max_length=50, 
        label="Title",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Max 50 chars"
            }
        )
    )
    price = forms.CharField(
        required=True, 
        max_length=8, 
        label="Price"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Max 240 chars"
            }), 
        required=True, 
        max_length=240, 
        label="Description"
    )
    image_url = forms.URLField(
        required=False,
        label="Image URL"    
    )
    category = forms.ChoiceField (
        choices=CATEGORY_CHOICES,
        label="Category"
    )


class CommentForm(forms.Form):    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "Max 240 characters"

    content = forms.CharField(
        widget=forms.Textarea(attrs={
                "rows": 5
            }),
        required=True,
        max_length=240,
        label="Comment"
    )


class BidForm(forms.Form):    
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "Amount"
        
    bid_amount = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=True,
        label="Bid"
    )


class CategorySearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CategorySearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    category = forms.ChoiceField (
        choices=CATEGORY_CHOICES,
        label="Category"
    )