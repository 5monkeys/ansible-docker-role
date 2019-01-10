# Ansible Docker Role

[![Build Status](https://travis-ci.com/5monkeys/ansible-docker-role.svg?branch=role-refactor)](https://travis-ci.com/5monkeys/ansible-docker-role)

## Dependencies

* Ansible >= 2.7
* pyOpenSSL

## Setup

Install ansible and dependencies by running `pip install -r requirements.txt`.

Add this role to your playbook requirements.yml:

```yaml
- src: https://github.com/5monkeys/ansible-docker-role
  name: docker
``` 

Install playbook dependencies by running `ansible-galaxy install -r requirements.yml` 

## Variables

```yaml
# What docker version to be installed. Default is latest
docker_ce_version:

# If linux-image-extra packages should be installed
docker_install_kernel_extras: true
# Where to download TLS-certificates
docker_home: ".docker"
# Maps to docker -H
docker_hosts:
  - "unix://"
  - "tcp://0.0.0.0:2376"
# What docker storage driver to use
docker_storage_driver: "overlay2"
# What version of the docker python library to use
docker_python_version: "3.6.0"

# If TLS should be enabled on the docker daemon and SSL-certificates generated
docker_use_tls: true
# What to set as Organization in SSL-certificates
docker_tls_organization: "Acme"
# Where to place certificates on host
docker_tls_path: "/etc/docker/certs"

# If a docker swarm manager node should be initialized on the host
docker_enable_swarm: true
# What version of the python openssl library to use
docker_py_openssl_version: "18.0.0"
```

## Example playbook
```yaml
- name: Setup docker
  hosts: managers
  become: true
  become_user: root
  roles:
    - docker
  vars:
    docker_home: "{{ inventory_dir }}/.certs/"
    docker_tls_organization: "my_org"
    docker_ce_version: "18.06"
```
