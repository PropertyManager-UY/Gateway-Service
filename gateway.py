from flask import Flask, request, jsonify
import requests
from kubernetes import client, config
import os

app = Flask(__name__)

# Determinar si estamos dentro de un pod de Kubernetes
def is_running_in_kubernetes():
    return os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token')

if is_running_in_kubernetes():
    config.load_incluster_config()  # Usar esta línea si la aplicación corre dentro de un pod
else:
    config.load_kube_config()  # Usar esta línea si corres la aplicación localmente con kubeconfig

v1 = client.CoreV1Api()
NAMESPACE = 'property-manager'

def discover_service_url(service_name):
    try:
        service = v1.read_namespaced_service(service_name + '-service', NAMESPACE)
        port = service.spec.ports[0].port
        return f'http://{service_name}-service.{NAMESPACE}.svc.cluster.local:{port}'
    except client.exceptions.ApiException as e:
        print(f"Error al obtener el servicio: {e}")
        return None

@app.route('/<service>/', defaults={'path': ''})
@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service, path):
    service_url = discover_service_url(service)
    if not service_url:
        return jsonify({"error": "Servicio no encontrado"}), 404

    destination_url = f"{service_url}/{path}"

    method = request.method
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_json() if request.is_json else request.form

    try:
        response = requests.request(method, destination_url, headers=headers, json=data)
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al realizar la solicitud al servicio: {e}"}), 500

@app.route('/help', methods=['GET'])
def list_services():
    try:
        services = v1.list_namespaced_service(NAMESPACE)
        service_list = []
        for svc in services.items:
            service_name = svc.metadata.name
            ports = [port.port for port in svc.spec.ports]
            service_list.append({"name": service_name, "ports": ports})
        return jsonify(service_list)
    except client.exceptions.ApiException as e:
        return jsonify({"error": f"Error al obtener la lista de servicios: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
