import pytest
from mixer.backend.django import mixer

# need to test the 2 manager methods: 
    # best_product(user_input):
        # fixture parametrise for diff prod
        # if no items in database ?
        
    # favorites_products(user_logged)
        # if the user have 3 prod return querysetlen 3
        # if no titem return none ?
        # if no items in database ?

# def test_favorites_products():
#     """
#         if the user have 3 prod return querysetlen 3
#         if no titem return none ?
#         if no items in database ?
#     """
#     user = mixer.blend(User)
