from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        district=request.POST.get('district')
        zip_code=request.POST.get('zip')
        
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            district=district,
            zip_code=zip_code,
        )
        order.items.add(*item_ids)
        
        body=('Cảm ơn bạn đã đặt hàng! Đơn hàng của bạn đang được chế biến và sẽ được gửi đến chỗ bạn nhanh thôi\n'
            f'Tổng cộng: {price}\n'
            'Cảm ơn đã đặt hàng')
        
        send_mail(
            'Cảm ơn bạn đã đặt hàng',
            body,
            'example@example.com',
            [email], 
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)