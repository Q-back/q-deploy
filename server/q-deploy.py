# it's just prototype
print(
    "Q-Deploy. Q-Back's script used to deploy Django apps using gunicorn"
    "supervisorctl and nginx. I need root privileges and I'll modify system"
    "files"
    )

account_name = input("Account name (admin_q)") or 'admin_q'
django_dir = input("Django directory (DjangoProjects)") or 'DjangoProjects'
program_name = input("Program name")
domain = input(f"Domain for {program_name}")
directory_path = f'/home/{account_name}/{django_dir}/{program_name}/{program_name}'

# Set up supervisor
print("writing to supervisord.conf ...")
with open('/etc/supervisord.conf', 'a+') as super_conf:
    new_conf = (
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
    super_conf.write(new_conf)
print("OK")

# Set up Nginx
print("writing nginx conf ...")
with open(f'/etc/nginx/sites-available/{domain}', 'w+') as nginx_conf:
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
    nginx_conf.write(conf)
print("OK")
