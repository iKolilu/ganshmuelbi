import pytest

from ...db import  get_provider, create_provider



def test_get_provider():
    """
      Testing  User Data Exists
    """


    
    new_user=None    
    new_user=get_provider(65)


    assert new_user is not None
    assert new_user == "Not implemented"
    # assert new_user == "Not implemented here "
    
    



def test_create_provider():
    """
      Testing  User Data Exists
    """

    
    print("####Started tests########")
    new_user=None    

    test_name="kofi"
    new_user=create_provider(test_name)



    assert new_user is not None

    assert new_user.id == 1001