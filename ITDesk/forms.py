from django import forms
from ITDesk.models import Tkt_Cat, Tkt_SubCat

class TicketForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Tkt_Cat.objects.all(), label="Category")
    subcategory = forms.ModelChoiceField(queryset=Tkt_SubCat.objects.none(), label="Subcategory")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Tkt_SubCat.objects.filter(Category_id=category_id)
            except (ValueError, TypeError):
                pass
