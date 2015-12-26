#!/usr/bin/env python
# Dimitrios Glentadakis <dglent@free.fr>
# Purpose: Convert a vcard3.0 vcf file to Trojita addressbook and sort by name
# License: GPLv3
#
# Usage: place the script in the folder ~/.abook/
# where you have the file addressbook of Trojita.
# To only sort by name the contacts in Trojita, run the script without
# any argument.
# To import contacts from a vcf file run the script with the contacts
# file as argument:
# <python vcf2addressbook.py contacts.vcf> this will OVERWRITE
# the 'addressbook' file and the existing contacts will be lost.

import vobject
import io
import sys


class Vcf2addressbook(object):

    def __init__(self, vcf_file):
        fname = vcf_file
        self.aa_list = []
        self.catalog = {}
        self.names = []
        self.newfile = []
        self.total_contacts = 0
        self.fn_addressbook = "addressbook"
        try:
            with open(self.fn_addressbook, 'r') as ff:
                self.addressbook = ff.readlines()
        except IOError:
            self.addressbook = []
        if fname != '':
            stream = io.open(fname, "r", encoding="utf-8")
            self.vcards = vobject.readComponents(stream)
            self.add_vcf()
            print('Imported {} contacts'.format(self.total_contacts))
        else:
            if len(self.addressbook) == 0:
                print('Missing or empty addressbook file... nothing done')
                return
            for i in self.addressbook:
                if i == '\n':
                    continue
                if i[:5] == "name=":
                    self.names.append(i[5:-1])
                ai = i.strip()
                if ai[0] == '[' and ai[-1] == ']':
                    aa = ai
                    self.catalog[aa] = []
                    continue
                self.catalog[aa].append(i)
        self.sort()
        self.write_file()

    def add_vcf(self):
        aa = 0
        for vcard in self.vcards:
            details = []
            address = ['address=']
            code = ['zip=']
            city = ['city=']
            region = ['state=']
            country = ['country=']
            fax = ['fax=']
            mobile = ['mobile=']
            phone = ['phone=']
            workphone = ['workphone=']
            email = ['email=']
            url = ['url=']
            aa += 1
            cat_aa = ('[' + str(aa) + ']')
            fn = vcard.fn.value.encode('utf-8')
            self.total_contacts += 1
            for p in vcard.getChildren():
                attributs = p.params.get("TYPE", [])
                if p.name == "ADR":
                    if p.value.street != '':
                        address.append(p.value.street.encode('utf-8') + '\\n')
                    if p.value.code != '':
                        code.append(p.value.code.encode('utf-8') + '\\n')
                    if p.value.city != '':
                        city.append(p.value.city.encode('utf-8') + '\\n')
                    if p.value.region != '':
                        region.append(p.value.region.encode('utf-8') + '\\n')
                    if p.value.country != '':
                        country.append(p.value.country.encode('utf-8') + '\\n')
                if p.name == 'TEL':
                    if 'FAX' in attributs:
                        if p.value != '':
                            fax.append(p.value.encode('utf-8') + '\\n')
                    if 'WORK' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            workphone.append(p.value.encode('utf-8') + '\\n')
                    if 'HOME' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            phone.append(p.value.encode('utf-8') + '\\n')
                    if 'CELL' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            mobile.append(p.value.encode('utf-8') + '\\n')
                    if len(attributs) == 0:
                        if p.value != '':
                            phone.append(p.value.encode('utf-8') + '\\n')
                if p.name == 'URL':
                    if p.name != '':
                        url.append(p.value.encode('utf-8').
                                   replace('http\://', 'http://') + '\\n')
                if p.name == 'EMAIL':
                    if p.value != '':
                        email.append(p.value.encode('utf-8') + '\\n')
            if fn == '':
                try:
                    fn = email[1][:-2]
                except:
                    fn = str(aa)
            self.names.append(fn)
            details.append('name=' + fn + '\n')
            if len(email) >= 2:
                email[-1] = email[-1][:-2]
                email.append('\n')
                ema = ''.join(i for i in email)
                details.append(ema)
            if len(url) >= 2:
                url[-1] = url[-1][:-2]
                url.append('\n')
                ur = ''.join(i for i in url)
                details.append(ur)
            if len(address) >= 2:
                address[-1] = address[-1][:-2]
                address.append('\n')
                add = ''.join(i for i in address)
                details.append(add)
            if len(city) >= 2:
                city[-1] = city[-1][:-2]
                city.append('\n')
                cit = ''.join(i for i in city)
                details.append(cit)
            if len(code) >= 2:
                code[-1] = code[-1][:-2]
                code.append('\n')
                cod = ''.join(i for i in code)
                details.append(cod)
            if len(region) >= 2:
                region[-1] = region[-1][:-2]
                region.append('\n')
                reg = ''.join(i for i in region)
                details.append(reg)
            if len(country) >= 2:
                country[-1] = country[-1][:-2]
                country.append('\n')
                cou = ''.join(i for i in country)
                details.append(cou)
            if len(fax) >= 2:
                fax[-1] = fax[-1][:-2]
                fax.append('\n')
                fa = ''.join(i for i in fax)
                details.append(fa)
            if len(mobile) >= 2:
                mobile[-1] = mobile[-1][:-2]
                mobile.append('\n')
                mob = ''.join(i for i in mobile)
                details.append(mob)
            if len(phone) >= 2:
                phone[-1] = phone[-1][:-2]
                phone.append('\n')
                pho = ''.join(i for i in phone)
                details.append(pho)
            if len(workphone) >= 2:
                workphone[-1] = workphone[-1][:-2]
                workphone.append('\n')
                wor = ''.join(i for i in workphone)
                details.append(wor)
            self.catalog[cat_aa] = details

    def sort(self):
        self.names.sort(key=str.lower)
        counter = []
        for e, n in enumerate(self.names):
            counter.append(str(e))
        counter.sort()
        count = 0
        for i in self.names:
            self.newfile.append('[' + counter[count] + ']\n')
            for k, l in self.catalog.items():
                for d in l:
                    if d[5:-1] == i:
                        for item in l:
                            self.newfile.append(item)
            self.newfile.append('\n')
            count += 1
        if self.newfile[-1] == '\n':
            del self.newfile[-1]

    def write_file(self):
        with open(self.fn_addressbook, 'wb') as out_file:
            out_file.writelines(self.newfile)

        if self.addressbook != self.newfile:
            with open(self.fn_addressbook + '.bak', 'wb') as out_bak:
                out_bak.writelines(self.addressbook)

if __name__ == '__main__':
    ff = ''
    if len(sys.argv) == 2:
        ff = sys.argv[1]
    out = Vcf2addressbook(ff)
