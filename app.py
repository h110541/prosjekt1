from flask import Flask
from flask import request
import data
import iperf

app = Flask(__name__)


@app.route("/api/hosts")
def hosts():
    return data.hosts


@app.route("/api/network-tests")
def network_tests():
    return data.network_test_results


@app.route("/api/network-tests/<test_id>")
def network_test(test_id):
    return data.network_test_results.get(test_id, None)


@app.post("/api/start-new-test")
def start_new_test():
    host = request.json["host"]
    test_id = iperf.create_new_test(host, data.network_test_results)
    return {"test_id": test_id}
