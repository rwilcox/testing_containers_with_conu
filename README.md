The Question:

How do we test containers to make sure they are somewhat valid before we launch them towards a deployment environment?

The Answer:

Some clever hacking with [Conu]( https://conu.readthedocs.io/en/latest/index.html)!!!

In this repo are two somewhat seperate behaviors we can execute with Conu:

  * "As a Docker pipeline that builds base images I want to know that the binaries I think are installed in the image really are" <-- see `test_created_container/` for this
  * "As a Docker pipeline that builds services, I want to know that the developers have created a service that maybe launches, given whatever dependancies they know they need" <-- see `test_docker_compose_service/` for this

These prototype examples shouldn't be too hard to scale up into real code (they do hardcode some values like the container name, but that hardcoding is isolated somewhat...)
