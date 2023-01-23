# clab-bgp



## Capabilities

*Testing*, *IaC*, *Configuration Management*, *Labs*

| Testing | IaC | Configuration Management | Labs |
|----------------|----------------|----------------|----------------|
| Column 1 Data  | Column 2 Data  | Column 3 Data  | Column 4 Data  |

vs.

<style>
table {
  width: 100%;
}

th, td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #f5f5f5;
}
</style>

<table>
  <tr>
    <th>Testing</th>
    <th>IaC</th>
    <th>Configuration Management</th>
    <th>Labs</th>
  </tr>
  <tr>
    <td>Column 1 Data</td>
    <td>Column 2 Data</td>
    <td>Column 3 Data</td>
    <td>Column 4 Data</td>
  </tr>
</table>

## Testing

Usage of python unittests

## Considerations

Ansible by default will perform strict SSH Key checking. This means that between containerlab deployments the (identity) key used for SSH will change, but the hostname provided as part of that key will remain the same. This results in the SSH key Checking mechanism beleiving that someone is eavesdropping on the conversation. This however is not the case. It is simply that the original router you were talking to was destroyed and another was created when containerlab destroyed and deployed the lab.

I've provided an `ansible.cfg` file in this repository. Ansible should by default use this configuration file, but it if does not then you may export the environmental variable provided below to avoid this error.

`export ANSIBLE_HOST_KEY_CHECKING=False`

## Deploying the lab

You can deploy the lab by ensuring you're in the same directory as the `topology.yaml` file and executing the `clab dep -t topology.yaml` command.

