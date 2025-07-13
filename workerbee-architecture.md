>>>>>>>>>>>>>>>>>>>> app dir
alan@alan-ASUSPRO-P5440UF:/opt/workerbee$ ls -la
total 52
drwxrwx---  8 gunicorn gunicorn 4096 Jul 13 15:29 .
drwxr-xr-x  4 root     root     4096 Mar  3 22:15 ..
drwxrwxr-x 16 gunicorn gunicorn 4096 Jul  4 22:08 data
drwxrwxr-x  8 gunicorn gunicorn 4096 Jul 13 15:19 .git
-rw-rw-r--  1 gunicorn gunicorn  142 Jul 13 15:29 .gitignore
drwxr-xr-x  2 gunicorn www-data 4096 Jul 13 15:19 __pycache__
-rw-rw-r--  1 gunicorn gunicorn  860 Mar  3 22:35 README.md
-rw-rw-r--  1 gunicorn gunicorn  176 Mar  3 22:21 requirements.txt
drwxrwxr-x  5 gunicorn gunicorn 4096 Mar  3 22:26 .venv
drwxrwxr-x  2 gunicorn gunicorn 4096 Jul 13 15:19 .vscode
drwxrwxr-x  7 gunicorn gunicorn 4096 Jul 13 14:46 workerbee
-rw-rw-r--  1 gunicorn gunicorn 2013 Mar  3 22:21 workerbee-architecture.md
-rw-rw-r--  1 alan     alan       53 Jul 13 15:19 wsgi.py

>>>>>>>>>>>>>>>>>>>> /etc/systemd/system/workerbee.service
[Unit]
Description=Workerbee App
After=network.target

[Service]
User=gunicorn
Group=www-data

RuntimeDirectory=workerbee
RuntimeDirectoryMode=0770
ExecStartPre=/bin/mkdir -p /var/run/workerbee
ExecStartPre=/bin/chown -R gunicorn:www-data /var/run/workerbee

WorkingDirectory=/opt/workerbee/
ExecStart=/opt/workerbee/.venv/bin/gunicorn --access-logfile /var/log/gunicorn/workerbee-access.log --error-logfile=/var/log/gunicorn/workerbee-error.log -w 4 --bind unix:/var/run/workerbee/workerbee.sock --umask 007 "wsgi:app"

Restart=always
RestartSec=5
Environment="SECRETBEEKEY=qwertyuiopasdfjkl;zxc,vmn.,masdflkjweqriouasdfjhalkjh139087471234"

[Install]
WantedBy=multi-user.target

>>>>>>>>>>>>>>> nginx.conf
location / {
    # Proxy pass to Gunicorn
    # proxy_pass http://127.0.0.1:5000;  # or to unix socket: unix:/tmp/gunicorn.sock;
    proxy_pass http://unix:/var/run/workerbee/workerbee.sock;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

>>>>>>>>>>>>>>>>>>>>> nginx <> gunicorn communication
alan@alan-ASUSPRO-P5440UF:/opt/workerbee$ ls -la /var/run/workerbee/
total 0
drwxrwx---  2 gunicorn www-data   60 Jan 19 15:40 .
drwxr-xr-x 40 root     root     1160 Jan 19 15:08 ..
srwxrwx---  1 gunicorn www-data    0 Jan 19 15:40 workerbee.sock

