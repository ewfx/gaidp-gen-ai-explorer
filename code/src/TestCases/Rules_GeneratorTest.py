import pytest
import json
import os
from flask import Flask
from app import app  # Import your Flask app

def test_generate_rules_file_not_found(client):
    response = client.post("/generate_rules", json={"ruleCount": 5, "excelTemplate": "non_existent.xlsx"})
    assert response.status_code == 400
    assert "File not found" in response.json["error"]

def test_generate_rules_success(client, mocker):
    mocker.patch("app.get_excel_data", return_value=(["col1", "col2"], [{"col1": "data1", "col2": "data2"}]))
    mocker.patch("app.generate_rules_gemini", return_value=[{"Rule Name": "Rule 1", "Description": "Description 1"}])
    response = client.post("/generate_rules", json={"ruleCount": 5, "excelTemplate": "test.xlsx"})
    assert response.status_code == 200
    assert response.json["rules_count"] == 1

def test_filter_data_no_file(client):
    response = client.get("/filter_data?file=")
    assert response.status_code == 400
    assert "No file provided" in response.json["error"]

def test_filter_data_file_not_found(client):
    response = client.get("/filter_data?file=non_existent.xlsx")
    assert response.status_code == 400
    assert "File not found" in response.json["error"]

def test_filter_data_no_rules(client, mocker):
    mocker.patch("pandas.read_excel", side_effect=ValueError("Sheet not found"))
    response = client.get("/filter_data?file=test.xlsx")
    assert response.status_code == 400
    assert "Please generate rules first." in response.json["error"]

def test_filter_excel_file_not_found(client):
    response = client.get("/filter-excel1?file=non_existent.xlsx")
    assert response.status_code == 400
    assert "Please generate rules first." in response.json["error"]

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client