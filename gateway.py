import socket
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Determinar si estamos dentro de un pod de Kubernetes
def is_running_in_kubernetes():
    return os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token')

def get_local_hostnames():
    with open('/etc/hosts', 'r') as f:
        return [line.split()[1] for line in f if line.strip().endswith('.local')]

def discover_service_url(service_name):
    if is_running_in_kubernetes():
        try:
            socket.gethostbyname(f'{service_name}-service')
            return f'http://{service_name}-service.property-manager.svc.cluster.local'
        except socket.gaierror:
            pass
    else:
        local_hostnames = get_local_hostnames()
        for hostname in local_hostnames:
            if hostname.startswith(service_name + ".local"):
                try:
                    ip_address = socket.gethostbyname(hostname)
                    if ip_address == '127.0.0.1' or ip_address == '::1':
                        return f'http://{hostname}:5000'  # Assumiendo que cada servicio corre en el puerto 5000
                except socket.gaierror:
                    pass
    return None

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service, path=''):
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
