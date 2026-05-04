from flask import Flask, jsonify, request

app = Flask(__name__)

estudiantes = [
    {"id": 1, "nombre": "Ana Torres", "grado": "5to"},
    {"id": 2, "nombre": "Luis Pérez", "grado": "3ro"},
]

@app.route("/")
def inicio():
    return jsonify({
        "sistema": "SistemaEducativo",
        "empresa": "EduTech Solutions S.A.C.",
        "version": "1.0.0",
        "estado": "activo"
    })

@app.route("/salud")
def salud():
    return jsonify({"status": "ok"})

@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    return jsonify({"estudiantes": estudiantes, "total": len(estudiantes)})

@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    datos = request.get_json()
    if not datos or "nombre" not in datos or "grado" not in datos:
        return jsonify({"error": "Se requieren nombre y grado"}), 400
    nuevo = {
        "id": len(estudiantes) + 1,
        "nombre": datos["nombre"],
        "grado": datos["grado"]
    }
    estudiantes.append(nuevo)
    return jsonify(nuevo), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
