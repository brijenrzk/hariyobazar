from django import forms
from .models import *


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']



class CreateSubCategoryForm(forms.Form):
    sub_category_name = forms.CharField(max_length=80)
    category = forms.ModelChoiceField(required=True, widget=forms.Select, queryset=Category.objects.all(),initial=0)
    def clean(self):
        cleaned_data = super(CreateSubCategoryForm, self).clean()
        sub_category_name = cleaned_data.get('sub_category_name')
        category = cleaned_data.get('category')
    
   

class CreateProductForm(forms.Form):
    name = forms.CharField(max_length=80)
    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea()
    )
    price = forms.IntegerField()
    category = forms.ChoiceField(
        choices=[(cat.id, cat.category_name) for cat in Category.objects.all()])
    condition = forms.CharField(max_length = 20)
    warranty = forms.IntegerField()
    premium = forms.BooleanField()


    def clean(self):
        cleaned_data = super(CreateProductForm, self).clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        condition = cleaned_data.get('condition')
        warranty = cleaned_data.get('warranty')
        premium = cleaned_data.get('premium')


class CreateProductImageForm(forms.Form):

    class Meta:
        model = ProductPhoto
        fields = ['product_photo']