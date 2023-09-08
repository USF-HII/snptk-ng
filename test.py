#!/usr/bin/env python3

import bz2
import json
import sqlite3
import sys


def build_db_merged(fname):
    """
    Build a dictionary of snp to merged snp. We must track revision because there may be multiple
    instances of the same snp so we take the highest revision.
    """
    db = {}

    with bz2.open(fname) as f:
        for line in f:
            j = json.loads(line)
            refsnp_id = int(j["refsnp_id"])
            for entry in j["dbsnp1_merges"]:
                merged_rsid = int(entry["merged_rsid"])
                revision = int(entry["revision"])

                if merged_rsid in db:
                    if revision > db[merged_rsid][1]:
                        db[merged_rsid] = (refsnp_id, revision)
                else:
                    db[merged_rsid] = (refsnp_id, revision)

    return db


db = build_db_merged(
    "/shares/hii/bioinfo/ref/ncbi/snp/archive/b156/JSON/refsnp-merged.json.bz2"
)

print("start")

c = sqlite3.connect("tmp/snptk2.db")

c.execute("DROP TABLE IF EXISTS merged")

c.execute("CREATE TABLE merged (rsid INTEGER PRIMARY KEY, rsid_merged INTEGER)")

c.executemany("INSERT INTO merged VALUES (?, ?)", ((k, db[k][0]) for k in sorted(db)))

c.commit()

# /shares/hii/bioinfo/ref/ncbi/snp/archive/b156/JSON/refsnp-merged.json.bz2
# /shares/hii/bioinfo/ref/ncbi/snp/archive/b156/JSON/refsnp-chr21.json.bz2
