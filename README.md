Initial Deployment
1.  `cd /opt`
2.  `git clone git@github.com:adj7388/workerbee.git`
    (adjust ownership to gunicorn:www-data?)
3.  `cd workerbee` (directory created by clone)
4.  `python3 -m venv .venv`
5.  `source .venv/bin/activate`
6.  `pip install -r requirements.txt`
7.  Create `/etc/workerbee.env` file -- see `workerbee.env.example` in repo
8.  `./deploy/deploy.sh`
9.  Use certbot to install Let's Encrypt certificates into nginx.
10. To run behind router, forward port 80/443 on router to this box port 80/443

Subsequent Deployments
1. `cd /opt/workerbee`
2. `git pull`
3. `./deploy/deploy.sh`
