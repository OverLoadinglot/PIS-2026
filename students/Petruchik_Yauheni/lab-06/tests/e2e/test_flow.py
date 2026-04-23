from fastapi.testclient import TestClient

from src.infrastructure.adapter.in_bound.budget_controller import app, repository


def test_create_budget_and_get_it():
    client = TestClient(app)
    response = client.post('/budgets/b49', json={'budget_id': 'b49', 'name': 'Про рубли'})
    assert response.status_code == 200
    data = response.json()
    assert data['budget_id'] == 'b49'
    assert data['name'] == 'Про рубли'

    response = client.get('/budgets/b49')
    assert response.status_code == 200
    data = response.json()
    assert data['budget_id'] == 'b49'
    assert data['name'] == 'Про рубли'
