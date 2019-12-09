from django.urls import reverse, resolve

def test_signup_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('signup')
    assert resolve(path).view_name == 'signup'