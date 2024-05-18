from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLUSTER_LOCAL_SUFFIX = '.property-manager.svc.cluster.local'

def discover_service_url(service_name):
    return f'http://{service_name}-service{CLUSTER_LOCAL_SUFFIX}'

@app.route('/<service>/', defaults={'path': ''})
@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service, path):
    service_url = discover_service_url(service)
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
    app.run(debug=True, port=5000)
