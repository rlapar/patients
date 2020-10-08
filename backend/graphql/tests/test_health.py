def test_ping(client):
    response = client.get('/graphql/ping')
    assert response.status_code == 200
    assert response.json == {'status': 'pong'}
