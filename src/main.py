from importer import import_cert_and_contact
import sys

csv_data = ''
with open(sys.argv[1], 'r') as f:
    csv_data = f.read()

print import_cert_and_contact(csv_data)
