# GeoNode Ansible Role

This Ansible Role will install GeoNode and required dependencies onto an Ubuntu 18.04 (Bionic) host. It includes tasks for PostgreSQL+PostGIS, GeoServer, GeoNode, nginx, uswgi and also includes tasks for using AWS RDS databases. It is meant to be used with a GeoNode template project by following the workflow described here http://github.com/geonode/geonode-project

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
* `geonode_version` - GeoNode version to install if this information is not included in the requirements.txt file (default: `2.10rc4`)

The `app_name` variable will be used to set the database names and credentials. You can override this behavior with the following variables.

* `db_data_instance` - Database instance for spatial data (default: `{{ app_name }}`)
* `db_metadata_instance` - Database instance for the application metadata (default: `{{ app_name }}_app`)
* `db_password` - Database password (default: `{{ app_name }}`)
* `db_user` - Database user (default: `{{ app_name }}`)

You can also change the war used to deploy geoserver with the following variable.

* `gs_war_url` - GeoServer war URL (default: `https://build.geo-solutions.it/geonode/geoserver/latest/geoserver-2.9.x-oauth2.war`)

You can tune PostgreSQL, Tomcat8, and NGINX with the following variables:

* `pg_max_connections` - PostgreSQL Max Connections (default: `100`)
* `pg_shared_buffers` - PostgreSQL Shared Buffers (default: `128MB`)
* `tomcat_xms` - Tomcat JAVA_OPTS xms (default: `1024M`)
* `tomcat_xmx` - Tomcat JAVA_OPTS xmx (default: `2048M`)
* `nginx_client_max_body_size` - NGINX Client Max Body Size (default: `400M`)
* `uwsgi_processes` - UWSGI number of processes (default: `4`)

The following security variables should be added to `ansible-playbook ...` as command line flags or stored securely outside of `ansible-geonode`, `geonode-project`, or your project repo.

* `gs_admin_password` - GeoServer Admin Password (default: `geoserver`)
* `gs_root_password` - GeoServer Root Password

## Dependencies

## Example Playbook

The following is an example playbook using variables. This playbook will be included in your geonode template project clone.

    - hosts: webservers
        remote_user: ubuntu
        vars:
            app_name: my_geonode
            github_user: GeoNode
        roles:
            - { role: GeoNode.geonode }

Run with:

    ansible-playbook --ask-become-pass ./playbook.yml

## License

BSD

## Author Information

This repo is maintained by the GeoNode development team (https://github.com/GeoNode/geonode/blob/master/AUTHORS)
