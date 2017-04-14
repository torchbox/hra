from datetime import datetime

from fabric.api import *

env.roledefs = {
    'production': [],  # CHANGEME
    'staging': [],  # CHANGEME
}


@roles('production')
def deploy_production():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    run('git pull')
    run('pip install -r requirements.txt')
    _run_migrate()
    run('django-admin collectstatic --noinput')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')

    _post_deploy()


@roles('staging')
def deploy_staging():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    run('git pull')
    run('pip install -r requirements.txt')
    _run_migrate()
    run('django-admin collectstatic --noinput')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')

    _post_deploy()


@runs_once
@roles('production')
def pull_production_data():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    _pull_data(
        env_name='production',
        remote_db_name='hra',
        local_db_name='hra',
        remote_dump_path='/usr/local/django/hra/tmp/',
        local_dump_path='/tmp/',
    )


@runs_once
@roles('staging')
def pull_staging_data():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    _pull_data(
        env_name='staging',
        remote_db_name='hra',
        local_db_name='hra',
        remote_dump_path='/usr/local/django/hra/tmp/',
        local_dump_path='/tmp/',
    )


@runs_once
@roles('production')
def pull_production_media():
    local('rsync -avz %s:\'%s\' /vagrant/media/' % (env['host_string'], '$CFG_MEDIA_DIR'))


@runs_once
@roles('staging')
def pull_staging_media():
    local('rsync -avz %s:\'%s\' /vagrant/media/' % (env['host_string'], '$CFG_MEDIA_DIR'))


@runs_once
def _pull_data(env_name, remote_db_name, local_db_name, remote_dump_path, local_dump_path):
    timestamp = datetime.now().strftime('%Y%m%d-%I%M%S')

    filename = '.'.join([env_name, remote_db_name, timestamp, 'sql'])
    remote_filename = remote_dump_path + filename
    local_filename = local_dump_path + filename

    params = {
        'remote_db_name': remote_db_name,
        'remote_filename': remote_filename,
        'local_db_name': local_db_name,
        'local_filename': local_filename,
    }

    # Dump/download database from server
    run('pg_dump {remote_db_name} -xOf {remote_filename}'.format(**params))
    run('gzip {remote_filename}'.format(**params))
    get('{remote_filename}.gz'.format(**params), '{local_filename}.gz'.format(**params))
    run('rm {remote_filename}.gz'.format(**params))

    # Load database locally
    local('gunzip {local_filename}.gz'.format(**params))
    local('dropdb {local_db_name}'.format(**params))
    local('createdb {local_db_name}'.format(**params))
    local('psql {local_db_name} -f {local_filename}'.format(**params))
    local('rm {local_filename}'.format(**params))

    newsuperuser = prompt('Any superuser accounts you previously created locally will have been wiped. Do you wish to create a new superuser? (Y/n): ', default="Y")
    if newsuperuser == 'Y':
        local('django-admin createsuperuser')


@runs_once
def _run_migrate():
    run('django-admin migrate --noinput')


@runs_once
def _post_deploy():
    # clear frontend cache
    run('ats-cache-purge $CFG_PRIMARY_HOST')

    # update search index
    run('django-admin update_index')
