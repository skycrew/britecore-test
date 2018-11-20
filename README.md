# Britecore Implementation Engineer Hiring Project: Feature Request App
### Live Demo:
https://britecore-test.ml/

### Setting Up Development Env

 - Install Docker
 - Clone this repo
 - Build docker image
    ```bash
    cd britecore-test
    ./dockerhelper.py build
    ```
 - Start flask app
 `./dockerhelper.py start`
  After you executed above command, you can now point your browser to https://localhost:8080
 - Or you can run tests for this app
 `./dockerhelper.py run_tests`
 - To stop the container
 `./dockerhelper.py stop`

### Deployment
To deploy this Flask app, you can use a script in `deployment/fabfile.py`. You need to install [Fabric](https://www.fabfile.org/ "Fabric") in order to run this script. While Fabric support both Python2 and Python3, I recommend you to use Python3 for this script. Make sure you have a Ubuntu VM with SSH access. Simply run the command below:
```bash
cd britecore-test/deployment
fab -f fabfile.py -H <host> provision
```
Once script executed successfully, you can now point your browser to http://vm-ip-address
