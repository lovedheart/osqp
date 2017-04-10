from __future__ import print_function
from builtins import input
import os
import tarfile
from platform import system
import osqp  # Need python OSQP module to run
import shutil as sh
from subprocess import call
import glob

def okay():
    print("Done.\n")


def compress_dir(path):

    print("Compressing files to %s.tar.gz..." % path)

    tar_file = tarfile.open('%s.tar.gz' % path, "w:gz")

    for file_name in glob.glob(os.path.join(path, "*")):
        print("  Adding %s..." % file_name)
        tar_file.add(file_name, os.path.basename(file_name))

    tar_file.close()

    okay()


if __name__ == '__main__':

    # Get oeprative system
    if system() == 'Windows':
        platform = 'windows'
        matlab_ext = 'mexw64'
    elif system() == 'Linux':
        platform = 'linux'
        matlab_ext = 'mexa64'
    elif system() == 'Darwin':
        platform = 'mac'
        matlab_ext = 'mexmaci64'

    # Get OSQP version
    m = osqp.OSQP()
    version = m.version()

    # Get package name
    package_name = "osqp-%s-matlab-%s" % (version, platform)

    print("Creating build directory %s/..." % package_name)

    # Create build directory
    if os.path.exists(package_name):
        sh.rmtree(package_name)
    os.makedirs(package_name)

    okay()

    print("Copying folders...")

    # Copy folders
    folders_to_copy = ['codegen', 'unittests']
    for folder_name in folders_to_copy:
        print("  Copying  %s/%s/..." % (package_name, folder_name))
        sh.copytree(os.path.join('..', folder_name),
                    os.path.join(package_name, folder_name))

    okay()

    print("Copying files...")
    # Copy interface files
    files_to_copy = ['osqp_mex.%s' % matlab_ext,
                     'osqp.m']

    for file_name in files_to_copy:
        print("  Copying  %s/%s..." % (package_name, file_name))
        sh.copy(os.path.join('..', file_name),
                os.path.join(package_name))

    okay()

    # Create tar.gz file
    compress_dir(package_name)

    # Upload to github
    print("Uploading to GitHub, release v%s ..." % version)
    gh_token = input("GitHub token: ")

    call(['github-release', 'upload',
          '--user', 'oxfordcontrol',
          '--security-token', gh_token,
          '--repo', 'osqp',
          '--tag', 'v%s' % version,
          '--name', package_name + '.tar.gz',
          '--file', package_name + '.tar.gz'])
