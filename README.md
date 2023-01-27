# Containerlab BGP Labs using CSR1000v

This is a repository that I am creating to teach myself unit testing, portable infrastructure as code, configuration management and labbing content for the Cisco ENCOR Exam. I have provided all necessary files to complete the lab ***except*** for the Cisco CSR 1000v image. You must obtain your own Cisco CSR 1000v image legally via Cisco. After obtaining your image you can use the [vrnetlab](https://containerlab.dev/manual/vrnetlab/) project to containerize it for [Containerlab](https://containerlab.dev/manual/kinds/vr-csr/).

## Capabilities

*Testing*, *IaC*, *Configuration Management*, *Labs*, *Secret Management*

<table>
  <tr>
    <th>Testing</th>
    <th>IaC</th>
    <th>Configuration Management</th>
    <th>Labs</th>
    <th>Secrets</th>
  </tr>
  <tr>
    <td>Feel free to use this repository to perform your own testing. I've also included an example of unit testing to accomplish pre-lab deployment checks as necessary. </td>
    <td>I am using ContainerLab to serve as my Infrastructure as Code (IaC) orchestrator, feel free to review and copy my method in your own project!.</td>
    <td>I am also using Ansible to provide configuration management, feel free to review and copy my method in your own project!</td>
    <td>This repository includes a lab folder which contains several scenarios. Using Ansible you can apply the configuration for each scenario by using the "Extra-Vars" option, which I will display an example below to better explain!</td>
    <td>For local Secret Management I am using Ansible-Vault to encrypt my secrets on disk. I am also using two environmental variables to share Vault details to my test cases.</td>
  </tr>
</table>

## Testing

Currently I am only using Python Unit tests to ensure inventory sanity and to confirm configuration operational state for each lab. To install the packages required for the untitests you should run the commands in the order shown:

1. `python3 -m venv .venv`
2. `python3 -m pip install -r requirements.txt`

These two commands should be ran *BEFORE* starting the lab.

## IaC

In this repository I am using [ContainerLab](https://containerlab.dev/) to serve as my Infrastructure as Code (IaC) orchestrator, feel free to review and copy my method in your own project!. From the ContainerLab documentation:

```
Containerlab provides a CLI for orchestrating and managing container-based networking labs. It starts the containers, builds a virtual wiring between them to create lab topologies of users choice and manages labs lifecycle.
```

You can get started with their install guide [here](https://containerlab.dev/install/). I am using Windows Subsystem for Linux as my local host, the warning provided in the documentation appears to be referring to WSL version 1. If you too choose to use the Windows Subsystem for Linux to run this project then ensure you are using [WSL version 2](https://containerlab.dev/install/).

Please click the asciinema recording below for an idea on how to perform lab resource management using ContainerLab.

[![asciicast](https://asciinema.org/a/553695.svg)](https://asciinema.org/a/553695?autoplay=1)


## Configuration Management

In this project I use ansible to configure each router for the lab scenario. The command is `ansible-playbook -i clab-bgp/ansible-inventory.yml -u admin -k configure.yaml -e lab=base`.

The command can be understood when broken down as such:

 * `-i clab-bgp/ansible-inventory.yml` the `-i` flag tells ansible to use a specific inventory file. The inventory file is generated by containerlab dynamically.
 * `-u admin -k` the use of the `-u` flag tells ansible to log into the routers using the `admin` user. The `-k` flag tells ansible to prompt for a password.
 * `-e lab=base` the use of the `-e` flag tells ansible that there are [extra variables](https://www.redhat.com/sysadmin/extra-variables-ansible-playbook) to be used in the play. This extra variable is used to specify which lab's configuration you want to deploy.

For an example of how to run the project and configure an example lab please click the asciinema recording below.

[![asciicast](https://asciinema.org/a/553697.svg)](https://asciinema.org/a/553697?autoplay=1)

## Labs

You can check what labs are available by opening the `labs` directory. If you pass a lab into the extra variables portion of the Ansible play you will alerted if it is invalid and what valid labs are.

```bash
root@wsl2-debian:~/labs/routing/bgp# ansible-playbook -i clab-bgp/ansible-inventory.yml -u admin -k configure.yaml -e lab=wrong_lab_name
SSH password: 
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details

PLAY [Setting up the lab] **************************************************************************************************************************************************************************************************************

TASK [Check that the lab extra vars is defined] ****************************************************************************************************************************************************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [check lab is valid] **************************************************************************************************************************************************************************************************************
fatal: [localhost]: FAILED! => {
    "assertion": "lab in labs",
    "changed": false,
    "evaluated_to": false,
    "msg": "Valid labs are, ['base', 'neighbors']."
}

PLAY RECAP *****************************************************************************************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

root@wsl2-debian:~/labs/routing/bgp#
```

## Secret Management

Secret Management is a very important topic for operating in a secure environment. Security of an environment should be a default mindset as well as the path of least resistance. I choose Ansible Vault for my secret management for this project due to how easily it can be obtained and the availability of a python library which meant interacting with it was easy.

To get started with Ansible Vault run the `ansible-vault create $file-name.yaml` command in your terminal. This will create the filename in your current directory and prompt you for a secure password.  This password can be any vault that you feel is secure enough for your environment. I for example always use `openssl rand -hex 14` to generate my password which ensures that my password is randomly generated, unlikely to be regenerated by chance again as well have a predictable encoding and length to allow me to use for example a Python script with the Regex Library to scan clear text or logs for a potentially leaked password.

* After generating your file you must export it's path as an environmental variable to allow the test scripts to locate the vault. This can be done with the command `export VAULT_LOC=/root/labs/routing/bgp/vault.yaml`.
* After generating your password you must export it value as an environmental variable to allow the test scripts to have access to the vault. This can be done with the command `export VAULT_PASS=abcd1234`.

You must add the credentials for your routers in this vault file in a specific syntax and order, however feel free to edit the value which is surrounded by the single ticks `'`. Here is an example of the same for my vault.

```
---
ios_user: 'admin'
ios_pass: 'admin'

```

Since the password for the vault is exported into an environmental variable it means that the variable will exist for as long as the ssh session to your server is active. If you close the session and start a new one at a later time you will have lost the information. Either feel free to re-create the vault using the same procedure above or keep your password in another location where you can still access it.

For a visual guide on how to perform these steps please consider the following asciinema link below:

[![asciicast](https://asciinema.org/a/555078.svg)](https://asciinema.org/a/555078?autoplay=1)

## Additional Considerations


Ansible by default will perform strict SSH Key checking. This means that between containerlab deployments the (identity) key used for SSH will change, but the hostname provided as part of that key will remain the same. This results in the SSH key Checking mechanism beleiving that someone is eavesdropping on the conversation. This however is not the case. It is simply that the original router you were talking to was destroyed and another was created when containerlab destroyed and deployed the lab.

I've provided an `ansible.cfg` file in this repository. Ansible should by default use this configuration file, but it if does not then you may export the environmental variable provided below to avoid this error.

`export ANSIBLE_HOST_KEY_CHECKING=False`