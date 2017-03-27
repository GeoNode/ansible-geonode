# GeoNode Ansible Role

This Ansible Role will install GeoNode and required dependencies onto an Ubuntu 16.04 (Xenial) host. It includes tasks for PostgreSQL+PostGIS, GeoServer, GeoNode, nginx, uswgi and also includes tasks for using AWS RDS databases. It is meant to be used with a GeoNode template project by following the workflow described here http://github.com/geonode/geonode-project

## Requirements

There are three cases to use this project:

* You already have a GeoNode template published on GitHub. You can continue with the next section without any additional requirements.
* You do not have a GeoNode template published on GitHub and wish to create one. You will need to create and activate a virtualenv, pip install geonode, clone the template project, push your changes to github and update the Role Variables. For more details see http://github.com/geonode/geonode-project
* You do not have a GeoNode template and you do not want to create one. In that case use "GeoNode" as the github_user variable, this Role will clone and install the empty GeoNode template project for you (this is meant to be a demonstration-only setup, for production setup use the first option).

## Role Variables

* `app_name` - GeoNode project name (default: `my_geonode`)
* `github_user` - GitHub username that owns the project (default: `GeoNode`)
* `repo_name` - GitHub repository name (defaults to `app_name`: `my_geonode`)
* `code_repository` - URL to the Code Repository (default: `https://github.com/{{ github_user }}/{{ app_name }}.git`)
* `branch_name` - Git branch to use for deployment (default: `master`)

The `app_name` variable will be used to set the database names and credentials. You can override this behavior with the following variables.

* `db_data_instance` - Database instance for spatial data (default: `{{ app_name }}`)
* `db_metadata_instance` - Database instance for the application metadata (default: `{{ app_name }}_app`)
* `db_password` - Database password (default: `{{ app_name }}`)
* `db_user` - Database user (default: `{{ app_name }}`)

You can also change the war used to deploy geoserver with the following variable.

* `gs_war_url` - GeoServer war URL (default: `http://build.geonode.org/geoserver/latest/geoserver.war`)

You can tune PostgreSQL, Tomcat8, and NGINX with the following variables:

* `pg_max_connections` - PostgreSQL Max Connections (default: `100`)
* `pg_shared_buffers` - PostgreSQL Shared Buffers (default: `128MB`)
* `tomcat_xms` - Tomcat JAVA_OPTS xms (default: `1024M`)
* `tomcat_xmx` - Tomcat JAVA_OPTS xmx (default: `2048M`)
* `nginx_client_max_body_size` - NGINX Client Max Body Size (default: `400M`)

The following security variables should be added to `ansible-playbook ...` as command line flags or stored securely outside of `ansible-geonode`, `geonode-project`, or your project repo.

* `dj_superuser_password` - Django Admin Password (default: `admin`)
* `gs_admin_password` - GeoServer Admin Password (default: `geoserver`)
* `gs_root_password` - GeoServer Root Password (default: `M(cqp{V1`)

## Dependencies


## Example Playbook

The following is an example playbook using variables. This playbook will be included in your geonode template project clone.

```
- name: Provision a GeoNode into Production
  hosts: production
  remote_user: ubuntu
  vars:
    app_name: {{ project_name }}
    github_user: geonode
    server_name: 0.0.0.0
    deploy_user: ubuntu
    code_repository: https://github.com/-----/{{ project_name }}.git" # e.g., "https://github.com/GeoNode/{{ project_name }}.git"
    branch_name: master
    virtualenv_dir: "/home/ubuntu/.venvs"
    site_url: "http://localhost:8000/" # The public url of the GeoNode instance
    geoserver_url: "http://build.geonode.org/geoserver/latest/geoserver-2.9.x-oauth2.war" # geoserver_url should match what is found in dev_config.yml
    pg_max_connections: 100
    pg_shared_buffers: 128MB
    tomcat_xms: "1024M"
    tomcat_xmx: "2048M"
    nginx_client_max_body_size: "400M"
    letsencrypt: False
  gather_facts: False
  pre_tasks:
    - name: Install python for Ansible
      become: yes
      become_user: root
      raw: test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)
    - name: 'Reconfigue Locales'
      become: yes
      become_user: root
      shell: "{{ item }}"
      with_items:
        - "export LANGUAGE=en_US.UTF-8"
        - "export LANG=en_US.UTF-8"
        - "export LC_ALL=en_US.UTF-8"
        - "locale-gen --purge en_US.UTF-8"
        - "echo 'LANG=en_US.UTF-8\nLANGUAGE=en_US:en\n' > /etc/default/locale"
    - name: "Install cul, vim, and unzip"
      become: yes
      become_user: root
      apt: name="{{ item }}" state=latest
      with_items:
        - curl
        - vim
        - unzip
    - setup: # aka gather_facts
  roles:
     - { role: GeoNode.geonode }
```

## Usage

Your command line call to `ansible-playbook` should look something like this.

```
ansible-playbook -e "gs_root_password=<new gs root password>" -e "gs_admin_password=<new gs admin password>" -e "dj_superuser_password=<new django admin password>" -i inventory --limit all playbook.yml
```

Additionally, you can set the `ANSIBLE_ROLES_PATH` environmental variable inline if you do not want to use the default path.

```
ANSIBLE_ROLES_PATH=~/workspaces/public ansible-playbook ...
```

## License

BSD

## Author Information

This repo is maintained by the GeoNode development team (https://github.com/GeoNode/geonode/blob/master/AUTHORS)
