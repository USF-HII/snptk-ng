import bz2
import json
import sqlite3
import sys

# API: https://api.ncbi.nlm.nih.gov/variation/v0/ (under /refsnp/{rsid})


def get_snps(fname):

    with bz2.open(fname) as f:
        for line in f:
            rs_obj = json.loads(line)
            rsid = rs_obj["refsnp_id"]

            if "primary_snapshot_data" in rs_obj:
                for alleleinfo in rs_obj["primary_snapshot_data"]["placements_with_allele"]:

                    if (
                        alleleinfo["is_ptlp"]
                        and len(alleleinfo["placement_annot"]["seq_id_traits_by_assembly"])
                        > 0
                    ):
                        assembly_name = alleleinfo["placement_annot"][
                            "seq_id_traits_by_assembly"
                        ][0]["assembly_name"]

                        for a in alleleinfo["alleles"]:
                            spdi = a["allele"]["spdi"]
                            if spdi["inserted_sequence"] != spdi["deleted_sequence"]:
                                (ref, alt, pos, seq_id) = (
                                    spdi["deleted_sequence"],
                                    spdi["inserted_sequence"],
                                    spdi["position"],
                                    spdi["seq_id"],
                                )
                                break

                        yield (int(rsid), int(pos))

                        #print("\t".join([assembly_name, seq_id, str(pos), ref, alt]))



#for snp in get_snps("test.json.bz2"):
#    print(snp[0])
#
#sys.exit(0)

chromosome = 21
#fname = "test.json.bz2"
fname = f"/shares/hii/bioinfo/ref/ncbi/snp/archive/b156/JSON/refsnp-chr{chromosome}.json.bz2"


c = sqlite3.connect("tmp/dbsnp.db")

c.execute("DROP TABLE IF EXISTS snps")

c.execute("CREATE TABLE snps (rsid INTEGER PRIMARY KEY, chromosome INTEGER, position INTEGER)")

c.execute("CREATE INDEX snps_ix ON snps (chromosome, position)")

c.executemany("INSERT INTO snps VALUES (?, ?, ?)", ((snp[0], chromosome, snp[1]) for snp in get_snps(fname)))

c.commit()


"""
db = build_db_merged(
    "/shares/hii/bioinfo/ref/ncbi/snp/archive/b156/JSON/refsnp-merged.json.bz2"
)

print("start")

c = sqlite3.connect("tmp/snptk2.db")

c.execute("DROP TABLE IF EXISTS merged")

c.execute("CREATE TABLE merged (rsid INTEGER PRIMARY KEY, rsid_merged INTEGER)")

c.executemany("INSERT INTO merged VALUES (?, ?)", ((k, db[k][0]) for k in sorted(db)))

c.commit()


def printPlacements(info):
    '''
    rs genomic positions
    '''

    for alleleinfo in info:
        # has top level placement (ptlp) and assembly info
        if alleleinfo['is_ptlp'] and \
                len(alleleinfo['placement_annot']
                    ['seq_id_traits_by_assembly']) > 0:
            assembly_name = (alleleinfo['placement_annot']
                                       ['seq_id_traits_by_assembly']
                                       [0]['assembly_name'])

            for a in alleleinfo['alleles']:
                spdi = a['allele']['spdi']
                if spdi['inserted_sequence'] != spdi['deleted_sequence']:
                    (ref, alt, pos, seq_id) = (spdi['deleted_sequence'],
                                               spdi['inserted_sequence'],
                                               spdi['position'],
                                               spdi['seq_id'])
                    break
            print("\t".join([assembly_name, seq_id, str(pos), ref, alt]))


parser = argparse.ArgumentParser(
    description='Example of parsing JSON RefSNP Data')
parser.add_argument(
    '-i', dest='input_fn', required=True,
    help='The name of the input file to parse')

args = parser.parse_args()


cnt = 0
with gzip.open(args.input_fn, 'rb') as f_in:
    for line in f_in:
        rs_obj = json.loads(line.decode('utf-8'))
        print(rs_obj['refsnp_id'] + "\t")  # rs ID

        if 'primary_snapshot_data' in rs_obj:
            printPlacements(
                rs_obj['primary_snapshot_data']['placements_with_allele'])
            printAllele_annotations(rs_obj['primary_snapshot_data'])
            print("\n")

        cnt = cnt + 1
        if (cnt > 1000):
            break
"""
