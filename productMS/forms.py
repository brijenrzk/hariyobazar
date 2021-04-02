from django import forms
from .models import *


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']


class CreateSubCategoryForm(forms.Form):
    sub_category_name = forms.CharField(max_length=80)
    category = forms.ModelChoiceField(
        required=True, widget=forms.Select, queryset=Category.objects.all(), initial=0)

    def clean(self):
        cleaned_data = super(CreateSubCategoryForm, self).clean()
        sub_category_name = cleaned_data.get('sub_category_name')
        category = cleaned_data.get('category')


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'category',
                  'sub_category', 'condition', 'warranty', 'premium', 'show_contact']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(
                    category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.sub_category.all(
            )


class PostProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'category',
                  'sub_category', 'show_contact']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(
                    category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.sub_category.all(
            )


class CreateProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductPhoto
        fields = ['product_photo']


class CreateBanner(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['name', 'photo', 'url']


class PostEditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'show_contact']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['answer']
