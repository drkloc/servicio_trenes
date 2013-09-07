from fabric.api import *
from fabric.decorators import hosts
import os
FAB_ROOT = os.path.dirname(os.path.realpath(__file__))


def virtualenv(command):
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local("/bin/bash -l -c '%s && %s'" % (env.activate, command))
    else:
        with cd(env.directory):
            run("%s && %s" % (env.activate, command))


def git_pull():
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local('git pull')
    else:
        with cd(env.directory):
            run('git pull')


def setup_virtualenv():
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local('virtualenv . --distribute')
    else:
        run('mkvirtualenv --no-site-packages --distribute coras')


@hosts('DEV')
def setflags():
    virtualenv('export CFLAGS="-I/usr/local/include -L/opt/local/lib"')


def install_requirements():
    setflags()
    virtualenv('pip install -U -r %s' % (os.path.join(env.directory, 'requirements.txt')))


def setup_app():
    virtualenv('cd %s && python manage.py syncdb --noinput' % env.project_directory)
    virtualenv('cd %s && python manage.py migrate' % env.project_directory)


def freeze():
    virtualenv('pip freeze | grep -v distribute | grep -v wsgiref > requirements.txt')


def push(message):
    local('git add . -A')
    local('git commit -m "%s"' % message)
    local('git push')


def DEV():
    env.hosts = ['localhost']
    env.directory = FAB_ROOT
    env.virtualenv = '~/.virtualenvs/horarios-trenes'
    env.activate = 'source %s' % os.path.join(env.virtualenv, 'bin/activate')
    env.project_directory = 'redminescore'


def setup():
    setup_virtualenv()
    install_requirements()


def update():
    git_pull()
    install_requirements()
    setup_app()


def quick_update():
    git_pull()
    setup_app()
