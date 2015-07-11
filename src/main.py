from importer import import_cert_and_contact
from datetime import datetime
from dateutil.relativedelta import relativedelta

import sys

report_configs = {
  'cert_acronyms': ['VSP','VTSP','VCP6-DCV','VCA-DCV','VSP - CP','VOP-CP'],
  'date_range': {'start': datetime(2013,7,1),
                 'end': datetime(2015,8,1),
                 'step': relativedelta(months=+1)
                 }
}

csv_data = ''
with open(sys.argv[1], 'r') as f:
    csv_data = f.read()

print import_cert_and_contact(csv_data,'ad',report_configs)
print import_cert_and_contact(csv_data,'ed',report_configs)

