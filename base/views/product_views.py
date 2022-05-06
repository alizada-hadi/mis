from math import prod
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.models import Category
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_groups
from base.forms.product_forms import  CategoryForm

@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def product_list_create_view(request):
    products = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('pro_name')
        description = request.POST.get("desc")
        image = request.FILES.get("product-name")
        try:
            Category.objects.create(
                name=name, 
                description=description, 
                image=image
            )
            messages.success(request, "محصول جدید موفقانه ذخیره گردید. ")
        except:
            messages.error(request, "مشکلی رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        return redirect("product-list")

    context = {
        "products" : products
    }
    return render(request, "base/products/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def product_detail_view(request, pk):
    product = get_object_or_404(Category, pk=pk)
    context = {
        "product" : product
    }
    return render(request, "base/products/detail.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def product_update_view(request, pk):
    product = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول شما موفقانه ویرایش گردید. ")
            return redirect("product-list")
    else:
        form = CategoryForm(instance=product)

    context = {
        "product" : product, 
        "form" : form
    }

    return render(request, "base/products/update.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def delete_product_view(request):

    if request.method == "POST":
        product = Category.objects.get(id=request.POST.get("product"))
        try:
            product.delete()
            messages.success(request, "محصول شما موفقانه از سیستم حذف گردید. ")
        except:
            messages.error(request, "مشکلی رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        return redirect("product-list")

