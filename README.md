Health Research Authority Wagtail site
==================

## URLs
- live: https://www.hra.nhs.uk/
- stage: http://hra-stage.trustsrv.io/

## Setting up a dev environment

First clone the repository

```bash
git clone git@github.com:isotoma/hra.git
cd hra
```

Then set up the dependencies:

### Docker

From https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt install docker
```

### Docker compose
```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install docker-compose
```

### Elastic search requirements
`sudo sysctl -w vm.max_map_count=262144` (or put in /etc/sysctl.conf for permanent change)

### Run the containers
`docker-compose up`
or individual containers can be run with `docker-compose start <name>`: See docker-compose.yml for the names

### Reload the web app
Uwsgi does not auto reload. To force a reload send a SIGHUP to the process on the web container.
`kill -HUP <pid>`


### Running a django shell or management command
```
docker exec -it hra_web bash
./manage.py <command>
```
or

```
docker-compose run web python manage.py shell
```

### Restoring a postgres dump
```
sudo cp ~/Downloads/<dumpfile>.pg pgdata/
sudo chown 999:999 pgdata/<dumpfile>.pg
docker exec -it hra_database_1 bash
dropdb hra -U hra
createdb hra -U hra
pg_restore -d hra -U hra /var/lib/postgresql/data/<dumpfile>.pg
```

## Static content
npm compile:css:prod and npm compile:js:prod in the hra/patternlab folder
TBC

## Deployments & Environment Specific Documentation
The application is hosted by Isotoma in their Trustserve hosting cluster - environment specific instructions can be found at:
https://github.com/isotoma/trustsrv.io/blob/master/doc/hra-dev.md
