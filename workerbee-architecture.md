>>>>>>>>>>>>>>>>>>>> app dir
alan@alan-ASUSPRO-P5440UF:/opt/workerbee$ ls -la
total 3816
drwxr-x--- 7 gunicorn gunicorn    4096 Jan 19 13:03 .
drwxr-xr-x 3 root     root        4096 Jan 19 10:49 ..
drwxr-xr-x 8 gunicorn gunicorn    4096 Jan 19 10:49 .git
-rw-r--r-- 1 gunicorn gunicorn      71 Jan 19 10:49 .gitignore
-rw-r--r-- 1 gunicorn gunicorn     843 Jan 19 10:49 README.md
-rw-r--r-- 1 gunicorn gunicorn     176 Jan 19 10:49 requirements.txt
drwxr-xr-x 5 gunicorn gunicorn    4096 Jan 19 13:03 .venv
drwxr-xr-x 2 gunicorn gunicorn    4096 Jan 19 10:49 .vscode
-rw-r--r-- 1 gunicorn gunicorn 3864812 Jan 19 10:49 words_alpha.txt
drwxr-x--- 6 gunicorn gunicorn    4096 Jan 19 10:49 workerbee

>>>>>>>>>>>>>>>>>>>> /etc/systemd/system/workerbee.service
[Unit]
Description=Workerbee App
After=network.target

[Service]
User=gunicorn
Group=www-data
WorkingDirectory=/opt/workerbee/
ExecStart=/opt/workerbee/.venv/bin/gunicorn \
    --access-logfile /var/log/gunicorn/workerbee-access.log \
    --error-logfile=/var/log/gunicorn/workerbee-error.log \
    -w 4 --bind unix:/var/run/workerbee/workerbee.sock \
    --umask 007 workerbee:app
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

