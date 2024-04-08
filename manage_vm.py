import subprocess

def get_vms_status():
    # Function to get the MAC address and status of a VM
    def get_vm_details(vm_name):
        result = subprocess.run(['VBoxManage', 'showvminfo', vm_name, '--machinereadable'], stdout=subprocess.PIPE)
        details = {'MAC_Address': None, 'Status': None}
        for line in result.stdout.decode('utf-8').split('\n'):
            if 'macaddress' in line:
                details['MAC_Address'] = line.split('=')[1].replace('"', '')
            if 'VMState=' in line:
                details['Status'] = line.split('=')[1].replace('"', '')
        return details

    # Get the list of all registered VM names and UUIDs
    vm_list = subprocess.run(['VBoxManage', 'list', 'vms'], stdout=subprocess.PIPE)
    vms_info = [line.split(' ') for line in vm_list.stdout.decode('utf-8').splitlines() if line]

    # Dictionary to store VM names, UUIDs, MAC addresses, and their statuses
    vms_data = {}

    # Loop through each VM info and get its details
    for vm_info in vms_info:
        vm_name = vm_info[0].strip('"')
        vm_uuid = vm_info[1].strip('{}')
        details = get_vm_details(vm_name)
        vms_data[vm_name] = {'UUID': vm_uuid, 'MAC_Address': details['MAC_Address'], 'Status': details['Status']}

    return vms_data, 0


def start_vm(target_mac_address):
    vms_data = get_vms_status()[0]
    ret = ""
    
    for vm_name, info in vms_data.items():
        if info['MAC_Address'] == target_mac_address:
            if info['Status'] == 'poweroff':
                # Start the VM if it's powered off
                subprocess.run(['VBoxManage', 'startvm', vm_name, '--type', 'headless'])
                ret = f"VM '{vm_name}' started."
                print(ret)
            elif info['Status'] == 'paused':
                # Resume the VM if it's paused
                subprocess.run(['VBoxManage', 'controlvm', vm_name, 'resume'])
                print(ret)
            else:
                ret = f"VM '{vm_name}' is already running."
                print(ret)
                return ret, 0 # TODO
            return ret, 0
    ret = "No VM with the provided MAC address found."
    return ret, 1


def pause_vm(target_mac_address):
    vms_data = get_vms_status()[0]
    ret = ""

    for vm_name, info in vms_data.items():
        if info['MAC_Address'] == target_mac_address:
            if info['Status'] == 'running':
                # Pause the VM if it's running
                subprocess.run(['VBoxManage', 'controlvm', vm_name, 'pause'])
                ret = f"VM '{vm_name}' paused."
                print(ret)
                return ret, 0
            else:
                ret = f"VM '{vm_name}' is not running, so it cannot be paused."
                print(ret)
                return ret, 0
    ret = "No VM with the provided MAC address found."
    print(ret)
    return ret , 1


def get_vm_status(target_mac_address):
    vms_data = get_vms_status()[0]

    for vm_name, info in vms_data.items():
        if info['MAC_Address'] == target_mac_address:
            # return f"VM '{vm_name}' status: {info['Status']}" , 0
            return info['Status'] , 0
    return "No VM with the provided MAC address found." , 1


def conv_mac(mac):
    if ":" in mac:
        mac = mac.replace(":", "")
    return mac.upper()
