import unittest
import sys
from collections import defaultdict
from importer import build_cid_map, load_contact_cert

CERTLIST = ['VSP','VTSP','VCP6-DCV','VCA-DCV']

class TestBuildCIDMap(unittest.TestCase):
    def setUp(self):
        self.certlist = CERTLIST
        self.data = build_cid_map(self.certlist)

    def test_loaded_data(self):
        keys = sorted(self.data['forward'].keys())
        self.assertListEqual(sorted(keys),sorted(self.certlist))

        for cert in self.certlist:
            ids = self.data['forward'][cert]
            self.assertTrue(self,len(ids) > 0)
            for id in ids:
                self.assertEqual(self.data['reverse'][id],cert)


class TestLoadContactCert(unittest.TestCase):
    def setUp(self):
        self.certlist = CERTLIST
        scsv = ''
        with open('sample/cert_and_contact.csv', 'r') as f:
            scsv = f.read()
        self.data = load_contact_cert(scsv,self.certlist)

    def test_loaded_data(self):
        counts = {'ad':defaultdict(int), 'ed':defaultdict(int)}

        for email, certdict in self.data.items():
            for cert in certdict:
                self.assertTrue(cert in self.certlist)
                for dtype in ['ad','ed']:
                    self.assertTrue(dtype in certdict[cert])
                    if len(certdict[cert][dtype])>0:
                        counts[dtype][cert] += 1

        for cert in self.certlist:
            self.assertTrue(cert in counts['ad'])
            print "## {}: {}".format(cert,counts['ad'][cert])

if __name__ == '__main__':
    unittest.main()