#!/usr/bin/python3

import os
from mako.template import Template
import json


mypath = os.path.split(os.path.abspath(__file__))[0]

with open(os.path.join(mypath, "sites.json")) as f:
  SITES = json.load(f)


def read_custom(s, filenametpl):
  customfile = filenametpl%s
  if os.path.exists(customfile): #  insert into config
    with open(customfile) as cust:
      return cust.read()
  else:
    return ""

with open("www.conf.template") as tf:
    tpl = tf.read()

with open("apache2.template") as tf:
  apache_tpl = Template(tf.read())

for s in SITES.keys():
    print(s)
    names = SITES[s]["names"]
    with_fpm = SITES[s].get("fpm", False) # default: without fpm
    with_ssl = SITES[s].get("ssl", True) # default: with SSL
    bind_ip = SITES[s].get("ip", "*")

    if with_fpm:
      poolconf = read_custom(s, "pool.conf-%s")
      os.system("useradd -m -g www-data %s"%s)
      with open("/etc/php/7.4/fpm/pool.d/%s.conf"%s, "w") as cf:
        cf.write(tpl%{"site":s}+"\n"+poolconf)

    with open("issue-%s"%s, "w") as f:
#        f.write("~/.acme.sh/acme.sh --issue --log --debug" + ''.join([" -d %s"%x for x in SITES[s]]) +" -w /var/www/html")
        f.write("certbot certonly" + ''.join([" -d %s"%x for x in names]) +" --webroot --webroot-path /var/www/html")

    custom = read_custom(s, "apache2.custom-%s")

    with open("/etc/apache2/sites-available/%s.conf"%s, "w") as f:
        print("mako site %s names %s"%(repr(s), repr(names)))
        f.write(apache_tpl.render(site=s, names=names, custom=custom, with_fpm=with_fpm, with_ssl=with_ssl, ip=bind_ip))

