from django.urls import reverse, resolve

def test_account_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('account-account')
    assert resolve(path).view_name == 'account-account'