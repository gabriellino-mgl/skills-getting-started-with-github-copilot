def test_root_redirect(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert isinstance(payload[expected_activity], dict)


def test_signup_for_activity_adds_new_email(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_email} for {activity_name}"


def test_signup_for_activity_with_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{existing_email}"
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Removed {existing_email} from {activity_name}"


def test_remove_nonexistent_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{missing_email}"
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Participant not found in this activity"


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_remove_from_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
