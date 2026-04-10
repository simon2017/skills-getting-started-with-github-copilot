from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app, follow_redirects=False)


def test_root_redirect():
    """Test that root endpoint redirects to static index.html"""
    # Arrange - TestClient is set up

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """Test getting all activities"""
    # Arrange - Activities are predefined in app

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]


def test_signup_activity_not_found():
    """Test signup for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up():
    """Test signup when student is already signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_delete_signup_success():
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity_name}" in data["message"]


def test_delete_signup_activity_not_found():
    """Test unregister from non-existent activity"""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_delete_signup_not_signed_up():
    """Test unregister when student is not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]