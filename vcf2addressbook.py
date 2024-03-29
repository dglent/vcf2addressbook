#!/usr/bin/env python
#
# *******************************************************************
# Convert a vcard3.0 vcf file to Trojita addressbook and sort by name
# *******************************************************************
#
# Dimitrios Glentadakis <dglent@free.fr>
#
# License: GPLv3
#
# Usage:
# ======
# Place the script in the folder ~/.abook/
# where you have the file addressbook of Trojita.
# To only sort by name the contacts in Trojita, run the script without
# any argument.
# To import contacts from a vcf file run the script with the contacts
# file as argument:
# <python vcf2addressbook.py contacts.vcf> this OVERWRITES
# the 'addressbook' file and the existing contacts will be lost.

import sys
try:
    import vobject
except:
    print('Please install the python-vobject package')
    sys.exit()
import io


class Vcf2addressbook(object):

    def __init__(self, vcf_file):
        fname = vcf_file
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
                record = i.strip()
                if record[0] == '[' and record[-1] == ']':
                    id_ = record
                    self.catalog[id_] = []
                    continue
                self.catalog[id_].append(i)
        self.sort()
        self.write_file()

    def add_vcf(self):
        id_ = 0
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
            notes = ['notes=']
            id_ += 1
            cat_id_ = ('[' + str(id_) + ']')
            try:
                fn = vcard.fn.value
            except AttributeError:
                fn = ''
            self.total_contacts += 1
            for p in vcard.getChildren():
                attributs = p.params.get("TYPE", [])
                if p.name == "ADR":
                    if p.value.street != '':
                        address.append(f'{p.value.street}\n')
                    if p.value.code != '':
                        code.append(f'{p.value.code}\n')
                    if p.value.city != '':
                        city.append(f'{p.value.city}\n')
                    if p.value.region != '':
                        region.append(f'{p.value.region}\n')
                    if p.value.country != '':
                        country.append(f'{p.value.country}\n')
                if p.name == 'TEL':
                    if 'FAX' in attributs:
                        if p.value != '':
                            fax.append(f'{p.value}\n')
                    if 'WORK' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            workphone.append(f'{p.value}\n')
                    if 'HOME' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            phone.append(f'{p.value}\n')
                    if 'CELL' in attributs and 'FAX' not in attributs:
                        if p.value != '':
                            mobile.append(f'{p.value}')
                    if len(attributs) == 0:
                        if p.value != '':
                            phone.append(f'{p.value}')
                if p.name == 'URL':
                    if p.name != '':
                        url.append(
                            f"{p.value}\n".replace('http\://', 'http://')
                        )
                if p.name == 'EMAIL':
                    if p.value != '':
                        email.append(f'{p.value}')
                if p.name == 'NOTE':
                    if p.value != '':
                        notes.append(f'{p.value}')
            if fn == '':
                try:
                    fn = email[1][:-2]
                except:
                    fn = str(id_)

            self.names.append(fn)
            details.append(f"name={fn}\n")
            if len(email) >= 2:
                email[-1] = ' ' + email[-1]
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
            if len(notes) >= 2:
                notes[-1] = notes[-1][:-2]
                notes.append('\n')
                note = ''.join(i for i in notes)
                details.append(note)
            self.catalog[cat_id_] = details

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
        with open(self.fn_addressbook, 'w') as out_file:
            out_file.writelines(self.newfile)

        if self.addressbook != self.newfile:
            with open(self.fn_addressbook + '.bak', 'w') as out_bak:
                out_bak.writelines(self.addressbook)

if __name__ == '__main__':
    ff = ''
    if len(sys.argv) == 2:
        ff = sys.argv[1]
    out = Vcf2addressbook(ff)
