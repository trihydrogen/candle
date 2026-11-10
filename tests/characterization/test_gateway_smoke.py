import httpx
import pytest


@pytest.mark.characterization
def test_gateway_responds(client: httpx.Client) -> None:
    response = client.get("/")
    assert response.status_code < 500


@pytest.mark.characterization
def test_seeded_room_timetable(client: httpx.Client) -> None:
    response = client.get("/miestnosti/F1-248")
    assert response.status_code == 200
    assert "F1-248" in response.text
