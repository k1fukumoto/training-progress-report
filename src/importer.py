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
Compact Contact-Cert List
{
  email1: {
     VCP: {
       ad: [date1, date2,...]
       ed: [data1, date2,...]
     },
     VSP: {
       ad: [date1, date2,...]
       ed: [data1, date2,...]
     }
  },
  email2: {
  ...
  }
'''
def load_contact_cert(scsv,acronyms):
    derr = datetime(1900,1,1)
    cid_map = build_cid_map(acronyms)

    ret = defaultdict(dict)
    reader = csv.reader(scsv.split('\n'), delimiter=',')
    for row in reader:
        certification_id = ""
        email = ""
        ad = derr
        ed = derr
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
            if len(enrolled_date)>0:
                ed = datetime.strptime(enrolled_date,'%Y/%m/%d')
                ed = ed.replace(day=1)
        except: pass

        if certification_id in cid_map['reverse']:
            gname = cid_map['reverse'][certification_id]
            if not gname in ret[email]:
                ret[email][gname] = {'ad':[], 'ed':[]}

            if ed == derr:
                # Enrolled date needs to exit. skip garbage entry
                pass
            elif ad == derr:
                # Not yet attained. Add enrolled date only
                ret[email][gname]['ed'].append(ed)
            elif ed > ad:
                # date inconsistency. Use ad for both
                ret[email][gname]['ad'].append(ad)
                ret[email][gname]['ed'].append(ad)
            else:
                ret[email][gname]['ad'].append(ad)
                ret[email][gname]['ed'].append(ed)
    return ret
'''
 Cert By Month
 {
   2015/07/01: {
     'VCP': {'ad': N0, 'ed': N1},
     'VSP': {'ad': N0, 'ed': N1},
     ...
   },
   2015/07/01: {
     ...
   },
 }
'''
def init_cert_by_month(start,end,step,acronyms):
    ret = defaultdict(dict)
    c = start
    while c < end:
        for a in acronyms:
            ret[c][a] = {'ad':0, 'ed':0}
        c += step
    return ret

def build_cert_by_month(scsv,cfgs):
    acronyms = cfgs['cert_acronyms']

    cc = load_contact_cert(scsv,acronyms)

    ret = init_cert_by_month(cfgs['date_range']['start'],
                             cfgs['date_range']['end'],
                             cfgs['date_range']['step'],
                             acronyms)

    for email in cc:
        for a in cc[email]:
            for dkey in ['ad','ed']:
                dlist = cc[email][a][dkey]
                if len(dlist) > 0:
                    d = min(dlist)
                    if d in ret:
                        ret[d][a][dkey] += 1
                    elif d < cfgs['date_range']['start']:
                        ret[cfgs['date_range']['start']][a][dkey] += 1
    return ret

'''
Report Format
      ,VCP     ,VCP     ,VCP  ,VSP     ,VSP     ,VSP
  Date,Attained,Enrolled,ED-AD,Enrolled,Attained,ED-AD
  2015/07/1,10,20,20
  2015/08/1,13,22,23
  2015/09/1,20,30,40
   ...
 ]
'''

def import_cert_and_contact(scsv,cfgs):
    rows = []
    acronyms = cfgs['cert_acronyms']

    hdr = ['']
    for a in acronyms:
        hdr = hdr + [a]*3
    rows.append(hdr)

    hdr = ['Date']
    for a in acronyms:
        hdr = hdr + ['Attained','Enrolled','ED-AD']
    rows.append(hdr)

    cm_dict = build_cert_by_month(scsv,cfgs)

    prev_cnt = {'ad':defaultdict(int), 'ed':defaultdict(int)}
    for d in sorted(cm_dict):
        row = [datetime.strftime(d,'%Y/%m/%d')]
        for a in acronyms:
            for dkey in ['ad','ed']:
                cnt = cm_dict[d][a][dkey] + prev_cnt[dkey][a]
                row.append(str(cnt))
                prev_cnt[dkey][a] = cnt
            row.append(str(prev_cnt['ed'][a]-prev_cnt['ad'][a]))
        rows.append(row)

    return '\n'.join([ ','.join(row) for row in rows])







