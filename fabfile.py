"""
    ACHTUNG. This is broken. Do not use it on the production server
    Usage:


    $ fab select:<development/staging/live> <command>

    Where command is one of:

    deploy
        Deploy to the server

    identify
        Identify the current and previous releases

    maintenance
        Put the site into maintenance mode (if possible)

    unmaintenance
        Put the site into normal operation mode (if possible)

    reload_webserver
        Reloads apache

    rollback
        Limited rollback, switches current and previous symlinks

    clean_up
        Provides a way to clean up old releases


"""
print "DO NOT USE THIS"
exit(1)
import re
import os
import time

from fabric.api import *
from fabric import colors
from fabric.contrib.files import upload_template, exists


#Globals
env.project_name = 'wiekiesjij'
env.server_type = 'linode'
env.virtualenv_folder = 'env'
env.processes = 2
env.threads = 2

ENV_DEV = 'development'
ENV_STAGING = 'staging'
ENV_LIVE = 'live'
ENVIRONMENTS = (ENV_DEV, ENV_STAGING, ENV_LIVE)


def _extra_commands():
    """
        Specify your project specific management commands here
        NOTE: these are run at every deployment !
        NOTE2: these are run on the new deployment, not the old one

    """
    require('hosts', 'environment', 'base_path', 'settings', 'hostname', provided_by=[select])
    _virtualenv_command('./manage.py setsite %(hostname)s --settings=%(settings)s' % env)


def select(name):
    """
        Select environment

    """

    if name not in ENVIRONMENTS:
        print """
            Please specify the environment:

            $ fab select:<environment>

            Where environment is one of %(environments)s
        """ % dict(environments=colors.red(", ".join(ENVIRONMENTS)))
        exit(1)

    env.environment = name

    if name == ENV_DEV:
        print(colors.red('Development environment not specified'))
        exit(1)
    elif name == ENV_STAGING:
       print "Not implemented"
       exit(1)
       env.user_name = env.project_name
       env.hosts = ['host62.griv.nl']
       env.hostname = '%(project_name)s.staging.getlogic.nl' % env
       env.settings = 'settings.staging_settings'
       env.processes = 2
       env.threads = 6
    elif name == ENV_LIVE:
       env.user_name = env.project_name
       env.hosts = ['wiekiesjij@host62.griv.nl']
       env.hostname = '%(project_name)s.nl' % env
       env.settings = 'settings.live_settings'
       env.processes = 2
       env.threads = 6

    env.base_path = '/var/projects/%(project_name)s/%(environment)s/' % env
    env.apache_config = '/etc/apache2/sites-available/%(project_name)s_%(environment)s' % env
    env.nginx_config = '/opt/nginx/conf/sites-available/%(project_name)s_%(environment)s' % env

def _print(key, value, color1=colors.white, color2=colors.yellow):
    """
        Print a key with it's value
    """
    print(color1(key, bold=True) + ' : ' + color2(value))


def clean_up():
    """
        Cleanup old releases
    """
    print "Not implemented"
    exit (1)
    require('hosts', 'environment', provided_by=[select])

    with hide('output', 'running', 'warnings'):
        with cd('%(base_path)sreleases' % env):
            result = run('ls -l')
            lines = result.split("\n")
            releases = []
            current_previous = []
            for line in lines:
                parts = line.split(" ")

                if 'current' in parts:
                    current_previous.append(parts[-1])
                    _print('current', parts[-1], color1=colors.red, color2=colors.yellow)
                    continue
                elif 'previous' in parts:
                    current_previous.append(parts[-1])
                    _print('previous', parts[-1], color1=colors.red, color2=colors.yellow)
                    continue
                elif 'total' in parts:
                    current_previous.append(parts[-1])
                else:
                    releases.append(parts[-1])

            for x in current_previous:
                if x in releases:
                    releases.remove(x)

            print "---"

            if len(releases) == 0:
                print(colors.red('No releases to be cleaned up'))
                exit(0)

            for i, release in enumerate(releases):
                _print(i, release)

            match = False
            x = 0
            y = 0
            while not match:
                user_range = prompt(colors.magenta('Give a range to clean up in the form of x-y (or c to cancel): '))
                if user_range == 'c':
                    print(colors.green('Canceled'))
                    exit(0)
                match = re.match(r'^(\d+)-(\d+)$', user_range)
                if not match:
                    print(colors.red('Invalid input'))
                    continue
                x = int(match.group(1))
                y = int(match.group(2))
                if x > y:
                    print(colors.red("First number can't be bigger then the second number"))
                    match = False
                y = y + 1

            print(colors.white('Releases to be deleted:'))
            for release in releases[x:y]:
                print(colors.yellow(release))
            if 'y' != prompt(colors.magenta('Are you sure you want to remove these releases? [y/N]')):
                print(colors.green('Canceled'))
                exit(0)

            for release in releases[x:y]:
                sudo('rm -rf ./%s' % release)

            print(colors.green('Removed the releases'))


def deploy():
    """
        Deploy to specified environment
    """
    require('hosts', 'environment', provided_by=[select])

    with hide('output', 'running', 'warnings'):

        while False:
            env.tag = prompt(colors.magenta("Which tag do you want to deploy to %(environment)s:" % env))
            if _check_tag(env.tag):
                break

        env.release_time = time.strftime('%Y%m%d-%H%M%S')
        env.revision = local('git describe --tags HEAD', capture=True)

        env.release = "%s-%s" % (env.release_time, env.revision)

        _print("environment", env.environment)
        _print("project", env.project_name)
        #_print("tag", env.tag)

        identify()

        _print("timestamp", env.release_time)
        _print("revision: ", env.revision)
        _print("new version to be deployed", env.release)



        if 'y' != prompt(colors.green('Is this correct? [y/N]')):
            print(colors.red("Aborting", bold=True))
            exit(1)

        print(colors.green("Deploying... ", bold=True))


        print(colors.cyan('Uploading to server'))
        _upload_to_server()

        print(colors.cyan('Installing requirements (will take a while)'))
        _install_requirements()

        print(colors.cyan('Putting site in maintenance', bold=True))
        maintenance()

        print(colors.cyan('Creating a backup'))
        _backup()

        print(colors.cyan('Switching symlink'))
        _symlink_current_release()

        print(colors.cyan('Building static files'))
        _build_static()

        print(colors.cyan('Migrating database'))
        _migrate()

        print(colors.cyan('Running extra commands'))
        _extra_commands()

        print(colors.cyan('Switching webserver config to current site'))
        _install_site()

        print(colors.cyan('Setting Mercurial environment tag'))
        _set_env_tag()

        print(colors.green('Done', bold=True))


def rollback():
    """
        Limited rollback capability. Simply loads the previously current
        version of the code. Rolling back again will swap between the two.
    """
    require('hosts', 'base_path', provided_by=[select])

    with hide('output', 'running', 'warnings'):

        identify()

        if 'y' != prompt(colors.green('Are you sure you wish to rollback? [y/N]')):
            abort(colors.red("Aborting", bold=True))

        with cd(env.base_path):
            sudo('mv releases/current releases/_previous;', user=env.user_name)
            sudo('mv releases/previous releases/current;', user=env.user_name)
            sudo('mv releases/_previous releases/previous;', user=env.user_name)
        reload_webserver()

        print(colors.green('Done', bold=True))

def identify():
    """
        Identifies the current and previous versions on the server
    """
    require('hosts', 'base_path', provided_by=[select])

    with hide('output', 'running', 'warnings'):
        current_version = _identify('%(base_path)sreleases/current/' % env)
        previous_version = _identify('%(base_path)sreleases/previous/' % env)

        _print("current version deployed", current_version)
        _print("previous version deployed", previous_version)


def _check_tag(tag):
    """
        Check if the given tag is valid
    """
    print "Not implemented"
    exit(1)
    with settings(warn_only=True):
        output = local('hg tags | grep "^%s "' % tag)
    return not output.failed or len(output) != 0


def _identify(path):
    """
        Identifies the version at the installed path
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])

    with settings(warn_only=True):
        with cd(path):
            return run("pwd -P | awk -F '/' '{ print $NF }'") or 'None'
    return 'None'

def _get_revision_for_tag():
    """
        Get the revision for the specified tag
    """
    require('tag', provided_by=[deploy])
    revision = local("hg identify -r %(tag)s | awk '{ print $1; }'" % env)
    return revision

def _push_to_server():
    """
        Push the code to the server
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])
    require('release', 'tag', provided_by=[deploy])

def _upload_to_server():
    """
        Upload the code to the server
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])
    require('release', provided_by=[deploy])

    #local('hg archive -r %(tag)s -t tgz %(release)s.tar.gz' % env)
    local('git archive --format=tar HEAD| gzip > %(release)s.tar.gz' % env)
    #TODO: Log deployment
    sudo('mkdir -p %(base_path)sreleases/%(release)s/' % env, user=env.user_name)
    sudo('mkdir -p %(base_path)spackages/' % env, user=env.user_name)
    sudo('chmod og+rw %(base_path)spackages/' % env, user=env.user_name)
    sudo('mkdir -p %(base_path)sbundles/' % env, user=env.user_name)
    sudo('chmod og+rw %(base_path)sbundles/' % env, user=env.user_name)

    #Upload the file
    put('%(release)s.tar.gz' % env, '%(base_path)s/packages/' % env)
    local('rm %(release)s.tar.gz' % env)

    with cd('%(base_path)sreleases/' % env):
        sudo('tar zxf ../packages/%(release)s.tar.gz' % env, user=env.user_name)

def _install_requirements():
    """
        Install the requirements
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])
    require('release', provided_by=[deploy])

    #changeset = local('hg log requirements.txt -r %(revision)s:0 -l 1 --template "{node}\\n"' % env) #TODO: before the given tag !
    changeset = 'XXX'

    env.pybundle = '%s.pybundle' % changeset

    if not exists('%(base_path)sbundles/%(pybundle)s' % env):
        print(colors.cyan('Could not find the requirements bundle, creating it'))
        with cd('%(base_path)sbundles/' % env):
            result = sudo('pip bundle -r ../releases/%(release)s/requirements.txt %(pybundle)s' % env, user=env.user_name)
            if result.failed:
                with open('error.log', 'w') as f:
                    f.write(result)
                    f.write(result.stderr)
                abort(colors.red('Creating bundle, see errors.log for the output'))

    with cd('%(base_path)s/releases/%(release)s/' % env):
        sudo('virtualenv %(virtualenv_folder)s' % env, user=env.user_name)
        result = sudo('pip -E %(virtualenv_folder)s install ../../bundles/%(pybundle)s' % env, pty=True, user=env.user_name)
        if result.failed:
            with open('error.log', 'w') as f:
                f.write(result)
                f.write(result.stderr)
            abort(colors.red('Installing requirements, see errors.log for the output'))


def reload_webserver():
    """
        Reloads the webserver
    """
    require('hostname', provided_by=[select])

    if env.server_type == 'linode':
        sudo('killall -HUP nginx')
        sudo('killall -HUP monit')
        time.sleep(2)
        sudo('monit restart %(hostname)s' % env)
    else:
        sudo('/etc/init.d/apache2 reload')

def maintenance():
    """
        Tries to put the site in maintenance
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])
    return

    with settings(warn_only=True):
        result = run('test -r %(base_path)sreleases/current/maintenance/index.html' % env)
        if not result.failed:
            upload_template(os.path.join(os.path.dirname(__file__), 'tools/templates/maintenance.txt'), env.apache_config, env, use_sudo=True)
            sudo('a2ensite %(project_name)s_%(environment)s' % env)
            reload_webserver()
        else:
            #TODO: fallback to the maintenance of the new deployment?
            warn(colors.red('Site not put into maintenance, there is no code available to do so.'))

def unmaintenance():
    """
        Tries to put get the site out of maintenance
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])
    return

    with settings(warn_only=True):
        result = run('test -r %(base_path)sreleases/current/maintenance/index.html' % env)
        if not result.failed:
            upload_template(os.path.join(os.path.dirname(__file__), 'tools/templates/normal.txt'), env.apache_config, env, use_sudo=True)
            sudo('a2ensite %(project_name)s_%(environment)s' % env)
            reload_webserver()
        else:
            #TODO: fallback to the maintenance of the new deployment?
            warn(colors.red('Site not put into maintenance, there is no code available to do so.'))


def _backup():
    """
        Run backup commands for database and media
    """
    #TODO: How will we do backups?
    pass

def _symlink_current_release():
    """
        Symlink our current release
        Note: Does switch the maintenance site already
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])


    with cd('%(base_path)s' % env):
        with settings(warn_only=True):
            result = sudo('test -e releases/previous && rm releases/previous', user=env.user_name)
            result = sudo('test -e releases/current && mv releases/current releases/previous', user=env.user_name)
            if not result.failed:
                print(colors.green('Symlinked the previous released version'))
        sudo('ln -s %(release)s releases/current' % env, user=env.user_name)

def _virtualenv_command(command):
    """
        Helper method to execute a command within the virtualenvironment
        NOTE: commands are all run in the current release, which at the deployment is the new one
        if called after the _symlink_current_release command. Or the old one if before
    """
    require('hosts', 'environment', 'base_path', 'settings', provided_by=[select])

    env.command = command
    with cd('%(base_path)sreleases/current/source/' % env):
        result = sudo('source ../%(virtualenv_folder)s/bin/activate && %(command)s' % env, user=env.user_name)
    env.command = None
    return result

def _build_static():
    """
        Build the static files
    """
    require('hosts', 'environment', 'base_path', 'settings', provided_by=[select])
    result = _virtualenv_command('./manage.py build_static --noinput --settings=%(settings)s' % env)
    if result.failed:
        with open('error.log', 'w') as f:
            f.write(result)
            f.write(result.stderr)
        abort(colors.red('Build static failed, see errors.log for the output'))

def _migrate():
    """
        Backup and migrate the database
    """
    require('hosts', 'environment', 'base_path', 'settings', provided_by=[select])
    result = _virtualenv_command('./manage.py syncdb --migrate --noinput --settings=%(settings)s' % env)
    if result.failed:
        with open('error.log', 'w') as f:
            f.write(result)
            f.write(result.stderr)
        abort(colors.red('Syncdb --migrate failed, see errors.log for the output'))

def _install_site():
    """
        Installs the site into
    """
    require('hosts', 'environment', 'base_path', provided_by=[select])

    if env.server_type == 'linode':
        _virtualenv_command('easy_install gunicorn')
        upload_template(os.path.join(os.path.dirname(__file__), 'tools/nginx_templates/normal.conf'), env.nginx_config, env, use_sudo=True)
        upload_template(os.path.join(os.path.dirname(__file__), 'tools/nginx_templates/gunicorn.conf.py'), env.base_path, env, use_sudo=True)
        upload_template(os.path.join(os.path.dirname(__file__), 'tools/nginx_templates/monit.conf'), '/etc/monit/conf.d/%(project_name)s_%(environment)s.conf' % env, env, use_sudo=True)
        sudo('ln -sf /opt/nginx/conf/sites-available/%(project_name)s_%(environment)s /opt/nginx/conf/sites-enabled/' % env)
    else:
        upload_template(os.path.join(os.path.dirname(__file__), 'tools/templates/normal.txt'), env.apache_config, env, use_sudo=True)
        sudo('a2ensite %(project_name)s_%(environment)s' % env)

    reload_webserver()

def _set_env_tag():
    """
    Sets a tag on the repository to indicate which revision is which deployment.
    """
    require('environment', provided_by=[select])
    require('tag', provided_by=[deploy])
    local("hg tag -r %(tag)s -f %(environment)s" % env)
