#!/bin/sh
# usage: run_census.sh WORD TAG MODE
cd /private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/r8
/private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/venv/bin/python -B tools/$4 $1 cands/$2.json $3
IMB_ROOT=$HOME/imb-r6c /private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/venv/bin/python -B tools/price_all.py $1 cands/$2.json cands/$2-price.json 10
