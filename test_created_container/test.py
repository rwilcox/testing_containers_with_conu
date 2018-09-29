#!/usr/bin/env python3

# given a (not running) container you have built, launch it and execute a command
# HERE we want to test that our docker building process has correctly installed the required binary
# SO just run which, which (hah!) works well enough for our purposes here
#
# Where is this useful? Potentially in a pipeline that builds base images,
# to make sure that your base images really do include the JRE, or ruby, or whatever it is.
#
# We use conu to reach inside the container and do this testing!
#
# Good references:
#
# * https://conu.readthedocs.io/en/latest/index.html
# * https://fedoramagazine.org/test-containers-python-conu/

from conu import DockerBackend, DockerRunBuilder
from conu.helpers import get_container_output


def execute_container_testing_cmd():
    with DockerBackend() as backed:
        image = backed.ImageClass("nginix_rpw", "1.0.0")
        cmd = DockerRunBuilder(command = ["which", "nginx"])
        our_container = image.run_via_binary(cmd)

        assert our_container.exit_code() == 0, "command not found"
        print( "******* ngnix was installed in container *******************8" )

execute_container_testing_cmd()

