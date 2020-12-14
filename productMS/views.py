from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateProductForm, CreateProductImageForm, CreateCategoryForm, CreateSubCategoryForm
from django.contrib import messages
from .models import Category, SubCategory, Product, ProductPhoto
# Create your views here.


def adminProductsList(request):
    p = Product.objects.all()
    return render(request=request, template_name="productMS/admin-products-list.html", context={'product': p})


def adminProductsDelete(request, pk=None):
    prod = Product.objects.get(id=pk)
    prodImg = ProductPhoto.objects.filter(product=prod.id)
    for p in prodImg:
        p.delete()
    prod.delete()
    messages.success(request, 'Product Deleted')
    return redirect('productMS:admin-products-list')


def adminProductsAdd(request):
    productForm = CreateProductForm()
    productImageForm = CreateProductImageForm()
    context = {'productForm': productForm,
               'productImageForm': productImageForm}

    if request.method == 'POST':
        productForm = CreateProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            product = Product()
            product.name = productForm.cleaned_data.get('name')
            product.description = productForm.cleaned_data.get('description')
            product.price = productForm.cleaned_data.get('price')
            product.category = productForm.cleaned_data.get('category')
            product.sub_category = productForm.cleaned_data.get('sub_category')
            product.user = request.user
            product.condition = productForm.cleaned_data.get('condition')
            product.warranty = productForm.cleaned_data.get('warranty')
            product.premium = productForm.cleaned_data.get('premium')
            product.save()

            fil = request.FILES.getlist('ph')

            for f in fil:
                pro_photo = ProductPhoto()
                pro_photo.product = product
                pro_photo.product_photo = f
                pro_photo.save()
                print(f)

            return redirect("productMS:admin-products-list")

    return render(request, "productMS/admin-products-add.html", context)

# AJAX


def load_subcat(request):
    category_id = request.GET.get('category_id')
    sub_category = SubCategory.objects.filter(category_id=category_id)
    return render(request, 'productMS/subcat-dropdown-list.html', {'subcat': sub_category})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def adminProductsEdit(request, pk=None):
    prod = Product.objects.get(id=pk)
    productForm = CreateProductForm(instance=prod)
    context = {'productForm': productForm}
    if request.method == 'POST':
        productForm = CreateProductForm(
            request.POST, instance=prod)
        if productForm.is_valid():
            productForm.save()
            messages.success(request, 'Sucessfully Updated')
            return redirect("productMS:admin-products-list")
    return render(request, "productMS/admin-products-edit.html", context)


def adminProductsCategory(request):
    cat = Category.objects.all()
    context = {"cat": cat}
    return render(request, "productMS/admin-products-category.html", context)


def adminProductsAddCategory(request):
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        cat = form['category_name'].value()
        checkExist = Category.objects.filter(category_name=cat)
        if form.is_valid():
            if not checkExist:
                form.save()
                messages.success(request, 'Sucessfully Created')
                return redirect("productMS:admin-products-category")
            else:
                messages.info(request, 'This category already exists')

    context = {'form': form}
    return render(request, "productMS/admin-products-addCategory.html", context)


def adminProductsDeleteCategory(request, pk=None):
    c = Category.objects.get(id=pk)
    c.delete()
    messages.success(request, 'Category Deleted')
    return redirect('productMS:admin-products-category')


def adminProductsEditCategory(request, pk=None):
    c = Category.objects.get(id=pk)
    form = CreateCategoryForm(instance=c)
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST, instance=c)
        if form.is_valid():
            checkExist = Category.objects.filter(category_name=c.category_name)
            if not checkExist:
                form.save()
                messages.success(request, 'Successfully updated!')
                return redirect("productMS:admin-products-category")
            else:
                messages.info(request, 'This category already exists')

    context = {'form': form}
    return render(request, "productMS/admin-products-editCategory.html", context)


def adminProductsSubCategory(request):
    cat = SubCategory.objects.all()
    context = {"cat": cat}
    return render(request, "productMS/admin-products-subcategory.html", context)


def adminProductsAddSubCategory(request):
    form = CreateSubCategoryForm()
    if request.method == 'POST':
        form = CreateSubCategoryForm(request.POST)
        sub_cat = form['sub_category_name'].value()
        catId = form['category'].value()
        category = Category.objects.get(id=catId)
        checkExist = SubCategory.objects.filter(sub_category_name=sub_cat)
        if form.is_valid():
            if not checkExist:
                subCategory = SubCategory()
                subCategory.sub_category_name = sub_cat
                subCategory.category = category
                subCategory.save()
                messages.success(request, 'Sucessfully Created')
                return redirect("productMS:admin-products-subcategory")
            else:
                messages.info(request, 'This sub-category already exists')

    context = {'form': form}
    return render(request, "productMS/admin-products-addsubCategory.html", context)


def adminProductsDeleteSubCategory(request, pk=None):
    c = SubCategory.objects.get(id=pk)
    c.delete()
    messages.success(request, 'Sub-category Deleted')
    return redirect('productMS:admin-products-subcategory')


def adminProductsEditSubCategory(request, pk=None):
    c = SubCategory.objects.get(id=pk)
    form = CreateSubCategoryForm(
        initial={'sub_category_name': c.sub_category_name, 'category': c.category.id})
    if request.method == 'POST':
        form = CreateSubCategoryForm(request.POST, initial={
                                     'sub_category_name': c.sub_category_name, 'category': c.category.id})
        if form.is_valid():
            c.sub_category_name = form['sub_category_name'].value()
            catId = form['category'].value()
            category = Category.objects.get(id=catId)
            c.category = category
            c.save()
            messages.success(request, 'Successfully updated!')
            return redirect("productMS:admin-products-subcategory")

    context = {'form': form}
    return render(request, "productMS/admin-products-editSubcategory.html", context)
