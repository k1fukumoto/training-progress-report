import csv

report = {}
target_cert_ids = {}

def init_report(acronyms):
    for a in acronyms:
        report[a] = {'ids':set(), 'passers':set()}
    load_trainings()
    load_certifications()

def load_trainings():
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
            if acronym in report:
                for id in cert_ids:
                    if len(id) > 0:
                        report[acronym]['ids'].add(id)
                        target_cert_ids[id] = acronym

def load_certifications():
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
            if acronym in report:
                for id in cert_ids:
                    try:
                        if len(id) > 0:
                            report[acronym]['ids'].add(id)
                            target_cert_ids[id] = acronym
                    except: pass

def import_cert_and_contact(scsv):
    init_report(['VSP','VTSP','VCP6-DCV','VCA-DCV','VSP - CP','VOP-CP'])

    reader = csv.reader(scsv.split('\n'), delimiter=',')
    for row in reader:
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
        except: pass
        if(certification_id in target_cert_ids):
            report[target_cert_ids[certification_id]]['passers'].add(email)

    ret = {}
    for k in report:
        ret[k] = len(report[k]['passers'])
    return ret

