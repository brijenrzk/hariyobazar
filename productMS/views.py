from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .forms import CreateProductForm, CreateProductImageForm, CreateCategoryForm, CreateSubCategoryForm, CreateBanner, PostProductForm, PostEditProductForm, ReplyForm
from django.contrib import messages
from .models import Category, SubCategory, Product, ProductPhoto, Banner, Questions
import random
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
            product.photo = request.FILES.get('photo')
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


def adminProductsAll(request):
    prodImg = ProductPhoto.objects.all()
    prods = Product.objects.all()
    context = {'prod': prodImg, 'prods': prods}
    return render(request, "productMS/admin-products-all.html", context)


# Banner

def adminBanner(request):
    banner = Banner.objects.all()
    context = {'banner': banner}
    return render(request, "productMS/banner/banner.html", context)


def adminBannerAdd(request):
    form = CreateBanner()
    if request.method == 'POST':
        form = CreateBanner(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucessfully Created')
            return redirect("productMS:admin-banner")

    context = {'form': form}
    return render(request, "productMS/banner/banner-add.html", context)


def adminBannerDelete(request, pk=None):
    b = Banner.objects.get(id=pk)
    b.delete()
    messages.success(request, 'Banner Deleted')
    return redirect("productMS:admin-banner")


# User side


def index(request):
    # preminum products
    prodPrem = Product.objects.filter(
        premium=True).order_by('-publish_date')[0:4]
    # latest products
    prodLat = Product.objects.exclude(
        premium=True).order_by('-publish_date')[0:8]
    # recommended products
    prodR = list(Product.objects.filter(premium=False))
    if(len(prodR) > 2):
        prodRecom = random.sample(prodR, 2)
    else:
        prodRecom = Product.objects.filter(premium=False)[0:4]
    # Category dropdown
    cat = Category.objects.all()
    # Banner
    ban = Banner.objects.all()

    context = {'prodPrem': prodPrem,
               'prodLat': prodLat, 'prodRecom': prodRecom, 'cat': cat, 'ban': ban}

    return render(request, "productMS/user/index.html", context)


# def premiumProducts(request):
#     # preminum products
#     prod = Product.objects.filter(
#         premium=True).order_by('-publish_date')
#     title = "Premium Listings"

#     # Category dropdown
#     cat = Category.objects.all()

#     context = {'prod': prod, 'title': title, 'cat': cat, }

#     return render(request, "productMS/user/product-list.html", context)

# premium product
class PremiumView(ListView):
    model = Product
    paginate_by = 4
    queryset = Product.objects.filter(premium=True).order_by('-publish_date')
    context_object_name = 'prod'
    template_name = 'productMS/user/product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        context['title'] = "Premium Listings"
        return context


# latest product
# def latestProducts(request):
#         # preminum products
#     prod = Product.objects.filter(
#         premium=False).order_by('-publish_date')
#     title = "Latest Listings"

#     # Category dropdown
#     cat = Category.objects.all()

#     context = {'prod': prod, 'title': title, 'cat': cat, }

#     return render(request, "productMS/user/product-list.html", context)


class LatestView(ListView):
    model = Product
    paginate_by = 4
    queryset = Product.objects.filter(premium=False).order_by('-publish_date')
    context_object_name = 'prod'
    template_name = 'productMS/user/product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        context['title'] = "Latest Listings"
        return context

# Category


# def categoryProducts(request, slug):
#     prod = Product.objects.filter(
#         category__slug=slug).order_by('-publish_date')
#     c_name = Category.objects.get(slug=slug)
#     title = c_name.category_name

#     # Category dropdown
#     cat = Category.objects.all()

#     context = {'prod': prod, 'title': title, 'cat': cat, }

#     return render(request, "productMS/user/product-list.html", context)


class CategoryView(ListView):
    model = Product
    paginate_by = 4
    context_object_name = 'prod'
    template_name = 'productMS/user/product-list.html'

    def get_queryset(self, **kwargs):
        return Product.objects.filter(category__slug=self.kwargs['slug']).order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        c_name = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = c_name
        return context


# Search
def searchProduct(request):
     # Category dropdown
    cat = Category.objects.all()
    title = "Search Results"
    query = ""
    context = {}
    if request.GET:
        query = request.GET['q']
    prod = get_data_queryset(query)
    context = {'prod': prod, 'title': title, 'cat': cat, }
    #context['prod'] = prod
    return render(request, "productMS/user/product-list.html", context)


# class SearchView(ListView):
#     model = Product
#     paginate_by = 4
#     context_object_name = 'prod'
#     template_name = 'productMS/user/product-list.html'

#     def get_queryset(self):  # new
#         query = self.request.GET.get('q')
#         object_list = Product.objects.filter(
#             Q(name__icontains=query)
#         )
#         return object_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cat'] = Category.objects.all()
#         context['title'] = "Serach Results"
#         return context


def get_data_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    # if len(queries) == 0:
    #     print("nothing")

    for q in queries:
        products = Product.objects.filter(
            Q(name__icontains=q)
        )

        for p in products:
            queryset.append(p)
    queryset = queryset[0:30]

    return (set(queryset))


def singleProduct(request, slug):
    cat = Category.objects.all()
    prod = Product.objects.get(slug=slug)
    prodImg = ProductPhoto.objects.filter(product=prod)
    fav = bool

    if prod.favourites.filter(id=request.user.id).exists():
        fav = True
    view = prod.views
    prod.views = view + 1
    prod.save()

    if request.method == 'POST':
        askQuestions = Questions()
        askQuestions.question = request.POST['question']
        askQuestions.user = request.user
        askQuestions.product = prod

        askQuestions.save()

    questions = Questions.objects.filter(product=prod)
    #question = {}
    context = {'prod': prod, 'prodImg': prodImg,
               'cat': cat, 'questions': questions, 'fav': fav}
    return render(request, "productMS/user/single-product.html", context)


@login_required(login_url='userMS:login')
def sell(request):
    productForm = PostProductForm()
    productImageForm = CreateProductImageForm()

    if request.method == 'POST':
        productForm = PostProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            product = Product()
            product.name = productForm.cleaned_data.get('name')
            product.description = productForm.cleaned_data.get('description')
            product.price = productForm.cleaned_data.get('price')
            product.photo = request.FILES.get('photo')
            product.category = productForm.cleaned_data.get('category')
            product.sub_category = productForm.cleaned_data.get('sub_category')
            product.user = request.user
            product.show_contact = productForm.cleaned_data.get('show_contact')
            product.save()

            fil = request.FILES.getlist('ph')

            for f in fil:
                pro_photo = ProductPhoto()
                pro_photo.product = product
                pro_photo.product_photo = f
                pro_photo.save()
            return redirect("productMS:index")
        else:
            print("fail")

    context = {'productForm': productForm,
               'productImageForm': productImageForm}
    return render(request, "productMS/user/sell.html", context)


def myAds(request):
    prod = Product.objects.filter(user=request.user).prefetch_related('ques')
    productForm = PostEditProductForm()
    cmt = Questions.objects.filter(
        answer__exact='').count()
    context = {'prod': prod, 'productForm': productForm, 'cmt': cmt}
    return render(request, 'productMS/user/ads.html', context)


def deleteMyAds(request, pk=None):
    prod = Product.objects.get(id=pk)
    prod.delete()
    return redirect("productMS:myAds")


def comments(request):
    prod = Product.objects.filter(user=request.user).prefetch_related('ques')

    cmt = Questions.objects.filter(
        answer__exact='').count()

    context = {'prod': prod, 'cmt': cmt}
    return render(request, 'productMS/user/comments.html', context)


def postEditProducts(request, pk=None):
    prod = Product.objects.get(id=pk)
    productForm = PostProductForm(instance=prod)
    cmt = Questions.objects.filter(
        answer__exact='').count()

    if request.method == 'POST':
        productForm = PostProductForm(
            request.POST, instance=prod)
        if productForm.is_valid():
            productForm.save()
            messages.success(request, 'Sucessfully Updated')
            return redirect("productMS:myAds")
    context = {'productForm': productForm, 'cmt': cmt}
    return render(request, "productMS/user/ads-edit.html", context)


def reply(request, pk=None):
    ques = Questions.objects.get(id=pk)
    replyForm = ReplyForm(instance=ques)
    cmt = Questions.objects.filter(
        answer__exact='').count()

    if request.method == 'POST':
        replyForm = ReplyForm(request.POST, instance=ques)
        if replyForm.is_valid():
            replyForm.save()
            messages.success(request, 'Comment Replied')
            return redirect("productMS:comments")

    context = {'replyForm': replyForm, 'ques': ques, 'cmt': cmt}
    return render(request, "productMS/user/reply.html", context)


def favourite_add(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        result = ''
        prod = Product.objects.get(id=id)
        if prod.favourites.filter(id=request.user.id).exists():
            prod.favourites.remove(request.user)
            prod.save()
            result = 0
        else:
            prod.favourites.add(request.user)
            prod.save()
            result = 1
        print(result)

    return JsonResponse({'result': result, })


def watchlist(request):
     # Category dropdown
    cat = Category.objects.all()
    title = "Watchlist"
    fav = True

    prod = Product.objects.filter(favourites=request.user)
    context = {'prod': prod, 'title': title, 'cat': cat, 'fav': fav}
    #context['prod'] = prod
    return render(request, "productMS/user/product-list.html", context)


def sold(request, pk=None):
    prod = Product.objects.get(id=pk)
    if prod.sold:
        prod.sold = False
        prod.save()
    else:
        prod.sold = True
        prod.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
