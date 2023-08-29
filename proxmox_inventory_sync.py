#!/usr/bin/env python3
from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth


def get_proxmox_nodes(proxmox_api_url, proxmox_token):
    # Get list of Proxmox nodes with tags
    headers = {
        "Authorization": f"Bearer {proxmox_token}",
    }
    response = requests.get(
        f"{proxmox_api_url}/nodes",
        headers=headers,
        verify=False
    )
    response.raise_for_status()
    nodes = response.json().get("data")

    return nodes


def generate_inventory(proxmox_api_url, proxmox_token):
    inventory = {
        "_meta": {
            "hostvars": {}
        }
    }

    nodes = get_proxmox_nodes(proxmox_api_url, proxmox_token)

    for node in nodes:
        hostname = node.get("node")
        tags = node.get("tags", "").split(",")

        for tag in tags:
            inventory.setdefault(tag, []).append(hostname)

        # Add host variables (optional)
        hostvars = {
            "ansible_host": node.get("ip"),
            "ansible_user": "your_ssh_username",
            "ansible_ssh_private_key_file": "your_private_key_path",
        }
        inventory["_meta"]["hostvars"][hostname] = hostvars

    return inventory


def main():
    module_args = dict(
        inventory_id=dict(type='int', required=True),
        proxmox_api_url=dict(type='str', required=True),
        proxmox_token=dict(type='str', required=True, no_log=True),
        awx_api_url=dict(type='str', required=True),
        awx_username=dict(type='str', required=True),
        awx_password=dict(type='str', required=True, no_log=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    inventory_id = module.params['inventory_id']
    proxmox_api_url = module.params['proxmox_api_url']
    proxmox_token = module.params['proxmox_token']
    awx_api_url = module.params['awx_api_url']
    awx_username = module.params['awx_username']
    awx_password = module.params['awx_password']

    # Update AWX inventory
    try:
        inventory = generate_inventory(proxmox_api_url, proxmox_token)
        inventory_json = module.jsonify(inventory)

        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "name": "Proxmox Inventory",
            "variables": inventory_json,
        }
        response = requests.put(
            f"{awx_api_url}/inventories/{inventory_id}",
            auth=HTTPBasicAuth(awx_username, awx_password),
            headers=headers,
            json=data,
            verify=False
        )
        response.raise_for_status()
        module.exit_json(changed=True, msg="Inventory updated successfully!")
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to update inventory: {str(e)}")


if __name__ == '__main__':
    main()
