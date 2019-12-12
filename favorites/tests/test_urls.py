from django.test import SimpleTestCase
from django.urls import reverse, resolve
from favorites.views import favorites


class TestUrls(SimpleTestCase):

    
    def test_favorites_name_is_reversed_and_resolved(self):
        """
            Check if the name of url is linked to the
            correct path. And if the correct template is returned
        """
        url = reverse("favorites-favorites")
        # name linked to url
        self.assertEqual(resolve(url).view_name, 'favorites-favorites')
        # url linked to the correct view function
        self.assertEqual(resolve(url).func, favorites)