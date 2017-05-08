#!/usr/bin/python

# Script til at liste interface og description
# Copyright Torben Rask Petersen - torben.rask.petersen@rsyd.dk

import paramiko
import getpass
import sys
import os
import time

#print " "
#print " Et lille script til at liste interface og description "
#print " "

def interface_description(host):
  des_found = False
  vlan_found = False
  int_found = False
  client = paramiko.SSHClient()
  #client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host, username=user, password=pw, timeout=10)
  stdin, stout, sterr = client.exec_command('sh run')
  for line in stout:

      if line.find('hostname ') >=0:
         hostline = line.strip('\r\n')
         hostname = hostline.strip('hostname ')

      if line.find('interface ') >=0:
         inter = line.strip('\r\n')
         interface = inter.strip('interface ')
         int_found = True

      if line.find('description ') >=0:
         des = line.strip('\r\n')
         slut = len(des)
         description = des[13:slut]
         des_found = True
     
      if line.find('switchport access vlan ') >=0:
#         if des_found == False:
#            description = " "
         vlanline = line.strip('\r\n') 
         vlan = vlanline.strip('switchport access vlan ')
         vlan_found = True

      if line.find('!') >=0 and int_found:
         #print host+";"+vlan+";"+interface+";"+description
         if des_found == False:
            description = " "
         if vlan_found == False:
            vlan = " "
         
         outputfile.write(host+";"+hostname+";"+vlan+";"+interface+";"+description+"\n")
         des_found = False
         vlan_found = False
         int_found = False

  client.close()

#user = input("Indtast brugerid: ")
#pw = getpass.getpass()
user="adm-ype2ub"
pw="KullenAugust2018"

hostfile = open('switche_vs.txt','r')
outputfile = open('port_des.txt','w')
outputfile.write("IP-adresse;Switchnavn;Vlan;Interface;Port-Description\n")

for line in hostfile:
    time.sleep(2)
    host = line.strip('\r\n')
    print('Behandler nu switch: ',host)
    ping = os.system("ping -n 1 " + host + ">null")
    if ping == 0:
       interface_description(host)
    else:
       print(host,'svarer ikke paa ping !')  

hostfile.close()
outputfile.close()



