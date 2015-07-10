import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict


'''
 Certification ID Map
 {
   'forward': {
       'VCP': [cert_id1, cert_id2, cert_id3],
       'VSP': [cert_id4, cert_id5, cert_id6],
       'VSTP': [cert_id7, cert_id8, cert_id9],
    },
    'reverse': {
       cert_id1: 'VCP',
       cert_id4: 'VSP',
       cert_id7: 'VSTP',
    }
 }
'''

def build_cid_map(acronyms):
    cid_map = {'forward':{}, 'reverse':{}}

    for a in acronyms:
        cid_map['forward'][a] = set()

    with open('./data/trainings.csv','rb') as f:
        reader = csv.reader(f)
        cert_ids = [0]*6
        for row in reader:
            category, \
            focus_product, \
            cb_version, \
            acronym, \
            naming_convention, \
            official_course_name, \
            ga, \
            duration, \
            cost, \
            delivery_mode,\
            delivery_location,\
            course_url,\
            acronym,\
            cert_ids[0],\
            cert_ids[1],\
            cert_ids[2],\
            cert_ids[3],\
            cert_ids[4],\
            cert_ids[5] = row
            if acronym in cid_map['forward']:
                for id in cert_ids:
                    if len(id) > 0:
                        cid_map['forward'][acronym].add(id)
                        cid_map['reverse'][id] = acronym

    with open('./data/certifications.csv','rb') as f:
        reader = csv.reader(f)
        cert_ids = [0]*6
        for row in reader:
            cb_version,\
            acronym,\
            exam,\
            type,\
            duration,\
            cost,\
            waived,\
            public_information,\
            acronym,\
            cert_ids[0],\
            cert_ids[1],\
            cert_ids[2],\
            cert_ids[3],\
            cert_ids[4] = row
            if acronym in cid_map['forward']:
                for id in cert_ids:
                    try:
                        if len(id) > 0:
                            cid_map['forward'][acronym].add(id)
                            cid_map['reverse'][id] = acronym
                    except: pass
    return cid_map

'''
 Import Dictionary Format
 {
   2015/07/01: {
     'VCP': [passer1, passer2, passer3],
     'VSP': [passer1, passer2, passer3],
     'VSTP': [passer1, passer2, passer3],
   },
   2015/07/01: {
     'VCP': [passer1, passer2, passer3],
     'VSP': [passer1, passer2, passer3],
     'VSTP': [passer1, passer2, passer3],
   },
   2015/07/01: {
     'VCP': [passer1, passer2, passer3],
     'VSP': [passer1, passer2, passer3],
     'VSTP': [passer1, passer2, passer3],
   }
 }
'''
def init_import_dict(start,end,step,acronyms):
    impd = defaultdict(dict)
    c = start
    while c < end:
        for a in acronyms:
            impd[c][a] = set()
        c += step
    return impd

def load_cert_and_contact(scsv,acronyms):
    d0 = datetime(2014,7,1)
    d1 = datetime(2015,6,1)
    derr = datetime(1900,1,1)

    cid_map = build_cid_map(acronyms)
    impd = init_import_dict(d0,d1,relativedelta(months=+1),acronyms)

    reader = csv.reader(scsv.split('\n'), delimiter=',')
    for row in reader:
        certification_id = ""
        email = ""
        attained_date = ""
        ad = derr
        try:
            geo, \
            region, \
            country, \
            first_name, \
            last_name, \
            email, \
            domain_name, \
            certification_id, \
            certication_type, \
            certification_desc, \
            attained_date, \
            enrolled_date,\
            active_flag = row

            if len(attained_date)>0:
                ad = datetime.strptime(attained_date,'%Y/%m/%d')
                ad = ad.replace(day=1)
        except: pass

        if certification_id in cid_map['reverse']:
            if ad in impd:
                impd[ad][cid_map['reverse'][certification_id]].add(email)
            elif ad != derr:
                impd[d0][cid_map['reverse'][certification_id]].add(email)

    return impd

'''
Report Format
  Date,VCP,VSP,VTSP
  2015/07/1,10,20,20
  2015/08/1,13,22,23
  2015/09/1,20,30,40
   ...
 ]
'''
def import_cert_and_contact(scsv):
    acronyms = ['VSP','VTSP','VCP6-DCV','VCA-DCV','VSP - CP','VOP-CP']
    rep = [','.join(['Date'] + acronyms)]

    cc = load_cert_and_contact(scsv,acronyms)
    prev_cnt = defaultdict(int)
    for d in sorted(cc):
        row = [datetime.strftime(d,'%Y/%m/%d')]
        for a in acronyms:
            cnt = len(cc[d][a]) + prev_cnt[a]
            row.append(str(cnt))
            prev_cnt[a] = cnt
        rep.append(','.join(row))

    return '\n'.join(rep)







