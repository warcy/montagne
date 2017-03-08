#!/usr/bin/env python

"""
Installation script for Montagne development virtualenv
"""

import os
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
VENV = os.path.join(ROOT, '.venv')
PIP_REQUIRES = os.path.join(ROOT, 'requirements.txt')
PY_VERSION = "python%s.%s" % (sys.version_info[0], sys.version_info[1])

VENV_EXISTS = bool(os.path.exists(VENV))


def die(message, *args):
    print(sys.stderr, 'ERROR: ' + message % args)
    sys.exit(1)


def run_command(cmd, redirect_output=True, check_exit_code=True):
    """
    Runs a command in an out-of-process shell, returning the
    output of that command.  Working directory is ROOT.
    """
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout)
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        raise Exception('Command "%s" failed.\n%s' % (' '.join(cmd), output))
    return output


HAS_EASY_INSTALL = bool(run_command(['which', 'easy_install'],
                                    check_exit_code=False).strip())
HAS_PIP_INSTALL = bool(run_command(['which', 'pip'],
                                   check_exit_code=False).strip())
HAS_VIRTUALENV = bool(run_command(['which', 'virtualenv'],
                                  check_exit_code=False).strip())


def check_dependencies():
    """Make sure virtualenv is in the path."""
    print('Checking virtualenv installation...')

    if not HAS_VIRTUALENV:
        raise Exception('virtualenv not found. '
                        'Try installing python-virtualenv')
    print('done.')


def check_python_version():
    print('Checking Python version...')
    print('Python Version: ', PY_VERSION)

    if sys.version_info < (2, 7):
        die("Need Python Version >= 2.7")

    print('done.')


def create_virtualenv(venv=VENV, install_pip=False):
    """Creates the virtual environment and installs PIP only into the
    virtual environment
    """
    print('Creating venv...')

    install = ['virtualenv', '-q', venv, '-p', PY_VERSION]
    run_command(install)

    print('done.')
    print('Installing pip in virtualenv...'),
    if install_pip and \
            not run_command(['tools/with_venv.sh', 'easy_install',
                             'pip>1.0']):
        die("Failed to install pip.")
    print('done.')


def install_dependencies(venv=VENV):
    print('Installing dependencies with pip (this can take a while)...')
    run_command(['tools/with_venv.sh', 'pip', 'install', '-r',
                 PIP_REQUIRES], redirect_output=False)


def print_help():
    help_script = """
 Montagne development environment setup is complete.

 Montagne development uses virtualenv to track and manage Python dependencies
 while in development and testing.

 To activate the Montagne virtualenv for the extent of your current shell
 session you can run:

 $ source .venv/bin/activate

 Or, if you prefer, you can run commands in the virtualenv on a case by case
 basis by running:

 $ tools/with_venv.sh <your command>

 To deactivate the Montagne virtualenv, you can run commands:

 $ deactivate

    """
    print(help_script)


def main(argv):
    check_python_version()
    check_dependencies()
    create_virtualenv()
    install_dependencies()
    print_help()

if __name__ == '__main__':
    main(sys.argv)
