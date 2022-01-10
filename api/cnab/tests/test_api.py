from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from tests.mocks import OpenMock, IOMock
from core import models
from cnab.settings import PROCESS_AREA


class APIViewCNABDocumentation(TestCase):
    def setUp(self):
        self.cnab_documentation = models.CNABDocumentation.objects.create(
            type=1,
            date="2022-10-12",
            value=300,
            cpf="99999999999",
            card="3123****7687",
            store_owner="test",
            store_name="Test store"
        )
        self.client = APIClient()
    
    def test_get(self):
        resp = self.client.get("/api/cnab-documentation/")
        data = resp.json()

        self.assertTrue(len(data) == 1)
        self.assertEqual(data[0]['id'], str(self.cnab_documentation.id))
    
    def test_get_id(self):
        resp = self.client.get(f"/api/cnab-documentation/{self.cnab_documentation.id}/")
        self.assertEqual(resp.status_code, 200)


class APIStoreTest(TestCase):
    def setUp(self):
        self.store = models.Store.objects.create(
            name="Test",
            owner="Test owner",
            balance=200
        )
        self.client = APIClient()
    
    def test_get(self):
        resp = self.client.get("/api/store/")
        data = resp.json()

        self.assertTrue(len(data) == 1)
        self.assertEqual(data[0]['id'], str(self.store.id))
    
    def test_get_id(self):
        resp = self.client.get(f"/api/store/{self.store.id}/")
        self.assertEqual(resp.status_code, 200)


class APIViewFileTest(TestCase):
    def setUp(self):
        self.file = models.File.objects.create(
            filepath="test"
        )
        self.client = APIClient()
    
    @patch("core.views.send_to_worker")
    @patch("core.views.open", return_value=OpenMock())
    @patch.object(IOMock, "write")
    def test_post(self, mock_io, mock_open, mock_send_to_worker):
        with open("tests/fixtures/cnab.txt") as f:
            resp = self.client.post(
                "/api/file/",
                data={
                    "file": f
                },
                format="multipart"
            )
        
        mock_open.assert_called_with(f"{PROCESS_AREA}/cnab.txt", "wb")
        mock_io.assert_called()
        mock_send_to_worker.assert_called()
        self.assertEqual(resp.status_code, 201)

    def test_post_fail(self):
        with open("tests/fixtures/cnab.txt") as f:
            resp = self.client.post(
                "/api/file/",
                data={},
                format="multipart"
            )
        self.assertEqual(resp.status_code, 400)
    
    def test_get(self):
        resp = self.client.get("/api/file/")
        data = resp.json()

        self.assertTrue(len(data) == 1)
        self.assertEqual(data[0]['id'], str(self.file.id))        
