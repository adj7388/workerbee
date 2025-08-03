- `systemd` for service/process management
Environment variables (especially SECRET_KEY) must be installed in `/etc/workerbee.env`
See files `workerbee.service` and `workerbee.env.example` in repo

- Nginx upstream proxy
See `nginx.conf` in repo for upstream proxy details

- Nginx and gunicorn communication
`workerbee.service` creates `/run/workerbee/workerbee.sock`
`nginx.conf` forwards traffic to `/run/workerbee/workerbee.sock`
