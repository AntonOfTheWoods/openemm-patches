#!/usr/bin/env python
import agn
import re
import os

agn.require('2.3.0')
agn.loglevel = agn.LV_INFO

agn.lock()
agn.log(agn.LV_INFO, 'main', 'Starting up')
db = agn.DBaseID()
if db is None:
        agn.die(s='Failed to setup database interface')
db.log = lambda a: agn.log(agn.LV_DEBUG, 'db', a)

curs = db.cursor()

if curs is None:
        agn.die(s='Failed to get database cursor')

emails = set()

for record in curs.query("select param from mailing_mt_tbl"):
        m = re.search('from=".*?<(.*?)>', record[0])
        if not m.group(1) is None:
                emails.add(m.group(1))

mailloop = "select concat('ext_', b.rid, '@', a.mailloop_domain) from company_tbl a inner join "
mailloop += "mailloop_tbl b on a.company_id = b.company_id where forward_enable = 0 and "
mailloop += "ar_enable = 0 limit 1;"

mailloopAddress = ""

for record in curs.query(mailloop):
        mailloopAddress = record[0]

localFilename = agn.base + os.sep + 'conf' + \
    os.sep + 'bav' + os.sep + 'bav.conf-local'

with open(localFilename, "r") as myfile:
        data = myfile.readlines()

newmails = emails.copy()

for email in emails:
        for alias in data:
                if alias.startswith(email):
                        newmails.remove(email)
                        break
with open(localFilename, "w") as newfile:
        for dataline in data:
                if dataline.strip() != "":
                        newfile.write(dataline.strip() + "\n")
        for newmail in newmails:
                newfile.write(newmail + "\talias:" + mailloopAddress + "\n")
