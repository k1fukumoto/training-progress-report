import unittest
import sys
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from importer import build_cid_map, load_contact_cert, build_cert_by_month

CFGS = {
    'cert_acronyms': ['VSP','VTSP','VCP6-DCV','VCA-DCV','VSP - CP','VOP-CP'],
    'date_range': {'start': datetime(2013,7,1),
                   'end': datetime(2015,8,1),
                   'step': relativedelta(months=+1)}
}

class TestBuildCIDMap(unittest.TestCase):
    def setUp(self):
        self.certlist = CFGS['cert_acronyms']
        self.data = build_cid_map(self.certlist)

    def test_loaded_data(self):
        keys = sorted(self.data['forward'].keys())
        self.assertListEqual(sorted(keys),sorted(self.certlist))

        for cert in self.certlist:
            ids = self.data['forward'][cert]
            self.assertTrue(self,len(ids) > 0)
            for id in ids:
                self.assertEqual(self.data['reverse'][id],cert)

class TestBuildCertByMonth(unittest.TestCase):
    def setUp(self):
        self.certlist = CFGS['cert_acronyms']
        self.scsv = ''
        with open('sample/cert_and_contact.csv', 'r') as f:
            self.scsv = f.read()

    def test_cert_by_month(self):
        cc = load_contact_cert(self.scsv,self.certlist)

        counts_a = {'ad':defaultdict(int), 'ed':defaultdict(int)}
        for email, certdict in cc.items():
            for cert in certdict:
                self.assertTrue(cert in self.certlist)
                for dtype in ['ad','ed']:
                    self.assertTrue(dtype in certdict[cert])
                    if len(certdict[cert][dtype])>0:
                        counts_a[dtype][cert] += 1

        for cert in self.certlist:
            self.assertTrue(cert in counts_a[dtype])
            self.assertGreaterEqual(counts_a['ed'][cert],counts_a['ad'][cert])

        counts_b = {'ad':defaultdict(int), 'ed':defaultdict(int)}
        for cdate, cdict in build_cert_by_month(self.scsv,CFGS).items():
            for cert, cntdict in cdict.items():
                for dtype in ['ad','ed']:
                    counts_b[dtype][cert] += cntdict[dtype]

        for dtype in ['ad','ed']:
            for cert in counts_a[dtype]:
                try:
                    self.assertEqual(counts_a[dtype][cert],counts_b[dtype][cert])
                except:
                    print "{}:{} - {} != {}".format(dtype,cert,counts_a[dtype][cert],counts_b[dtype][cert])
                    pass

if __name__ == '__main__':
    unittest.main()