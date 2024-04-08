from flask import Flask, jsonify
import manage_vm  # make sure this file is in the same directory as your server script
from manage_vm import conv_mac

app = Flask(__name__)

@app.route('/status/<mac>', methods=['GET'])
def get_vm_status(mac):
    status, _ = manage_vm.get_vm_status(conv_mac(mac))
    if _:
        return jsonify({'status': status}), 404
    print(status)
    if status == "paused" or status == "poweroff":
        return status, 406
    elif status == "running":
        return status, 200
    return jsonify({'status': status}), 405

@app.route('/pause/<mac>', methods=['GET'])
def pause_vm(mac):
    result = manage_vm.pause_vm(conv_mac(mac))
    return jsonify({'result': result}), 200

@app.route('/start/<mac>', methods=['GET'])
def start_vm(mac):
    result = manage_vm.start_vm(conv_mac(mac))
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
    # app.run(debug=True, host="0.0.0.0")

