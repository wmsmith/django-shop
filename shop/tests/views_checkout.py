#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from shop.addressmodel.models import Country, Address
from shop.models.ordermodel import Order
from shop.tests.util import Mock
from shop.views.checkout import CheckoutSelectionView
from shop.models.cartmodel import Cart
from decimal import Decimal
        
class ShippingBillingViewTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="test", 
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Toto")
        
        self.country = Country.objects.create(name="Switzerland")
        
        self.address = Address.objects.create(country=self.country)
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')
    
    def test_shipping_address_cache(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
        res2 = view.get_shipping_address_form()
        self.assertEqual(res, res2)
    
    def test_shipping_address_form_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
    
    def test_shipping_address_form_user_preset(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
    
    def test_shipping_address_form_user_no_preset(self):
        setattr(self.request, 'user', self.user)
        
        address = Address.objects.create(country=self.country, user_shipping=self.user)
        address.save()
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertEqual(res.instance, address)
    
    def test_billing_address_cache(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
        res2 = view.get_billing_address_form()
        self.assertEqual(res, res2)
    
    def test_billing_address_form_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
    
    def test_billing_address_form_user_preset(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
    
    def test_billing_address_form_user_no_preset(self):
        setattr(self.request, 'user', self.user)
        
        address = Address.objects.create(country=self.country, user_billing=self.user)
        address.save()
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertEqual(res.instance, address)

    #===========================================================================
    # Billing and shipping form
    #===========================================================================

    def test_billing_and_shipping_selection_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        self.assertNotEqual(res, None)
        
    def test_billing_and_shipping_selection_get(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        self.assertNotEqual(res, None)
        
    def test_billing_and_shipping_selection_cached(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        res2 = view.get_billing_and_shipping_selection_form()
        self.assertEqual(res, res2)

    #===========================================================================
    # Context Data
    #===========================================================================
    
    def test_get_context_data(self):
        setattr(self.request, 'method', 'GET')
        view = CheckoutSelectionView(request=self.request)
        ctx = view.get_context_data()
        self.assertNotEqual(ctx, None)
        self.assertNotEqual(ctx['shipping_address'], None)
        self.assertNotEqual(ctx['billing_address'], None)
        self.assertNotEqual(ctx['billing_shipping_form'], None)
        

class ShippingBillingViewOrderStuffTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="test", 
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Toto")
        
        self.order = Order.objects.create()
        
        self.country = Country.objects.create(name='CH')
        
        self.s_add = Address.objects.create() # Shipping
        self.s_add.name = 'TestName'
        self.s_add.address = 'address'
        self.s_add.city = 'city'
        self.s_add.zip_code = 'zip'
        self.s_add.state = 'state'
        self.s_add.country = self.country
        self.s_add.save()
        
        self.b_add = Address.objects.create() # Billing
        self.s_add.name = 'TestName'
        self.b_add.address = 'address'
        self.b_add.city = 'city'
        self.b_add.zip_code = 'zip'
        self.b_add.state = 'state'
        self.b_add.country = self.country
        self.b_add.save()
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')
        
    def check_order_address(self):
        order = self.order
        self.assertEqual(order.shipping_name, self.s_add.name)
        self.assertEqual(order.shipping_address, self.s_add.address)
        self.assertEqual(order.shipping_address2, self.s_add.address2)
        self.assertEqual(order.shipping_city, self.s_add.city)
        self.assertEqual(order.shipping_zip_code, self.s_add.zip_code)
        self.assertEqual(order.shipping_state, self.s_add.state)
        self.assertEqual(order.shipping_country, self.s_add.country.name)
        
        self.assertEqual(order.billing_name, self.b_add.name)
        self.assertEqual(order.billing_address, self.b_add.address)
        self.assertEqual(order.billing_address2, self.b_add.address2)
        self.assertEqual(order.billing_city, self.b_add.city)
        self.assertEqual(order.billing_zip_code, self.b_add.zip_code)
        self.assertEqual(order.billing_state, self.b_add.state)
        self.assertEqual(order.billing_country, self.b_add.country.name)
        
    def test_assigning_to_order_from_view_works(self):
        view = CheckoutSelectionView(request=self.request)
        view.save_addresses_to_order(self.order, self.s_add, self.b_add)
        
        self.check_order_address()
        
    def test_assigning_to_order_from_view_works_with_name_and_address(self):
        self.s_add.name = 'toto'
        self.s_add.address2 = 'address2'
        self.s_add.save()
        self.b_add.name = 'toto'
        self.b_add.address2 = 'address2'
        self.b_add.save()
        
        view = CheckoutSelectionView(request=self.request)
        view.save_addresses_to_order(self.order, self.s_add, self.b_add)
        
        self.check_order_address()


class CheckoutCartToOrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", 
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Toto")
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')

        self.cart = Cart()
        self.cart.user = self.user
        self.cart.save()

    def test_order_created(self):
        
        view = CheckoutSelectionView(request=self.request)
        res = view.create_order_object_from_cart()
        self.assertEqual(res.order_total, Decimal('0'))
