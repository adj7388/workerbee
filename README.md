# Background
The original intent of this project was to develop a simple web application (simple, but not too simple, i.e., not a toy) that I was going to use to produce a series of web app development tutorials on YouTube. My vision was to aim the tuturials at complete beginners, maybe high school-ish age, but really for "kids" of all ages who might be curious about how web apps work. This led me down a rabbit hole described in the About page. I'll not repeat all that here.

Long story short: I never did the tutorials, but decided to make the code public anyway in case it interests anyone.

# Initial Deployment
1. `cd /opt`
1. `git clone git@github.com:adj7388/workerbee.git`
1. `sudo chown gunicorn:www-data -R .`
1. `cd workerbee` (directory created by clone)
1. `python3 -m venv .venv`
1. `source .venv/bin/activate`
1. `pip install -r requirements.txt`
1. I used VS Code to develop this, so you should be able to launch VS Code now and open the `workerbee` folder. 


1. Create `/etc/workerbee.env` file -- see `workerbee.env.example` in repo
1. `./deploy/deploy.sh`
1. Use certbot to install Let's Encrypt certificates into nginx.
1. To run behind router, forward port 80/443 on router to this box port 80/443

# Subsequent Deployments
1. `cd /opt/workerbee`
1. `git pull`
1. `./deploy/deploy.sh`
