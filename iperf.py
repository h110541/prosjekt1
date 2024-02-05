import subprocess
import uuid
import json
from datetime import datetime
from threading import Thread


def thread_function(host, port, test_id, results_dict):
    try:
        iperf_result = subprocess.run(['iperf3', '-c', host, '-p', str(port), '--json'], capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        results_dict[test_id]['failure_type'] = 'timeout'
        results_dict[test_id]['status'] = 'failed'
    else:
        iperf_stdout = iperf_result.stdout.decode('utf-8', errors='ignore')
        result = json.loads(iperf_stdout)
        results_dict[test_id]['result'] = result

        if iperf_result.returncode == 0:
            results_dict[test_id]['status'] = 'finished'
        else:
            results_dict[test_id]['failure_type'] = 'non-zero exit code'
            results_dict[test_id]['status'] = 'failed'


def create_new_test(host, port, results_dict):
    test_id = str(uuid.uuid4())
    results_dict[test_id] = {'host': host, 'id': test_id, 'status': 'running', 'created': datetime.now()}
    Thread(target=thread_function, args=(host, port, test_id, results_dict)).start()
    return test_id
