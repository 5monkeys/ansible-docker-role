# Ansible Docker Role

### Setup
Add this repository as a `submodule` to your existing playbook repository
``` sh
git submodule add git@github.com:5monkeys/ansible-docker-role.git roles/docker
```

### Install
Run your playbook with `install-docker` tag to install and configure docker
``` sh
ansible-playbook -i <ip>, <playbook>.yml --tags install-docker
```

**NOTE:** See [playbook.example.yml](https://github.com/5monkeys/ansible-docker-role/blob/master/playbook.example.yml) for usage example
