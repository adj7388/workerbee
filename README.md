1. Clone this repo
2. Create virtual environment `python3 -m venv .venv`
3. Activate virutal environemt with `source .venv/bin/activate` (Linux) or `.venv/Scripts/activate` (Windows)
4. Install dependencies `pip install -r requirements.txt`
5. Set required env variable: `export SECRET_KEY='Shhhh' (Linux) or `set SECRET_KEY=Shhhhhhhh` (Windows)
6. For development, launch Flask `flask workerbee:app`
7. Create gunicorn user:group, no-login.
8. Create `/etc/systemd/system/workerbee.service` file; then `sudo systemctl daemon-reload`
9. Launch `sudo systemctl start workerbee`, launches gunicorn on port 5000
10. Install nginx and configure for upstream proxy to gunicorn port 5000. (see /etc/nginx/nginx.conf)
11. In Google Home, forward port 80 to ASUSPRO-P5440UF port 80
12. Use certbot to install Let's Encrypt certificates into nginx
13. testing 1234
