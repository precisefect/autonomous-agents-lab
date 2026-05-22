"""Basic unit tests for the agent template."""

import unittest

from fastapi.testclient import TestClient

from app.models.model import DummyModel
from app.services.agent_service import run_agent
from main import app


class TestHealthEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_returns_healthy(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "healthy")


class TestPredictEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_predict_returns_prediction(self) -> None:
        payload = {"data": {"temperature": 72.5, "pressure": 14.2}}
        response = self.client.post("/api/v1/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("prediction", body)
        self.assertEqual(body["status"], "success")


class TestDummyModel(unittest.TestCase):
    def test_predict_empty_data(self) -> None:
        model = DummyModel()
        self.assertEqual(model.predict({}), 0.0)

    def test_run_agent_mock(self) -> None:
        result = run_agent({"vibration": 0.12, "rpm": 1800})
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["prediction"], float)


if __name__ == "__main__":
    unittest.main()
