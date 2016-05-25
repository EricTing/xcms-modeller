#!/usr/bin/env python

from __future__ import print_function

import sys
import pandas as pd
from queryBioLiP import QueryBioLiP

sampled_ifn = "./xcms_mod.sampled.txt"

pdbs = [line.rstrip() for line in file(sampled_ifn)]

all_df = pd.DataFrame()
for mypdb in pdbs:
    task = QueryBioLiP(mypdb)
    if task.complete():
        ifn = task.output().path
        df = pd.read_csv(ifn, index_col=0)
        df = df.rename(columns = {u'spearmanr': u'xcms'})
        df['query'] = mypdb
        df['template'] = df.index
        all_df = all_df.append(df)
    else:
        print("{} Failed".format(mypdb), file=sys.stderr)

all_df.to_csv("../dat/xcms_mod.sampled.csv", index=False)


def main():
    pass


if __name__ == '__main__':
    main()
