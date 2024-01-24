import subprocess
import uuid
import json
from threading import Thread


def run_iperf(host):
    iperf_result = subprocess.run(['iperf3', '-c', host, '--json'], capture_output=True)
    iperf_stdout = iperf_result.stdout.decode('utf-8', errors='ignore')
    return iperf_stdout


def thread_function(host, test_id, results_dict):
    iperf_stdout = run_iperf(host)
    result = json.loads(iperf_stdout)
    results_dict[test_id]['result'] = result
    results_dict[test_id]['status'] = 'finished'


def create_new_test(host, results_dict):
    test_id = str(uuid.uuid4())
    results_dict[test_id] = {'host': host, 'id': test_id, 'status': 'running'}
    Thread(target=thread_function, args=(host, test_id, results_dict)).start()
    return test_id
