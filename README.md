# Britecore Implementation Engineer Hiring Project: Feature Request App

This repo contain small web application that allow IWS staff to log a feature request, requested by the client. The web application will list all feature requests. Staff can create, update or delete the feature requests. This project should meet the minimum requirements as listed in the **[QUESTION](https://github.com/skycrew/britecore-test/blob/master/QUESTION.md "QUESTION")**

### Live Demo:
https://britecore-test.ml/

Hosted in GCP (micro instance) running on Ubuntu 18.04 LTS

### Setting Up Development Env

 - Install Docker
 - Clone this repo
 - Build docker image
    ```bash
    cd britecore-test
    ./dockerhelper.py build
    ```
 - Start flask app
 ```bash
 ./dockerhelper.py start
 ```
  After you executed above command, you can now point your browser to https://localhost:8080
 - Or you can run tests for this app
```bash
./dockerhelper.py run_tests
```
 - To stop the container
```bash
./dockerhelper.py stop
```
 - To edit the source code, you can SSH into the container
```bash
./dockerhelper.py ssh
```
 - Or you can mount the source code to the container so that any code changed, will be reflected in the container

### Deployment
To deploy this Flask app, you can use a script in `deployment/fabfile.py`. You need to install [Fabric](https://www.fabfile.org/ "Fabric") in order to run this script. While Fabric support both Python2 and Python3, I recommend you to use Python3 for this script. Make sure you have a Ubuntu VM with SSH access. Simply run the command below:
```bash
cd britecore-test/deployment
fab -f fabfile.py -H <host> provision
```
Once script successfully executed, you can now point your browser to http://vm-ip-address

### Tech Stack
- Docker Ubuntu 18.04 container
- Python 2.7
- MariaDB
- Flask
- SQLAlchemy
- Bootstrap 4
- jQuery
- sass
