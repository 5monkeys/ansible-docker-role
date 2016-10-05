# Ansible Docker Role

### Setup
Add this repository as a `submodule` to your existing playbook repository
``` sh
git submodule add git@github.com:5monkeys/ansible-docker-role.git roles/docker
```

### Install
Run your playbook with `install` tag to install and configure docker
``` sh
ansible-playbook -i <ip>, <playbook>.yml --tags install
```

### Playbook variables
``` yaml
docker_network_name: foobar  # If defined, creates a docker network with this name.
docker_network_driver: bridge  # Default
docker_network_subnet: 172.25.0.0/16  # Default
```

    NOTE: See [playbook.example.yml](https://github.com/5monkeys/ansible-docker-role/blob/master/playbook.example.yml) for usage example
    
