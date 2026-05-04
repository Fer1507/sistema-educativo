import sys
import os
import unittest
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app, estudiantes


class TestSistemaEducativo(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_inicio(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        datos = json.loads(respuesta.data)
        self.assertEqual(datos["sistema"], "SistemaEducativo")

    def test_salud(self):
        respuesta = self.client.get("/salud")
        self.assertEqual(respuesta.status_code, 200)
        datos = json.loads(respuesta.data)
        self.assertEqual(datos["status"], "ok")

    def test_obtener_estudiantes(self):
        respuesta = self.client.get("/estudiantes")
        self.assertEqual(respuesta.status_code, 200)
        datos = json.loads(respuesta.data)
        self.assertIn("estudiantes", datos)
        self.assertIsInstance(datos["estudiantes"], list)

    def test_agregar_estudiante(self):
        nuevo = {"nombre": "Carlos Ruiz", "grado": "4to"}
        respuesta = self.client.post(
            "/estudiantes",
            data=json.dumps(nuevo),
            content_type="application/json"
        )
        self.assertEqual(respuesta.status_code, 201)
        datos = json.loads(respuesta.data)
        self.assertEqual(datos["nombre"], "Carlos Ruiz")
        self.assertEqual(datos["grado"], "4to")


if __name__ == "__main__":
    unittest.main()
