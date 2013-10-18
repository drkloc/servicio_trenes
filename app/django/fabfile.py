from fabric.api import *
from fabric.contrib.files import exists
import os
FAB_ROOT = os.path.dirname(os.path.realpath(__file__))


def virtualenv(command):
    if env.host_string in ['localhost', '127.0.0.1']:
        local("/bin/bash -l -c '%s && %s'" % (env.activate, command))
    else:
        run("%s && %s" % (env.activate, command))


def git_pull():
    if env.host_string in ['localhost', '127.0.0.1']:
        with lcd(env.directory):
            local('git pull')
    else:
        with cd(env.directory):
            run('git pull')


def setup_virtualenv():
    if env.host_string in ['localhost', '127.0.0.1']:
        l = local
    else:
        l = run

    if not exists(os.path.join(env.work_on, env.project)):
        c = "WORKON_HOME=%s && source virtualenvwrapper.sh && mkvirtualenv %s" % (
            env.work_on,
            env.project,
        )
        if env.host_string in ['localhost', '127.0.0.1']:
            l("/bin/bash -l -c '%s'" % c)
        else:
            l(c)


def install_requirements():
    virtualenv('pip install -r %s' % (os.path.join(env.directory, 'requirements.txt')))


def setup_app():
    if not exists('%s/logs' % env.log_dir):
        virtualenv('cd %s && mkdir -p logs' % env.log_dir)
    virtualenv('cd %s && python manage.py syncdb --noinput' % env.project)
    virtualenv('cd %s && python manage.py collectstatic --noinput' % env.project)
    virtualenv('cd %s && python manage.py crear_lineas' % env.project)

def restart_celery():
    pass
    # run('/home/teo/bin/supervisorctl restart dtcelerybeat dtceleryd')

def freeze():
    virtualenv(
        'pip freeze | %s > %s' % (
            'grep -v distribute | grep -v wsgiref',
            os.path.join(
                env.directory,
                'requirements.txt'
            )
        )
    )


def push(message):
    local('git add . -A')
    local('git commit -m "%s"' % message)
    local('git push')


def LOCAL():
    env.hosts = ['localhost']
    env.project = 'horariostrenes'
    env.work_on = '~/.virtualenvs/horarios-trenes'
    env.directory = FAB_ROOT
    env.activate = 'source %s' % os.path.join(env.work_on, 'bin/activate')


def DEV():
    env.hosts = ['127.0.0.1']
    env.project = 'servicetrenes'
    env.log_dir = os.path.join(
        FAB_ROOT,
        env.project,
        env.project
    )
    env.user = 'horariostrenes'
    env.password = 'horariostrenes'
    env.work_on = '/home/%s/.virtualenvs/' % env.user
    env.directory = FAB_ROOT
    env.activate = 'source %s' % os.path.join(
        env.work_on,
        env.project,
        'bin/activate'
    )


def setup():
    setup_virtualenv()
    install_requirements()
    setup_app()


def update():
    git_pull()
    install_requirements()
    setup_app()


def quick_update():
    git_pull()
    setup_app()
