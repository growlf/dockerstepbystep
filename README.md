# Docker - A fast lesson

From here to there, quickly and directly. 

In this tutorial exercise, we will skip the steps of installing Git, Docker, docker-compose, and Portainer as they are covered in depth elsewhere already.  Please see the links at the end of this README for more information.

Further, this codebase and documentation is meant to be used in conjunction with the [video posted by University of Calgary](https://ucalgary.yuja.com/V/Video?v=447394&node=1843378&a=1263204823&autoplay=1)

## 1.) Using Docker 

### First steps

Executing the basic command without any parameters will display built-in help:

    docker

Running an example container image:

    docker run hello-world

Review local images:

    docker image ls

Run explicitly tagged (version) of an image (default value is 'latest'):

    docker run hello-world:latest

Look at images again and notice there is no new image - because it is the same one:

    docker image ls

Help works with all commands and sub commands. Use tab-complete for command-completion in most shells:

    docker container

List containers and non-running containers:

    docker container ls
    docker ps
    docker ps -a

Use docker image ID or name to manage the image:

    docker container inspect <container_name or ID>

Run a container with a specific name:

    docker run --name test1 hello-world

List all containers (useful for finding names and status of the containers):

    docker ps -a

Run and login to a container:

    docker run --name test2 -it alpine sh
    ls -la
    pwd
    exit

Review progress to this point:

    docker image ls
    docker container ls -a
    docker network ls

Run a container with the same name again - it fails:

    docker run --name test2 hello-world

Use a new name, and add the auto-remove flag to remove the container when it finishes running:

    docker run --rm --name test3 hello-world
    docker ps -a

Clean up:

    docker container rm test2
    docker container rm <from list>
    docker ps -a
    docker system prune
    docker container ls -a

Full clean - do not do this on production systems:

    docker system prune -af
    docker image ls -a


## 2.) Run custom service in a container

Clone the project folder and files, and then review them:

    ls -la
    cat Dockerfile
    cat app/app.py
    cat requirements.txt

Build the image:

    docker build -t myapp:latest .

Run the image as a container service with exposed port in interactive mode:

    docker run --rm -p 8080:8080 myapp:latest 

Browse the localhost by accessing `http://localhost:8080/` - Use CTRL+C to stop the service when finished:

    CTRL+C

Run the image as a container with a chosen name in detached/daemon mode:

    docker run --rm -d -p 8080:8080 --name test1 myapp:latest

Verify that it is still running and attach to the logs for debugging:

    docker ps
    docker logs -f test1

USe CTRL+C to stop the log view:

    CTRL+C

Log into the still running container to test and debug directly and then stop it:

    docker exec -it test1 sh
    ls -la
    exit
    docker stop test1

## 3.) Data persistence and volumes

Run the image as a container in detached/daemon mode *and* bind a persistent volume:

    docker run --rm -d -p 8080:8080 --name test1 -v ${PWD}/app_data:/var/app_data/ myapp:latest

View the web page (`http://localhost:8080/`). Login to the container to review the `/var/app_data` directory.

    docker exec -it test1 sh
    cd /var/app_data
    ls -la
    cat counter.txt
    exit

Now, stop the container.  Since we used the `--rm` flag, it will auto remove itself.

    docker stop test1
    docker ps -a

Re run the container, view the page (`http://localhost:8080/`), and ensure that you see the counter has indeed incremented further and not simply reset itself.  

    docker run --rm -d -p 8080:8080 --name test1 -v ${PWD}/app_data:/var/app_data/ myapp:latest

Log back into the container and change the value of the counter manually.

    docker exec -it test1 sh
    cd /var/app_data
    echo '99999' > counter.txt
    exit

View the web page (`http://localhost:8080/`) again to see that the value has indeed increased dramatically.  Now open the project folder and look at `app_data/counter.txt` file and see that the value is indeed reflected there as well.  This shows that what happened in the container persists on the host filesystem.

Do not forget to stop the container.  Since we used the `--rm` flag, it will auto remove itself once stopped.

    docker stop test1


## 4.) Connecting another container with docker-compose

Many times, we will want to create more than one service for a particular deployment.  Think in terms of a website that also has a database server.  In this example we will look at only two services, but you can create and connect to more.

### Docker-compose

We are now going to use `docker-compose` to develop and test our application further because it simplifies working with multiple containers/volumes/networks/etc and also assists in some of the repetitive tasks of our cycle.  Once our application is ready for 'real' deployment, we will likely want to create a stack file from our `docker-compose.yml` which will allow the deployment to multiple hosts.

Make sure that you have docker-compose installed on your host.  Then execute the docker-compose command to build the app.

    docker-compose build

Now, bring the container up using docker-compose.

    docker-compose up

This command essentially replicates the lengthy `docker run --rm -d -p 8080:8080 --name test1 -v ${PWD}/app_data:/var/app_data/ myapp` command by putting the configuration information into `docker-compose.yml`.

Browse your webpage (`http://localhost:8080/`) to see that the application is running and properly incrementing our counter.

Hitting `CTL-C` will disconnect you from the log, but it will not shut down the container. Shut down the container when we have finished using it.

    docker-compose down

Using the `down` subcommand will tell docker to remove our container, transient volumes, networks, etc.  Leaving a clean slate for our next run.

### Adding another container

We want to add a database to our project now. We will be using a different application `app_wdb.py` and docker compose file `docker-compose-wdb.yml`. The application is very similar to the previous one, except that it is 'with database' instead of using `counter.txt` for the counter. Take a look at the contents of both files. You may find it helpful to do a side-by-side comparison between the two applications.

Start by building the container.

    docker-compose -f ./docker-compose-wdb.yml build

Bring up the container. Notice how the log contains information about both the application and the Redis database.

    docker-compose -f ./docker-compose-wdb.yml up

Browse your webpage (`http://localhost:8080/`) to see that the application is running and properly incrementing our counter.

Don't forget to shut down the container.

    docker-compose -f ./docker-compose-wdb.yml down

We can also run the container in detached mode,

    docker-compose -f ./docker-compose-wdb.yml up -d

see what containers are running,

    docker ps

connect to view the log file,

    docker-compose -f ./docker-compose-wdb.yml logs -f

disconnect with `CTL-C`, and connect to the container.

    docker exec -it myapp sh

Shut down the project when you are done.

    docker-compose -f ./docker-compose-wdb.yml down

## 5.) Portainer

Portainer is an amazing management and development tool that affords us easy, web-enabled access to all of our containers, images, networks, and so much more.

Use the documentation links below to install for your particular environment.  For myself and this demo, I am using a Windows11 system with WSL2, so my installation command is the following:

    docker run -d -p 8000:8000 -p 9443:9443 -p 9000:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data cr.portainer.io/portainer/portainer-ce:2.9.3

Since this document is intended to be used with the video, and this tool is largely a visual system, I will not detail the usage here that is demonstrated in that video. That said, once this is deployed, you can look at `http://localhost:9000/` to see an amazing new world of access to your containers and projects.

# Additional Links

## Installation documentation

* Getting started wth [Docker](https://www.docker.com/get-started)
* Getting started with [docker-compose](https://docs.docker.com/compose/gettingstarted/)
* Installing [Portainer](https://docs.portainer.io/v/ce-2.9/start/install)

## Images used

* [hello-world](https://hub.docker.com/_/hello-world)
* [Redis](https://hub.docker.com/_/redis)
* [Python](https://hub.docker.com/_/python)
* [Alpine](https://hub.docker.com/_/alpine) Linux

## Docs and sources

* [Docker](https://docs.docker.com/)
* [redis-py](https://redis-py.readthedocs.io/en/stable/)
* [Docker Hub](https://hub.docker.com/) - home of many official images, and more

## Authors and Inspiration

* [Garth Johnson](https://www.linkedin.com/in/growlf/)
* [Ann Barcomb](https://www.linkedin.com/in/annbarcomb/)
* [Ryan Shupe](https://www.linkedin.com/in/ryan-shupe-74a48219/)
* [Lance Leonard](https://www.linkedin.com/in/lleonard/)

