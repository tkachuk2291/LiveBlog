from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class PrivateHomePageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        self.client.force_login(user)
        self.res = self.client.get(reverse("taxi:home-page-main"))

    def test_private_homepage_test(self):
        self.assertEquals(self.res.status_code, 200)

#
# class PublicHomePageTest(TestCase):
#     def setUp(self):
#         self.res = self.client.get(reverse("taxi:index"))
#
#     def test_public_home_page(self):
#         self.assertNotEquals(self.res.status_code, 200)
#
#
# class IndexViewTest(TestCase):
#     def setUp(self):
#         driver_test = get_user_model().objects.create_user(
#             username="Anton", password="tiguti26", license_number="NO55555"
#         )
#
#         manufacturer_test = Manufacturer.objects.create(
#             name="test_Manufacturer", country="test_Country"
#         )
#         self.car = Car.objects.create(
#             model="test_Model",
#             manufacturer=manufacturer_test,
#         )
#         self.car.drivers.add(driver_test)
#         self.client.force_login(driver_test)
#         self.response = self.client.get(
#             reverse("taxi:index")
#         )