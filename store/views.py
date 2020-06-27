from django.shortcuts import render,get_object_or_404,redirect
from store.models import *
from django.views.generic import ListView,DetailView,View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

class ItemView(DetailView):
    model = Item
    template_name = "product.html"
    slug_url_kwarg = "slug"


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
                #todo: msg  item updated successfully
            else:
                order.items.add(order_item)
                #todo: msg item added successfully

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
            context = {"order":order}
        except ObjectDoesNotExist:
            #todo: msg you do not have any active order
            return redirect("store:homepage")

        return render(self.request,"order_summary.html",context)



