from flask import Flask
from flask import request
import data
import iperf

app = Flask(__name__)


@app.route("/api/servers")
def hosts():
    return data.servers


@app.route("/api/network-tests")
def network_tests():
    return data.iperf_results


@app.route("/api/network-tests/<test_id>")
def network_test(test_id):
    try:
        return data.iperf_results[test_id]
    except KeyError:
        return {
            "id": test_id,
            "status": "failed",
            "failure_type": "No test with supplied ID found"
        }


@app.route("/api/network-tests-list")
def network_tests_list():
    l = [{'id': x['id'], 'created': x['created'], 'status': x['status']} for x in data.iperf_results.values()]
    return sorted(l, key=lambda x: x['created'], reverse=True)


@app.post("/api/start-new-test")
def start_new_test():
    host = request.json["host"]
    port = request.json["port"]
    test_id = iperf.create_new_test(host, port, data.iperf_results)
    return {"test_id": test_id}
