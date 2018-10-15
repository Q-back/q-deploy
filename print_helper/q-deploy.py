print(
    "Q-Deploy Print Helper. Just a simple helper which prints you ",
    "config files and where to paste them/what to do with them.\n",
    "It's really useful before finishing deployment scripts or when changing ",
    "server configuration.\n\n"
)
print(
    "Right now only 'Django + nginx + supervisor + gunicorn' "
    "is supported.\n\n"
)
program_name = input("Enter your program name\n")
domain = input("Enter your domain name\n")
account_name = input("Account name (admin_q)") or 'admin_q'
django_dir = input("Django directory (DjangoProjects)") or 'DjangoProjects'
directory_path = (
    f'/home/{account_name}/{django_dir}/{program_name}/{program_name}'
)

print(
    "If you're not using *pipenv*, then go to ~/DjangoProjects and run: \n",
    f"virtualenv -p python3 {program_name}"
)

supervisor_conf = (
    f"""
    [program:{program_name}]
    command=/home/{account_name}/{django_dir}/{program_name}/bin/gunicorn {program_name}.wsgi -b unix:/tmp/{program_name}.sock
    directory={directory_path}
    user=nobody
    autostart=true
    autorestart=true
    redirect_stderr=true
    """
)
print("Add to \n/etc/supervisord.conf\nThe config:")
print(supervisor_conf)

conf = (
    f"""
    upstream q-page {{
      server unix:/tmp/{program_name}.sock;
    }}
    server {{
            server_name {domain};

              access_log /home/admin_q/DjangoProjects/logs/access/{program_name}.log;

            location / {{
                    proxy_pass http://{program_name};
                    proxy_set_header Host $host;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }}

            location /static/ {{
                    alias /home/admin_q/DjangoProjects/{program_name}/static/;
            }}
    """
)
print(
    "Now run:\n",
    f"sudo ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/{domain}\n",
    f"sudo supervisorctl restart {program_name}\n"
    f"sudo sudo nginx -s reload\n"
)
print("Should work now ;)")
