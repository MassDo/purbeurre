from django.urls import reverse, resolve

def test_login_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('login')
    assert resolve(path).view_name == 'login'

def test_logout_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('logout')
    assert resolve(path).view_name == 'logout'