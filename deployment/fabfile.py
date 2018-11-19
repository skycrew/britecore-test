from fabric.tasks import task


@task
def provision(c):
    # update apt
    cmd = "apt update"
    sudo_cmd(c, cmd)

    # install apt packages
    cmd = "apt -y install python-pip python-dev mariadb-server libmysqlclient-dev nginx git"
    sudo_cmd(c, cmd)

    # get latest source code from github
    cmd = "git clone https://github.com/skycrew/britecore-test.git"
    run_cmd(c, cmd)

    # install library from pip
    cmd = "sudo -H -s pip install -r britecore-test/requirements.txt"
    run_cmd(c, cmd)

    # init db
    cmd = "python britecore-test/web/init_db.py"
    sudo_cmd(c, cmd)

    # copy systemd service file
    cmd = "cp britecore-test/deployment/britecore-test.service /etc/systemd/system/"
    sudo_cmd(c, cmd)

    # enable britecore service
    cmd = "systemctl enable britecore-test"
    sudo_cmd(c, cmd)

    # start britecore service
    cmd = "systemctl start britecore-test"
    sudo_cmd(c, cmd)

    # remove nginx default config
    cmd = "rm /etc/nginx/sites-enabled/default"
    sudo_cmd(c, cmd)

    # copy britecore nginx config
    cmd = "cp britecore-test/deployment/britecore-test.ml.conf /etc/nginx/sites-available/"
    sudo_cmd(c, cmd)

    # enable britecore nginx config
    cmd = "ln -s /etc/nginx/sites-available/britecore-test.ml.conf /etc/nginx/sites-enabled"
    sudo_cmd(c, cmd)

    # restart nginx
    cmd = "systemctl restart nginx"
    sudo_cmd(c, cmd)


@task
def update(c):
    cmd = "cd britecore-test; git pull"
    run_cmd(c, cmd)


def sudo_cmd(c, cmd):
    result = c.sudo(cmd)
    print(result)


def run_cmd(c, cmd):
    result = c.run(cmd)
    print(result)
