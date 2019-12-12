from django.test import SimpleTestCase
from django.urls import reverse, resolve
from legals.views import legals


class TestUrls(SimpleTestCase):

    
    def test_legals_name_is_reversed_and_resolved(self):
        """
            Check if the name of url is linked to the
            correct path. And if the correct template is returned
        """
        url = reverse("legals-legals")
        # Name linked to url
        self.assertEqual(resolve(url).view_name, 'legals-legals')
        # Url linked to the correct view function
        self.assertEqual(resolve(url).func, legals)