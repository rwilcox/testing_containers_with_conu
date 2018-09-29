#!/usr/bin/env python3

# Testing microservices is a bit different from testing containers
#
# Often a microservice will require other services: for example, a database
# 
# As a build pipeline I don't want to care about what dependancies the developer's silly program requires
# I just want to make sure that _maybe_ their application runs even just a little bit inside the container.
# "Does it even launch? Maybe respond to a health check? Please?""
#
# This example code implements those behaviors by expecting the developer to create a Docker Compose file
# for us.
#
# Docker Compose is not magic, in from an image/container perspective half of Docker Compose is just NAMESPACES
# THUS, because nothing's really super magic (until the deep magic hits) we can reverse-engineer enough
# magic to identify and grab onto the container Docker Compose has launched
# (then do tests against that container!!)
#
# we again use conu. Thanks, conu.

from conu import DockerBackend, DockerRunBuilder
from conu.helpers import get_container_output


def iterate_containers(name):
    with DockerBackend() as backend:
        for current in backend.list_containers():

            # need the name of the container, not the name of the image here,
            # as we may be running containers whose image name is the same (ie on a CI server)
            # BUT Docker Compose namespaces _container_ names
            docker_name = current.get_metadata().name
            if docker_name.find(name) > -1:
                return current


def is_container_running(containerId, containerName):
    with DockerBackend() as backend:
        container = backend.ContainerClass(None, containerId, containerName)

        assert container.is_running(), ("Container found, but is not running (%s)" % containerName)

        with container.http_client(port=8081) as request:
            res = request.get("/health")  # HAHA, http-echo returns what we say EXCEPT for /health. That is special. Thanks(??) Hashicorp. WD-rpw 09-29-2018
            text = res.text.strip()
            assert text == """{"status":"ok"}""", ("Text was %s", text)


docker_compose_namespace = "test_docker_compose_service"
docker_compose_container_name = "%s_sit" % docker_compose_namespace
found = iterate_containers( docker_compose_container_name )

assert found != None, ("No container found for %s", docker_compose_container_name)
is_container_running( found.get_id(), found.get_image_name() )

print("****** TESTS DONE EVERYTHING IS FINE *********************")