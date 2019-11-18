from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, Order, OrderProduct
from django.views.generic import DetailView, ListView, TemplateView, View
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    listCate = Category.objects.all()
    listPro = Product.objects.all()
    return render(request, 'home/index.html',{'Categories':listCate, 'Products':listPro,'nav': 'home'} )


def Products(request):
    listCate = Category.objects.all()
    listPro = Product.objects.all()
    return render(request, 'home/menu.html', {'Categories':listCate, 'Products':listPro,'nav': 'menu'})


class itemdetailView(DetailView):
    model = Product
    template_name = "home/product.html"


@login_required()
def add_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product , created = OrderProduct.objects.get_or_create(
        product = product,
        user = request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug = product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "sản phẩm đã được cập nhật số lượng")
        else:
            messages.info(request, "sản phẩm này đã được thêm vào giỏ hàng ")
            order.products.add(order_product)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "sản phẩm này đã được thêm vào giỏ hàng ")
    return redirect("cf:product", slug=slug)


@login_required()
def remove_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug = product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product = product,
                user = request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, "sản phẩm này đã xóa khỏi giỏ hàng")
            return redirect("cf:cart")
        else:
            messages.info(request, "sản phẩm này đã chưa có trong giỏ hàng")
            return redirect("cf:cart")       
    else:
        messages.info(request, "bạn chưa đặt hàng")
        return redirect("cf:cart")


@login_required()
def remove_single_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug = product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product = product,
                user = request.user,
                ordered=False
            )[0]
            if order_product.quantity >1:
                order_product.quantity -= 1
                order_product.save()
            else: 
                order.products.remove(order_product)
            
            messages.info(request, "sản phẩm này đã xóa khỏi giỏ hàng")
            return redirect("cf:cart")
        else:
            messages.info(request, "sản phẩm này đã chưa có trong giỏ hàng")
            return redirect("cf:cart")       
    else:
        messages.info(request, "bạn chưa đặt hàng")
        return redirect("cf:cart")


@login_required()
def add_single_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product , created = OrderProduct.objects.get_or_create(
        product = product,
        user = request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug = product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "sản phẩm đã được cập nhật số lượng")
        else:
            messages.info(request, "sản phẩm này đã được thêm vào giỏ hàng ")
            order.products.add(order_product)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "sản phẩm này đã được thêm vào giỏ hàng ")
    return redirect("cf:cart")


# def login(request):
#     return render(request, 'home/login.html')


#class cart(LoginRequiredMixin, TemplateView):
#    template_name = 'home/cart.html'



class cart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user =self.request.user, ordered = False)
            context = {
                'order' : order
            }
            return render(self.request, 'home/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "ban can kich hoat dat hang")
            return redirect("/")

        