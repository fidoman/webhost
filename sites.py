#!/usr/bin/python3

import os
from mako.template import Template
import json


myhost=os.popen("hostname -f").read().strip()
print("Configuring on:", myhost)

mypath = os.path.split(os.path.abspath(__file__))[0]

with open(os.path.join(mypath, "sites.json")) as f:
  SITES = json.load(f)

site_config=SITES[""]
if myhost in SITES:
    print("updating config with local settings")
    site_config.update(SITES[myhost])
else:
    print("use defaults")

del SITES

#print(site_config)
#exit(0)

def read_custom(s, filenametpl):
  customfile = filenametpl%s
  if os.path.exists(customfile): #  insert into config
    with open(customfile) as cust:
      return cust.read()
  else:
    return ""

with open(os.path.join(mypath, "www.conf.template")) as tf:
  fpm_tpl = tf.read()

with open(os.path.join(mypath, "apache2.template")) as tf:
  apache_tpl = Template(tf.read())

srv_folders=site_config.get("srv", ["/srv"])
apache_root=site_config.get("apache_root", "/tmp")
apache_conf=site_config.get("apache_conf", "/tmp")
fpm_pools=site_config.get("fpm_pools","/tmp")
www_group=site_config.get("www_group","www")
userprefix=site_config.get("userprefix","www-")
logs=site_config.get("logs","/var/log/www-")
phpsess=site_config.get("phpsess","/var/php/sessions-")
le_prefix=site_config.get("le_prefix","")
email=site_config["email"]

for srv_folder in srv_folders:
  print("Looking for sites in:", srv_folder)
  for f in os.listdir(srv_folder):
    serv=f
    f=str(os.path.join(srv_folder, f))
    if not os.path.isdir(f):
      continue
    # serv: server name
    # f: server directory

    names_file=os.path.join(f, "names.json")
    if os.path.isfile(names_file):
      print("configure server", serv, "with", names_file)
      names_conf=json.load(open(names_file))

      for site_name in names_conf.keys():

        print("configuring", site_name, " in ", serv)
        names = names_conf[site_name]["names"]
        with_fpm = names_conf[site_name].get("fpm", False) # default: without fpm
        with_ssl = names_conf[site_name].get("ssl", True) # default: with SSL
        bind_ip = names_conf[site_name].get("ip", "*")
        bind_port = names_conf[site_name].get("port")
        with_custom = names_conf[site_name].get("custom", False) # causes fail if file is lost, as it may have security restriction

        site_user=userprefix+serv
        print("create user %s"%site_user)
        os.system("pw useradd %s -m -g %s"%(site_user, www_group))
        os.system("useradd %s -m -g %s"%(site_user, www_group))
        os.system("chown -R %s:%s %s/htdocs"%(site_user,www_group,f))
        os.system("chmod -R 640 %s/htdocs"%f)
        os.system("chmod -R ug+X %s/htdocs"%f)

        if with_fpm:
          poolconf = read_custom(site_name, os.path.join(f, "pool.conf-%s"))
          # create dir for session files
          site_phpsess=phpsess+serv
          if not os.path.exists(site_phpsess):
            os.makedirs(site_phpsess)
          os.system("chown %s %s"%(serv, site_phpsess))

          # create dir for logs
          os.system("mkdir -p %s/php"%logs)
          os.system("chgrp -R %s %s/php"%(www_group, logs))
          os.system("chmod g+w %s/php"%logs)

          print("write", "%s/%s.%s.conf"%(fpm_pools, serv, site_name))
          with open("%s/%s.%s.conf"%(fpm_pools, serv, site_name), "w") as cf:
            cf.write(fpm_tpl%{"serv": serv, "user": site_user, "group": www_group, "site":site_name, "logs":logs, "phpsess":phpsess}+"\n"+poolconf)

        with open(os.path.join(f, "issue-%s.%s"%(serv, site_name)), "w") as of:
#          f.write("~/.acme.sh/acme.sh --issue --log --debug" + ''.join([" -d %s"%x for x in names_conf[site_name]]) +" -w /var/www/html")
          of.write("certbot certonly" + ''.join([" -d %s"%x for x in names]) +" -m %s --webroot --webroot-path %s"%(email, apache_root))

        apache_custom_file=os.path.join(f, "apache2.custom-%s"%site_name)

        # load custom anyway if it exists
        if not with_custom and os.path.exists(apache_custom_file):
          print("!!!", apache_custom_file, "exists but custom not set in config")
          with_custom = True

        if with_custom: # if custom file not exists fail with error
          custom = open(apache_custom_file, "r").read()
        else:
          custom = ""

        print("write", os.path.join(apache_conf, "%s.%s.conf"%(serv, site_name)))
        with open(os.path.join(apache_conf, "%s.%s.conf"%(serv, site_name)), "w") as of:
          print("mako site %s.%s names %s"%(repr(serv), repr(site_name), repr(names)))
          of.write(apache_tpl.render(serv_path=f, logs=logs, serv=serv, site=site_name, names=names, custom=custom, with_fpm=with_fpm, with_ssl=with_ssl, ip=bind_ip, port=bind_port, email=email, le_prefix=le_prefix))
