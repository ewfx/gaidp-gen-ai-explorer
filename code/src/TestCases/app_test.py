import unittest
import json
import os
from flask import Flask
from app import app  # Importing the Flask app
from io import BytesIO


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_upload_file_page(self):
        response = self.app.get('/upload_file')
        self.assertEqual(response.status_code, 200)

    def test_new_rule(self):
        response = self.app.get('/new_rule')
        self.assertEqual(response.status_code, 200)

    def test_chatbot(self):
        response = self.app.get('/chatbot')
        self.assertEqual(response.status_code, 200)

    def test_data_with_rules(self):
        response = self.app.get('/datawithrules.html')
        self.assertEqual(response.status_code, 200)

    def test_data_rules(self):
        response = self.app.get('/data_rules')
        self.assertEqual(response.status_code, 200)

    def test_upload_invalid_file(self):
        response = self.app.post('/upload', data={})
        self.assertEqual(response.status_code, 400)

    def test_upload_no_file_selected(self):
        data = {'file': (BytesIO(b""), '')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_get_data_no_file(self):
        response = self.app.get('/data', query_string={"file": "nonexistent.xlsx"})
        self.assertEqual(response.status_code, 200)

    def test_get_excel_templates(self):
        response = self.app.get('/get-excel-templates')
        self.assertEqual(response.status_code, 200)

    def test_get_rules_no_file(self):
        response = self.app.get('/get-rules', query_string={"file": "nonexistent.xlsx"})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
