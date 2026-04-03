import pytest
from fastapi import status
from db.enums import UserRole

def test_get_user_by_id_as_admin(client, admin_user, regular_user):
    target_user_id = regular_user["user"].id
    response = client.get(
        f"/users/{target_user_id}",
        headers=admin_user["headers"]
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == regular_user["user"].username

def test_get_user_by_id_as_viewer_fails(client, regular_user):
    target_user_id = regular_user["user"].id
    response = client.get(
        f"/users/{target_user_id}",
        headers=regular_user["headers"]
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_admin_update_user_role(client, admin_user, regular_user):
    target_user_id = regular_user["user"].id
    response = client.patch(
        f"/users/{target_user_id}?role={UserRole.ANALYST.value}",
        headers=admin_user["headers"]
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["updated_fields"]["role"] == UserRole.ANALYST.value

def test_admin_cannot_update_own_role(client, admin_user):
    admin_id = admin_user["user"].id
    response = client.patch(
        f"/users/{admin_id}?role={UserRole.VIEWER.value}",
        headers=admin_user["headers"]
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Admins cannot modify their own role" in response.json()["detail"]
