import pytest
from src.server_suivi import post_pos, get_list, post_list, get_pos, post_start, post_stop, post_pattern

markers_info = []

@pytest.mark.server_suivi
def post_pos_test():
    response = post_pos(100, 200, 45)
    assert (response.status_code == 401 or response.status_code == 200)
    print("[server_suivi] test_post_pos passed with status code:", response.status_code)

@pytest.mark.server_suivi
def get_list_test():
    balise_id = get_list()
    assert isinstance(balise_id, int), "Balise ID should be an integer"
    assert 5 <= balise_id <= 16, "Balise ID should be between 5 and 16"
    print("[server_suivi] test_get_list passed with balise id:", balise_id)

@pytest.mark.server_suivi
def post_list_test():
    balise_id = get_list()
    marker_info = next((m for m in markers_info if m[0] == balise_id), None)
    sect = marker_info[1] if marker_info else 'A'
    inner = marker_info[2] if marker_info else 1
    response = post_list(balise_id, sect, inner)
    assert (response.status_code == 401 or response.status_code == 200 or response.text == "Marker already captured") , "Post list should return status code 200 or 401"
    print("[server_suivi] test_post_list passed with status code:", response.status_code)

@pytest.mark.server_suivi
def get_pos_test():
    position = get_pos()
    assert isinstance(position, tuple), "Position should be a tuple"
    assert len(position) == 3, "Position tuple should have three elements"
    print("[server_suivi] test_get_pos passed with position:", position)

@pytest.mark.server_suivi
def post_start_test():
    reponse = post_pattern(1)
    assert (reponse.status_code == 401 or reponse.status_code == 200 or reponse.text == "Already started"), "Post pattern should return status code 200 or 401"
    reponse_json = reponse.json()
    for marker in reponse_json.get("markers", []):
        markers_info.append((marker["id"], marker["s"], marker["i"]))
    response = post_start()
    assert (response.status_code == 401 or response.status_code == 200 or response.text == "Already started"), "Post start should return status code 200 or 401 or Already started"
    print("[server_suivi] test_post_start passed with status code:", response.status_code)

@pytest.mark.server_suivi
def post_stop_test():
    response = post_stop()
    assert (response.status_code == 401 or response.status_code == 200)
    print("[server_suivi] test_post_stop passed with status code:", response.status_code)

if __name__ == "__main__":
    post_start_test()
    post_pos_test()
    get_list_test()
    post_list_test()
    get_pos_test()
    post_stop_test()