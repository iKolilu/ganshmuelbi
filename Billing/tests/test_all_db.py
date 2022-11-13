import pytest



from db import get_provider, create_provider, connect, clear_provider_table, clear_a_record_provider_table

connection=connect()


def test_get_provider():
    """
    Testing User Data Exists
    """



    new_user=None 
    new_user=get_provider(connection, "DonSimonk")


    assert new_user is  None
    # assert new_user == "Not implemented"

    # assert "a"=="b" is True
    # assert new_user == "Not implemented here "





def test_create_provider():
    """
    Testing User Data Exists
    """


    print("####Started tests########")
    new_user=None 
    clear_a_record_provider_table(connection)

    test_name="kofi"
    new_user=create_provider(connection,test_name)



    assert new_user is not None

    assert new_user == 10001


    print("######### . Record inserted, Database Test Passed ############") 