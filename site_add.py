#!/usr/bin/env python
#coding=utf-8

import os
import sys
import getopt

help1="""
        Скрипт создания нового виртуального хоста
        Принимает параметры:
        -n имя сайта
        -r параметр DocumentRoot
        -d полное имя каталога сайта 
        (если не задан считается равным DocumentRoot )
        
"""

vhost_tpl = 'vhost.tpl' #имя файла шаблона конфига для Apache
apache_vhost_configs = '/etc/apache2/sites-available/' #каталог конфигов виртуальных хостов

try:
    optlist, args = getopt.getopt(sys.argv[1:],'sdn:r:')
    #print optlist
    server_name = filter(lambda item: item[0]=='-n',optlist)[0][1]
    document_root = filter(lambda item: item[0]=='-r',optlist)[0][1]
except:
    print 'Usage %s [-s] -n <site_name> -d <site_dir> -r <document_root>' % sys.argv[0]
    exit(1)

if '-d' in map(lambda item: item[0],optlist):
    site_dir = filter(lambda item: item[0]=='-d',optlist)[0][1]
else:
    site_dir = document_root

if '-s' not in map(lambda item: item[0],optlist):
    print help1
 
 
try:
    f = open(vhost_tpl, 'r');
    host_config = f.read()
    host_config = host_config.replace('@server_name@', server_name)
    host_config = host_config.replace('@document_root@', document_root)
    f.close()
except:
    print 'Cant\' open file %s' % vhost_tpl
    exit(1)


try:
    conf_file = apache_vhost_configs + server_name.split('.')[0] + '.conf'   
    f = open(conf_file, 'w')
    f.write(host_config)
    f.close()
except:
    print 'Can\'t write to file %s' % conf_file
    exit(1)

if not site_dir == document_root:
    command = "mkdir " + site_dir
    os.system(command)

command = "mkdir " + document_root
os.system(command)

try:
    index_file = document_root + '/index.php'   
    f = open(index_file, 'w')
    f.write('<?php phpinfo();?>')
    f.close()
except:
    print 'Can\'t write to file %s' % index_file
    exit(1)

command = "a2ensite " + server_name.split('.')[0] + '.conf'
os.system(command)

command = "service apache2 restart"
os.system(command)

command = "chmod -R 777 " + document_root
os.system(command)

try:
    hosts_file = '/etc/hosts'   
    f = open(hosts_file, 'a+')
    f.write("\n127.0.0.1  " + server_name)
    f.close()
except:
    print 'Can\'t write to file %s' % hosts_file
    exit(1)
    

    
    



