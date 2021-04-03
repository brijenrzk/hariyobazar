from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .forms import CreateBlogForm
from django.contrib import messages
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
# Create your views here.


def adminBlogs(request):
    blog = Blogs.objects.all()
    context = {'blog': blog}
    return render(request, "blogs/admin-blogs-list.html", context)


def adminAddBlogs(request):
    blogForm = CreateBlogForm()
    if request.method == 'POST':
        blogForm = CreateBlogForm(request.POST, request.FILES)
        if blogForm.is_valid():
            blogForm.save()
            messages.success(request, 'Sucessfully Created')
            return redirect("blogs:admin-blogs")
    context = {'blogForm': blogForm}
    return render(request, "blogs/admin-blogs-add.html", context)


def adminDeleteBlogs(request, pk=None):
    blog = Blogs.objects.get(id=pk)
    blog.delete()
    messages.success(request, 'Blog Deleted')
    return redirect("blogs:admin-blogs")


def adminEditBlogs(request, slug):
    blog = Blogs.objects.get(slug=slug)
    blogForm = CreateBlogForm(instance=blog)
    if request.method == 'POST':
        blogForm = CreateBlogForm(request.POST, request.FILES, instance=blog)
        if blogForm.is_valid():
            blogForm.save()
            messages.success(request, 'Sucessfully Edited')
            return redirect("blogs:admin-blogs")
    context = {'blogForm': blogForm}
    return render(request, "blogs/admin-blogs-edit.html", context)


# user side


class BlogsView(ListView):
    model = Blogs
    paginate_by = 6
    context_object_name = 'blog'
    template_name = 'blogs/user/blogs.html'

    def get_queryset(self, **kwargs):
        return Blogs.objects.all().order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blogs"
        return context


def singleBlog(request, slug):
    blog = Blogs.objects.get(slug=slug)
    title = "Blogs"
    context = {'title': title, 'blog': blog}
    return render(request, "blogs/user/blogs-single.html", context)
