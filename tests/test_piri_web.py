import json

import falcon


def test_get_schema(client):
    """Test that we get json data back on 'GET'."""
    response = client.simulate_get('/')

    assert response.status == falcon.HTTP_OK
    assert response.headers.get('content-type') == falcon.MEDIA_JSON
    assert response.json


def test_post_map(client, configuration):
    """Test that we can map data."""
    json_data = {
        'configuration': configuration,
        'data': {
            'key': 'val1',
            'key2': 'val2',
            'a1': 'a1',
            'a2': 'a2',
            'persons': [{'name': 'john'}, {'name': 'bob'}],
            'extra': {
                'extra1': 'extra1val',
                'extra2': 'extra2val',
            },
        },
    }
    expected_result = {
        'name': 'default2',
        'address': {
            'address1': 'a1',
            'address2': 'a2',
        },
        'people': [
            {'firstname': 'john'},
            {'firstname': 'bob'},
        ],
        'extrafield': [
            {'dataname': 'one', 'datavalue': 'extra1val'},
            {'dataname': 'two', 'datavalue': 'extra2val'},
        ],
    }

    response = client.simulate_post(
        body=json.dumps(json_data),
    )

    assert response.status == falcon.HTTP_OK
    assert response.headers.get('content-type') == falcon.MEDIA_JSON
    assert response.json == expected_result


def test_post_empty_data_map(client):
    """Test no payload is bad request."""
    response = client.simulate_post()

    assert response.status == falcon.HTTP_BAD_REQUEST
    assert response.headers.get('content-type') == falcon.MEDIA_JSON
