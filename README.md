Initial Deployment
1. Create /etc/workerbee.env file 
    (see workerbee.env.example in repo)
2. $ cd /opt
3. $ git clone git@github.com:adj7388/workerbee.git
4. $ python3 -m venv .venv
5. $ source .venv/bin/activate
6. $ pip install -r requirements.txt
7. $ ./deploy/deploy.sh
8. Use certbot to install Let's Encrypt certificates into nginx
9. In Google Home, forward port 80 to ASUSPRO-P5440UF port 80

Subsequent Deployments
1. cd /opt/workerbee
2. git pull
3. ./deploy/deploy.sh
