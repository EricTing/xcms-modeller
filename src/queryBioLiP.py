#!/usr/bin/env python

from paths import SeparatePdb, Paths
from biolip import BioLipReferencedSpearmanR
import pandas as pd
import luigi
import os


class QueryBioLiP(SeparatePdb):
    def requires(self):
        return SeparatePdb(self.mypdb)

    def run(self):
        sdf, pdb = self.requires().output()
        query = BioLipReferencedSpearmanR(sdf.path, pdb.path, title=self.mypdb)
        minimum_tani = 0.5
        result = query.calculate(maximum_search_results=500, tani=minimum_tani)

        dat = {}
        for l in result:
            dat[l[0]] = l[1]

        df = pd.DataFrame(dat).T
        df.to_csv(self.output().path)

    def output(self):
        ofn = os.path.join(Paths(self.mypdb).work_dir, self.mypdb + '.csv')
        return luigi.LocalTarget(ofn)


def main(mypdb):
    luigi.build([QueryBioLiP(mypdb)], local_scheduler=True)


def test():
    mypdb = "BDB00035804-000-T0002-3vgaA00.mod.pdb"
    luigi.build([QueryBioLiP(mypdb)], local_scheduler=True)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
    # test()
