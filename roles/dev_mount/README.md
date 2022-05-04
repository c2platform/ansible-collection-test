# Ansible Role dev_mount

This role allows you to configure and SSH public key for `.ssh/authorized_keys` and then mount one or more directories on the Ansible control node using [SSHFS](https://en.wikipedia.org/wiki/SSHFS).

<!-- MarkdownTOC levels="2,3" autolink="true" -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
- name: Mount
  hosts: all
  become: yes

  roles:
    - { role: c2platform.test.dev_mount }

  vars:
    dev_mount_ssh_key: https://raw.githubusercontent.com/hashicorp/vagrant/master/keys/vagrant.pub #"{{ common_dev_key }}"
    dev_mount_dir: /home/user/project/infra/mounts/dev
    dev_mount_owner: myuser
    dev_mount_state: present
    dev_mount:
      - owner: root
        hosts: "{{ groups['haproxy'] }}"
        mounts: []
        #  - /var/log
        #  - /etc/haproxy
      - owner: tomcat
        hosts: "{{ groups['suwinet_tomcat']|difference(groups['suwinet_util_disabled']) }}"
        mounts:
          - /opt/tomcat/tomcat/logs
          - /opt/tomcat/tomcat/conf
```
