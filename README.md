Documentation for the module:

______________________________________________________________________

## Ansible Module: Proxmox Tag-based Inventory Sync

This Ansible module allows you to synchronize the inventory in Ansible Tower/AWX with a Proxmox cluster based on tags associated with Proxmox nodes. It retrieves the tags from Proxmox and dynamically generates inventory groups in Ansible Tower/AWX based on those tags.

### Module Parameters

- `inventory_id` (required): The ID of the inventory in Ansible Tower/AWX to be updated.
- `proxmox_api_url` (required): The URL of the Proxmox API.
- `proxmox_username` (required): The username to authenticate with the Proxmox API.
- `proxmox_password` (required): The password to authenticate with the Proxmox API.
- `awx_api_url` (required): The URL of the Ansible Tower/AWX API.
- `awx_username` (required): The username to authenticate with the Ansible Tower/AWX API.
- `awx_password` (required): The password to authenticate with the Ansible Tower/AWX API.

### Usage Example

```yaml
- name: Sync Proxmox inventory with Ansible Tower
  proxmox_inventory_sync:
    inventory_id: 1
    proxmox_api_url: "https://proxmox.example.com/api2"
    proxmox_username: "admin"
    proxmox_password: "secret"
    awx_api_url: "https://awx.example.com/api/v2"
    awx_username: "admin"
    awx_password: "secret"
```

### How it Works

1. The module authenticates with the Proxmox API using the provided username and password.
1. It retrieves the list of Proxmox nodes along with their associated tags.
1. Based on the tags, the module generates inventory groups in Ansible Tower/AWX.
1. Each Proxmox node is added to the corresponding inventory group based on its tags.
1. The module also allows you to specify additional host variables for each Proxmox node (e.g., SSH credentials).
1. The updated inventory is sent to Ansible Tower/AWX API, and the inventory in Ansible Tower/AWX is updated.

### Notes

- The module assumes that the tags in Proxmox correspond to Ansible group names. For example, if a Proxmox node has a tag "web_servers", it will be added to the Ansible group "web_servers" in the inventory.
- Make sure to provide the correct API URLs and authentication credentials for both Proxmox and Ansible Tower/AWX.
- The module uses the `requests` library to interact with the Proxmox and Ansible Tower/AWX APIs.
- Ensure that the `requests` library is installed on the machine where you run the playbook containing this module.
- The module requires the `ansible.module_utils.basic` module and the `AnsibleModule` class for proper integration with Ansible.

### Limitations

- The module assumes a one-to-one mapping between Proxmox nodes and Ansible hosts. If you have a more complex inventory structure, additional customization may be required.
- The module does not handle the deletion of inventory groups or hosts that are no longer present in Proxmox. It only adds or updates existing inventory groups and hosts.

### Support

______________________________________________________________________

Feel free to customize the documentation to fit your specific needs. This example provides an overview of the module, its parameters, usage example, and important notes and limitations.
