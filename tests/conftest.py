import json

import pytest
from falcon import testing

from piri_web.app import application


@pytest.fixture(scope='session')
def client():
    """Create a Testing client."""
    return testing.TestClient(application)


@pytest.fixture(scope='session')
def configuration():
    """Load json configuration."""
    config_data = {}
    with open('tests/config.json') as config_file:
        config_data = json.load(config_file)

    return config_data
