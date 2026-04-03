import pytest
from fastapi import status
from db.enums import TransactionType, TransactionCategory

def test_create_record_as_admin(client, admin_user):
    payload = {
        "amount": 100.50,
        "type": TransactionType.INCOME,
        "category": TransactionCategory.SALARY,
        "description": "Monthly Salary"
    }
    response = client.post(
        "/records",
        json=payload,
        headers=admin_user["headers"]
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "record added successfully"
    assert response.json()["details"]["amount"] == 100.50

def test_viewer_cannot_create_record(client, regular_user):
    payload = {
        "amount": 50.0,
        "type": TransactionType.EXPENSE,
        "category": TransactionCategory.FOOD,
        "description": "Lunch"
    }
    response = client.post(
        "/records",
        json=payload,
        headers=regular_user["headers"]
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_list_records(client, admin_user):
    # Add a record first
    client.post(
        "/records",
        json={
            "amount": 10.0,
            "type": TransactionType.EXPENSE,
            "category": TransactionCategory.SHOPPING,
            "description": "New shirt"
        },
        headers=admin_user["headers"]
    )
    
    response = client.get("/records", headers=admin_user["headers"])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] >= 1
    assert any(r["description"] == "New shirt" for r in response.json()["details"])

def test_delete_record_as_admin(client, admin_user):
    # Create a record
    create_res = client.post(
        "/records",
        json={
            "amount": 20.0,
            "type": TransactionType.EXPENSE,
            "category": TransactionCategory.OTHER,
            "description": "Temporary record"
        },
        headers=admin_user["headers"]
    )
    # Get record id
    # Note: The response structure for create_record doesn't return the ID right now according to routers/records.py
    # but list_records does.
    list_res = client.get("/records", headers=admin_user["headers"])
    record_id = list_res.json()["details"][0]["id"]
    
    # Delete it
    del_res = client.delete(f"/records/{record_id}", headers=admin_user["headers"])
    assert del_res.status_code == status.HTTP_200_OK
    assert del_res.json()["deleted_id"] == record_id
