from django.urls import reverse, resolve

def test_search_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('search-search')
    assert resolve(path).view_name == 'search-search'

def test_results_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('search-results')
    assert resolve(path).view_name == 'search-results'