import json
import os

import testinfra.utils.ansible_runner

runner = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
)
testinfra_hosts = runner.get_hosts("all")


def test_docker_running_and_enabled(host):
    docker = host.service("docker")
    assert docker.is_running
    assert docker.is_enabled


def test_able_to_access_docker_without_root(host):
    assert "docker" in host.user("ubuntu").groups


def test_docker_swarm_enabled(host):
    swarm_state = json.loads(
        host.check_output(
            "docker info --format '{{json .Swarm.LocalNodeState}}'"
        )
    )
    assert swarm_state == "active"


def test_docker_swarm_status(host):
    swarm_info = json.loads(
        host.check_output("docker info --format '{{json .Swarm}}'")
    )
    hostname = host.check_output("hostname -s")

    if hostname in runner.get_hosts("docker_swarm_managers"):
        msg = "Expected '%s' to be a manager" % hostname
        assert swarm_info["ControlAvailable"], msg
        assert swarm_info["Managers"] == 2
        assert swarm_info["Nodes"] == 3
    elif hostname in runner.get_hosts("docker_swarm_workers"):
        msg = "Expected '%s' to be a worker" % hostname
        assert not swarm_info["ControlAvailable"], msg
    else:
        assert False, "Unexpected hostname in swarm setup: %s" % hostname


def test_docker_swarm_labels(host):
    def get_labels(hostname):
        cmd = "docker node inspect %s --format '{{json .Spec.Labels}}'"
        return json.loads(host.check_output(cmd % hostname))

    hostname = host.check_output("hostname -s")
    if hostname in runner.get_hosts("docker_swarm_managers"):
        assert get_labels("ubuntu16") == {"one": "manager", "second": "label"}
        assert get_labels("ubuntu18") == {"a": "worker"}
        assert get_labels("extra_manager") == {"a": "worker"}
        assert get_labels("extra_manager2") == {}
