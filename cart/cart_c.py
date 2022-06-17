from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """ Инициализация объекта корзины """
        self.session = request.session  # Мы запоминаем текущую сессию в атрибуте self.session
        cart = self.session.get(settings.CART_SESSION_ID) # Затем пытаемся получить данные корзины, обращаясь к словарю сесси, ключу cart
        if not cart:
            # Сохраняем в сессии пустую корзину
            """ Если не получаем объект корзины, создаем ее как пустой словарь в сессии. В этом словаре ключами будут 
                являться ID товаров, а значениями – количество и цена. Так мы будем уверены, что
                товар не добавлен в корзину больше одного раза. Хранение корзины в виде
                словаря упростит доступ к ее элементам."""
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        ''' Проходим по товарам корзины и получаем соответствующие объекты Product '''
        product_ids = self.cart.keys()  # достаем все id товаров(ключи) из корзины
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids) # все продукты которые есть в корзине

        for product in products: # все продукты которые есть в корзине
            self.cart[str(product.id)]['product'] = product # создаем ключ продукт и присваеваем продукт

        for item in self.cart.values():
            item['price'] = Decimal(item['price']) # из строки в число
            item['total_price'] = item['price'] * item['quantity'] # считаем цену
            yield item

    def add(self, product, quantity=1, update_quantity=False): #нужно ли заменить значение количества товаров на новое (True)
        ''' Добавления товара в корзину или обновление его кол-ва '''

        product_id = str(product.id) # Django использует формат JSON для сериализации данных сессии, а в JSON-ключами могут быть только строки
        if product_id not in self.cart: # если продукта нет в корзине(проверка на дублирование)
            ''' мы создаем объект в словаре с ключем product_id и значением : ...  '''
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)} # Данные о цене также преобразуются в строку, чтобы их можно было сериализовать
        if update_quantity: # если обновляем кол-во в закаже просто обращаемся к ключу кол-во
            self.cart[product_id]['quantity'] = quantity
        else: # если добавляем к кол-ву еще несколько
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """ Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart: # если такой id есть в корзине
            del self.cart[product_id] # удаляем объект из корзины
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart  # обновление сессии cart
        self.session.modified = True  #  отметить сеанс как измененный чтобы убедиться что он сохранен

    def __len__(self):
        """ Подсчет всех товаро в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ Подсчет стоимости всей корзины """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ удаление корзины из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
