from django.urls import reverse, resolve

def test_legals_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('legals-legals')
    assert resolve(path).view_name == 'legals-legals'