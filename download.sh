#!/usr/bin/env bash

set -euo pipefail

version=b156
curl="/bin/curl -sSL"
target="/shares/hii/bioinfo/ref/ncbi/snp/archive/${version}/JSON"
url="https://ftp.ncbi.nlm.nih.gov/snp/archive/${version}/JSON"


list="
$(echo refsnp-chr{{1..22},X,Y,MT}.json.bz2)
refsnp-merged.json.bz2
refsnp-withdrawn.json.bz2
CHECKSUMS
"

echo /bin/mkdir -p ${target}

for item in ${list}; do
  echo "${curl} -sSL ${url}/${item} > ${target}/${item}"
done
