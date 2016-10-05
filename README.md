# Ansible Docker Role

Add this repository as a submodule to your existing playbook repository
``` sh
git submodule add git@github.com:5monkeys/ansible-docker-role.git roles/docker
```

Run your playbook with `install` tag to install and configure docker
``` sh
ansible-playbook -i <ip>, <playbook>.yml --tags install
```
