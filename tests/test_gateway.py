import unittest
from unittest.mock import patch, Mock
from flask import json
import requests
from gateway import app, discover_service_url

class GatewayTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('gateway.requests.request')
    def test_discover_service_url(self, mock_request):
        service_name = "test-service"
        expected_url = f'http://{service_name}-service.property-manager.svc.cluster.local'
        self.assertEqual(discover_service_url(service_name), expected_url)

    @patch('gateway.requests.request')
    def test_get_request(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = Mock()
        mock_response.content = b'{"message": "success"}'
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Realizar la solicitud GET simulada
        response = self.app.get('/test-service/test-path')
        
        # Verificar que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "success"}')
        self.assertEqual(response.content_type, 'application/json')

    @patch('gateway.requests.request')
    def test_post_request(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = Mock()
        mock_response.content = b'{"message": "created"}'
        mock_response.status_code = 201
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Realizar la solicitud POST simulada
        response = self.app.post('/test-service/test-path', json={"key": "value"})
        
        # Verificar que la respuesta sea la esperada
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, b'{"message": "created"}')
        self.assertEqual(response.content_type, 'application/json')

    @patch('gateway.requests.request')
    def test_put_request(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = Mock()
        mock_response.content = b'{"message": "updated"}'
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Realizar la solicitud PUT simulada
        response = self.app.put('/test-service/test-path', json={"key": "value"})
        
        # Verificar que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "updated"}')
        self.assertEqual(response.content_type, 'application/json')

    @patch('gateway.requests.request')
    def test_delete_request(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = Mock()
        mock_response.content = b'{"message": "deleted"}'
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Realizar la solicitud DELETE simulada
        response = self.app.delete('/test-service/test-path')
        
        # Verificar que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "deleted"}')
        self.assertEqual(response.content_type, 'application/json')

    @patch('gateway.requests.request')
    def test_request_exception(self, mock_request):
        # Configurar el mock para lanzar una excepción
        mock_request.side_effect = requests.exceptions.RequestException("Error")

        # Realizar la solicitud GET simulada
        response = self.app.get('/test-service/test-path')
        
        # Verificar que la respuesta maneje correctamente la excepción
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("Error al realizar la solicitud al servicio", data["error"])

if __name__ == '__main__':
    unittest.main()
