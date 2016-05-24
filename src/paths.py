#!/usr/bin/env python

from job_path import JOB_PATH
import luigi
import pybel
import os


class Paths:
    def __init__(self, mypdb):
        self.mypdb = mypdb
        self.pdb_path = JOB_PATH[self.mypdb]


class SeparatePdb(luigi.Task):
    mypdb = luigi.Parameter()

    def output(self):
        path = Paths(self.mypdb)
        sdf = path.pdb_path + '.lig.sdf'
        pdb = path.pdb_path + '.prt.pdb'
        return [luigi.LocalTarget(p) for p in [sdf, pdb]]

    def run(self):
        path = Paths(self.mypdb).pdb_path
        with open(path, 'r') as ifs:
            content = ifs.readlines()
            HETATM_lines = [line for line in content if 'HETATM' in line]
            non_HETATM_lines = [line for line in content
                                if 'HETATM' not in line]
            lig = pybel.readstring('pdb', ''.join(HETATM_lines))
            sdf, pdb = self.output()
            lig.write('sdf', sdf.path, overwrite=True)
            with open(pdb.path, 'w') as ofs:
                ofs.writelines(non_HETATM_lines)


def test():
    mypdb = "BDB00000001-000-T0000-1crpA06.mod.pdb"
    luigi.build([SeparatePdb(mypdb)], local_scheduler=True)


def main(mypdb):
    luigi.build([SeparatePdb(mypdb)], local_scheduler=True)


if __name__ == '__main__':
    # import sys
    # main(sys.argv[1])
    test()
