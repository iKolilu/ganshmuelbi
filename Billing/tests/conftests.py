# Third party modules
import pytest

# First party modules
from Billing import create_app

import db
# import tempfile



@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# @pytest.fixture(scope="session")
# def db_handle():
#    app = create_app() 
#    app.config["TESTING"] = True
#    with app.app_context():
#         app.db.create_all()
        
#    yield app.db
