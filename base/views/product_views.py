from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.models import Category
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_groups


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