from fastapi.testclient import TestClient

from truck_agent.main import app

client = TestClient(app)

def test_sample_decide_request():
    """
    Use this test to check if the truck_agent is working correctly.
    Of course, when you change the agent, you should also change this test.
    """
    payload = open("tests/sample_decide_0.json", "r").read()
    response = client.post(
        "/decide",
        headers={"Content-Type": "application/json"},
        data=payload,
    )
    assert response.status_code == 200
    assert response.json() == {
        "command": "DELIVER",
        "argument": "100",
    }
