"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(-1) is True, 'Ожидаем True. quantity продукта меньше запрашиваемого'
        assert product.check_quantity(0) is True, 'Ожидаем True. quantity продукта меньше запрашиваемого'
        assert product.check_quantity(999) is True, 'Ожидаем True. quantity продукта больше запрашиваемого'
        assert product.check_quantity(1000) is True, 'Ожидаем True. quantity продукта равно запрашиваемому'
        assert product.check_quantity(1001) is False, 'Ожидаем False. quantity продукта меньше запрашиваемого'

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(333)
        assert product.quantity == 667, 'осталось после покупки 333шт'
        product.buy(333)
        assert product.quantity == 334, 'осталось после покупки 333шт'
        product.buy(333)
        assert product.quantity == 1, 'осталось после покупки 333шт'

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(2000)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0, 'Проверка что корзина пустая'
        cart.add_product(product)
        assert cart.products[product] == 1, 'проверим добавление продуков +1'
        cart.add_product(product, 9999)
        assert cart.products[product] == 10000, 'проверим добавляем продуктов +9999'
        assert len(cart.products) == 1, 'проверим количество типов продуктов в корзине'

    def test_remove_product(self, cart, product):
        cart.add_product(product, 1000)
        cart.remove_product(product, 400)
        assert cart.products[product] == 600, 'проверяем остаток в корзине после удаления'
        cart.remove_product(product)
        assert len(cart.products) == 0, 'Удаление продукта без указания количества'
        cart.add_product(product, 2000)
        cart.remove_product(product, 3000)
        assert len(cart.products) == 0, 'Удаление продукта с указанием количества больше чем в корзине'
        cart.add_product(product, 100)
        cart.remove_product(product, 100)
        assert len(cart.products) == 0, 'Удаление точно такого же количества товара, которое было в корзине'


    def test_clear(self,  cart, product):
        cart.add_product(product, 100)
        cart.clear()
        assert len(cart.products) == 0, 'проверка очистки корзины'

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == 500, 'проверка подсчета стоимости товара в корзине'

    def test_buy_product(self, cart, product):
        cart.add_product(product, 20)
        cart.buy()
        assert len(cart.products) == 0, 'Удаление товара из корзины после покупки'

    def test_product_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1234)
        with pytest.raises(ValueError):
            assert cart.buy()
