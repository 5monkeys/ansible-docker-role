# Ansible Docker Role

[![Build Status](https://travis-ci.com/5monkeys/ansible-docker-role.svg?branch=role-refactor)](https://travis-ci.com/5monkeys/ansible-docker-role)

## Dependencies

* Ansible >= 2.7
* pyOpenSSL

## Setup

* Install ansible and dependencies by running `pip install -r requirements.txt`.

* Add this role to your playbook requirements.yml:

```yaml
- src: https://github.com/5monkeys/ansible-docker-role
  name: docker
```

* Update `ansible.cfg` to search for roles relative to playbook:

```ini
roles_path = ./roles
```

* Install playbook dependencies by running `ansible-galaxy install -r requirements.yml`.

## Variables

```yaml
# What docker version to be installed (18.06, 5:18.09). Default is latest.
docker_ce_version:

# If linux-image-extra packages should be installed. Needed for the AUFS storage driver.
docker_install_kernel_extras: false
# Where to download TLS-certificates
docker_home: ".docker"
# Maps to docker -H
docker_hosts:
  - "unix://"
  - "tcp://0.0.0.0:2376"
# What docker storage driver to use
docker_storage_driver: "overlay2"
# What version of the docker python library to use
docker_python_version: "4.0.1"

# If TLS should be enabled on the docker daemon and SSL-certificates generated
docker_use_tls: "{{ 'docker_swarm_managers' in group_names }}"
# What to set as Organization in SSL-certificates
docker_tls_organization: "Acme"
# Where to place certificates on host
docker_tls_path: "/etc/docker/certs"
# When the client certificate should expire.
docker_tls_client_expires_after: "+52w"
# The client certificate common name
docker_tls_client_common_name: "client"

# If a docker swarm manager node should be initialized on the host
docker_enable_swarm: true
# What version of the python openssl library to use
docker_py_openssl_version: "19.0.0"

# These are only relevant when 'docker_enable_swarm' is true
docker_swarm_interface: "{{ ansible_default_ipv4['interface'] }}"
docker_swarm_addr: "{{ hostvars[inventory_hostname]['ansible_' + docker_swarm_interface]['ipv4']['address'] }}"
docker_swarm_port: 2377

# No node labels set per default
docker_swarm_labels: {}
```

## Example playbook(s)

The first host in the `docker_swarm_managers` group will be initiated as the master node.

Any host declared in both groups will be configured as a manager and worker(or master 
and worker if above is true).

In order to declare a node as both worker and manager, it has to be explicitly
declared in both `docker_swarm_managers` and `docker_swarm_workers` groups. _Unlike
the default behaviour from docker_, where a joining manager node will perform tasks,
if not `--availability=[drain|pause]` argument is given.

### Single node setup

```ini
# hosts file
[docker_swarm_managers]
host1

[docker_swarm_workers]
host1

[nodes]
host1
```

```yaml
# playbook.yml
- name: Setup docker
  hosts: nodes
  become: true
  become_user: root
  roles:
    - docker
  vars:
    docker_home: "{{ inventory_dir }}/.certs/"
    docker_tls_organization: "my_org"
    docker_ce_version: "5:19.03"
```

### Multi node setup

A multi node setup only accepts a `docker_swarm_managers` group with an **odd**
host count. This is in line with Docker's recommendation([which you can read more
about here](https://docs.docker.com/engine/swarm/admin_guide/)).

```ini
# hosts file
[docker_swarm_managers]
manager1  # <-- Will be initiated as master node
manager2
manager3

[docker_swarm_workers]
worker1
worker2
manager3  # <-- A manager node accepting tasks

[nodes:children]
docker_swarm_managers
docker_swarm_workers
```

```yaml
# playbook.yml
- name: Setup docker swarm
  hosts: nodes
  become: true
  become_user: root
  roles:
    - docker
  vars:
    docker_home: "{{ inventory_dir }}/.certs/"
    docker_tls_organization: "my_org"
    docker_ce_version: "5:19.03"
    docker_enable_swarm: true
```

## Adding labels to swarm nodes

The playbook looks for a declared variable named `docker_swarm_labels` in order
to set swarm labels on a node.

`docker_swarm_labels` is expected to be defined as a dict.

For a given host, the value of the `docker_swarm_labels` variable will replace
_all_ of the node's current labels. As so; if a node had previously defined any
labels, running your playbook again but now with an undefined or empty
`docker_swarm_labels` variable would remove _all_ labels from that node.

```yml
# playbook.yml
- name: Setup docker swarm
  hosts: nodes
  become: true
  become_user: root
  roles:
    - docker
  vars:
    docker_swarm_labels:
      nodes: gets_this_label
```

## Converting "manager and worker" node to "manager only" node

Converting an already deployed "manager and worker" node to a "manager only" node
is done by removing the node from the `docker_swarm_workers` group.

Consider an initial deploy with a hosts file like:

```ini
# hosts file
[docker_swarm_managers]
host1

[docker_swarm_workers]
host1
worker1
```

Now changing hosts to what follows and then running your playbook again would set
the node as "manager only":

```ini
# hosts file
[docker_swarm_managers]
host1

[docker_swarm_workers]
worker1
```
