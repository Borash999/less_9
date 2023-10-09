import logging

from django.http import HttpResponse

# from django.shortcuts import render


logger = logging.getLogger(__name__)

headers = {'Cache-Control': 'no-cache, must-revalidate',
           'Pragma': 'no-cache'}


def main(request):
    body = """
    <title>Главная страница</title>
    <body>
        <div>
            <h1>Главная страница</h1>
            <p>Содержимое главной страницы</p>
            <p>Перейдите на страницу: /about_me</p>
        </div>
        <footer>
            <div>
                <p>Copyright &copy;
                    <script type="text/javascript"> document.write(new Date().getFullYear());</script>
                    Communications Inc. Все права защищены.
                </p>
            </div>
        </footer>
    </body>
    """
    logger.info(f'Страница открыта: {body}')
    return HttpResponse(body, charset="utf-8", headers=headers)


def about_me(request):
    body = """
        <title>О себе</title>  
        <body>     
            <div>
                <h1>Баранов Владислав Евгеньевич</h1>
                <p>Мужчина, 26 лет, родился 9 сентября 1997</p>
                <p>Перейдите на страницу: /main</p>
            </div>
            <footer>
                <div>
                    <p>Copyright &copy;
                        <script type="text/javascript"> document.write(new Date().getFullYear());</script>
                        Communications Inc. Все права защищены.
                    </p>
                </div>
            </footer>
        </body>
        """
    logger.info(f'Страница открыта: {body}')
    return HttpResponse(body, charset="utf-8", headers=headers)

from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.total_amount}"

# Создание клиента
def create_client(name, email, phone_number, address):
    client = Client(name=name, email=email, phone_number=phone_number, address=address)
    client.save()
    return client

# Получение всех клиентов
def get_all_clients():
    return Client.objects.all()

# Получение клиента по ID
def get_client_by_id(client_id):
    return Client.objects.get(id=client_id)

# Обновление информации о клиенте
def update_client(client_id, name, email, phone_number, address):
    client = get_client_by_id(client_id)
    client.name = name
    client.email = email
    client.phone_number = phone_number
    client.address = address
    client.save()

# Удаление клиента
def delete_client(client_id):
    client = get_client_by_id(client_id)
    client.delete()

# Создание товара
def create_product(name, description, price, quantity):
    product = Product(name=name, description=description, price=price, quantity=quantity)
    product.save()
    return product

# Получение всех товаров
def get_all_products():
    return Product.objects.all()

# Получение товара по ID
def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)

# Обновление информации о товаре
def update_product(product_id, name, description, price, quantity):
    product = get_product_by_id(product_id)
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product.save()

# Удаление товара
def delete_product(product_id):
    product = get_product_by_id(product_id)
    product.delete()

# Создание заказа
def create_order(client, products, total_amount):
    order = Order(client=client, total_amount=total_amount)
    order.save()
    order.products.set(products)
    return order

# Получение всех заказов
def get_all_orders():
    return Order.objects.all()

# Получение заказа по ID
def get_order_by_id(order_id):
    return Order.objects.get(id=order_id)

# Обновление информации о заказе
def update_order(order_id, client, products, total_amount):
    order = get_order_by_id(order_id)
    order.client = client
    order.total_amount = total_amount
    order.save()
    order.products.set(products)

# Удаление заказа
def delete_order(order_id):
    order = get_order_by_id(order_id)
    order.delete()

    import datetime

# Заказы клиента
orders = [
 {
 'id': 1,
 'timestamp': datetime.datetime(2022, 10, 5),
 'products': ['product1', 'product2', 'product3']
 },
 {
 'id': 2,
 'timestamp': datetime.datetime(2022, 10, 14),
 'products': ['product2', 'product4', 'product5']
 },
 {
 'id': 3,
 'timestamp': datetime.datetime(2022, 9, 10),
 'products': ['product3', 'product6', 'product7']
 },
 {
 'id': 4,
 'timestamp': datetime.datetime(2022, 8, 20),
 'products': ['product1', 'product5', 'product8']
 }
]

def get_ordered_products(orders, days):
 result = set()

 # Получаем текущую дату
 today = datetime.datetime.now()

 # Вычисляем начальную дату
 start_date = today - datetime.timedelta(days=days)

 # Проходим по каждому заказу
 for order in orders:
 # Проверяем, попадает ли заказ в указанный временной интервал
    if start_date <= order['timestamp'] <= today:
 # Добавляем товары заказа в результат
 result.update(order['products'])

 return list(result)

# Получаем список товаров заказанных за последние 7 дней
last_7_days = get_ordered_products(orders, 7)
print("За последние 7 дней:")
print(last_7_days)

# Получаем список товаров заказанных за последние 30 дней
last_30_days = get_ordered_products(orders, 30)
print("За последние 30 дней:")
print(last_30_days)

# Получаем список товаров заказанных за последний год
last_365_days = get_ordered_products(orders, 365)
print("За последний год:")
print(last_365_days)

from django.db import models
from django.db.models.fields.files import ImageField

class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='product_photos/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

python manage.py makemigrations
python manage.py migrate

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'photo']