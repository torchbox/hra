Health Research Authority Wagtail site
==================

# Setting up a local build

This repository includes a Vagrantfile for running the project in a Debian VM and
a fabfile for running common commands with Fabric.

To set up a new build you will require compatible versions of vagrant and virtualbox installed then:

``` bash
git clone git@github.com:torchbox/hra.git
cd hra
vagrant up
vagrant ssh
```

Then within the SSH session:

``` bash
dj createsuperuser
djrun
```

This will make the site available on the host machine at: http://127.0.0.1:8000/


# Available Fabric commands

To populate your local database with the content of staging/production:

``` bash
fab pull_staging_data
fab pull_production_data
```

Additionally, to fetch images from staging:

``` bash
fab pull_staging_media
```

(This will only take the "original" images. New versions of the other renditions will be recreated on the fly.)



To deploy the site to staging/production:


``` bash
fab deploy_staging
fab deploy_production
```
