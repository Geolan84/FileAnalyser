from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_uncompleted_search(mocker):
    mocker.patch(
        'search_repository.SearchRepository.get_search_result', return_value=(False,))
    response = client.get("/searches/21c54b3e-98ad-428e-a1fd-6a7de2d0138b")
    assert response.status_code == 200
    assert response.json() == {"finished": False}


def test_get_completed_empty_search(mocker):
    mocker.patch(
        'search_repository.SearchRepository.get_search_result', return_value=(True, []))
    response = client.get("/searches/21c54b3e-98ad-428e-a1fd-6a7de2d0138b")
    assert response.status_code == 200
    assert response.json() == {"finished": True, "paths": []}


def test_get_completed_search(mocker):
    mocker.patch('search_repository.SearchRepository.get_search_result', return_value=(
        True, ["C:\\Users\\lanin\\Downloads\\Test\\test1.jpg"]))
    response = client.get("/searches/21c54b3e-98ad-428e-a1fd-6a7de2d0138b")
    assert response.status_code == 200
    assert response.json() == {"finished": True, "paths": [
        "C:\\Users\\lanin\\Downloads\\Test\\test1.jpg"]}


def test_get_nonexistent_search(mocker):
    mocker.patch('search_repository.SearchRepository.get_search_result',
                 side_effect=ValueError())
    response = client.get("/searches/21c54b3e-98ad-428e-a1fd-6a7de2d0138b")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No record with id 21c54b3e-98ad-428e-a1fd-6a7de2d0138b in history!"}


def test_create_search(mocker):
    mocker.patch('search_repository.SearchRepository.search_files',
                 return_value="21c54b3e-98ad-428e-a1fd-6a7de2d0138b")
    mocker.patch('sys.argv', return_value=['main.py'])
    response = client.post("/search",  json={})
    assert response.status_code == 523
    assert response.json() == {
        "detail": "Specify directory! - 'python main.py directory_name'"}
