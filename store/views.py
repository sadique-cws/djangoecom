from django.shortcuts import render,get_object_or_404,redirect
from store.models import *
from django.views.generic import ListView,DetailView,View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from store.forms import *
from django.contrib import messages
import random
import string

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


def create_txn_id():
    return  '' .join(random.choices(string.ascii_lowercase + string.digits,k=20))


class ItemView(DetailView):
    model = Item
    template_name = "product.html"
    slug_url_kwarg = "slug"

    def get_context_data(self,*args,**kwargs):
        context = super(ItemView,self).get_context_data(*args,**kwargs)
        context["related_items"] = Item.objects.exclude(slug=self.kwargs["slug"])
        return context


class RemoveFromCart(LoginRequiredMixin,View):
    def get(self,request,slug,*args,**kwargs):
        item = get_object_or_404(Item,slug=slug)
        order_qs = Order.objects.filter(user = request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=slug).exists():
                order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False
                )[0]

                if order_item.qty > 1:
                    order_item.qty -= 1
                    order_item.save()
                    #todo: msg your cart is updated
                else:
                    order.items.remove(order_item)
                    #todo: msg item removed
                return redirect("store:order_summary")
            else:
                #todo: msg this item is not in your cart
                return redirect("store:order_summary")
        else:
            #todo: you do not have any active order in your cart
            return redirect("store:order_summary")


class RemoveItem(LoginRequiredMixin,View):
    def get(self,request,slug,*args,**kwargs):
        item = get_object_or_404(Item,slug=slug)

        order_qs = Order.objects.filter(
            user = request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
                order.items.remove(order_item)
                order_item.delete()
                #todo: msg item removed successfully
                return redirect("store:order_summary")
            else:
                #todo: item was not in your cart
                return redirect("store:order_summary")
        else:
            #todo: you don't have any active order
            return redirect("store:order_summary")


class AddToCart(LoginRequiredMixin,View):
    def get(self,request,slug,*args,**kwargs):
        item = get_object_or_404(Item,slug=slug)

        order_item, create = OrderItem.objects.get_or_create(
            item = item,
            user = request.user,
            ordered= False
        )

        order_query = Order.objects.filter(user=request.user,ordered=False)

        if order_query.exists():
            order = order_query[0]

            if order.items.filter(item__slug=slug).exists():
                order_item.qty += 1
                order_item.save()
                messages.success(self.request,"item updated successfully")
            else:
                order.items.add(order_item)
                messages.success(self.request, "item added successfully")
            return redirect("store:order_summary")
        else:
            add_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered=False,
                add_date=add_date
            )

            order.items.add(order_item)
            #todo: msg item added successfully
            return redirect("store:order_summary")


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            order = Order.objects.get(user=request.user,ordered=False)
            form = CouponForm()
            context = {"order":order,"form":form}
        except ObjectDoesNotExist:
            #todo: msg you do not have any active order
            return redirect("store:homepage")

        return render(self.request,"order_summary.html",context)


class CheckoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = CheckoutForm()

            context = {
                "form": form,
                'order':order,
                'address':Address.objects.filter(user=self.request.user)
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request,"You don't have any active order")
            return redirect("store:order_summary")

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user,ordered=False)

            if self.request.method == "POST":
                save_address = self.request.POST.get("save_address",None)

                if save_address != None:
                    selected_address = Address.objects.get(id=save_address)
                    order.address = selected_address
                    order.save()
                    return redirect("store:payment")
                else:
                    if form.is_valid():
                        data = form.save(commit=False)
                        data.user = self.request.user
                        data.save()

                        order.address = data
                        order.save()
                        return redirect("store:payment")
                    else:
                        messages.warning("please check form data")
                        return redirect("store:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request,"not found any active order")
            return redirect("store:order_summary")


class PaymentView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)

        if not order.address:
            return redirect("store:checkout")
        else:
            context = {
                "order":order,
            }
        return render(self.request,"payment.html",context)

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)

        if self.request.POST.get("payment") == "cod":
            pay = Payment()

            pay.user = self.request.user

            pay.amount = order.get_total()
            pay.txn_id  = create_txn_id()
            pay.order_id = order
            pay.save()

            order_item = order.items.all()
            order_item.update(ordered=True)

            for item in order_item:
                item.save()

            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

            return redirect("store:homepage")


def check_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return True
    except ObjectDoesNotExist:
        return False

def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request,"this coupon doesn't exist")
        return redirect("store:order_summary")


class AddCouponView(View):
    def post(self,request,*args,**kwargs):
        if self.request.method == "POST":
            form = CouponForm(self.request.POST or None)

            if form.is_valid():
                code = form.cleaned_data.get("code")
                if check_coupon(self.request,code):
                    order = Order.objects.get(user=self.request.user,ordered=False)
                    order.coupon = get_coupon(self.request,code)
                    order.save()
                    messages.success(self.request,"msg coupon add successfully")
                    return redirect("store:order_summary")
                else:
                    messages.error(self.request,"invalid Coupon")
                    return redirect("store:order_summary")
            else:
                #todo : invalid form data try again
                return redirect("store:order_summary")


class MyOrderView(View):
    def get(self,request,*args,**kwargs):

        context = {
            "order":Order.objects.filter(user=self.request.user,ordered=True)
        }

        return render(self.request,"myOrder.html",context)

