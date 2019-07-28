import argparse, json
import simpleamt
import sys
from itertools import chain
"""
Run with --prod to get all the hits from production.
"""

def get_all_reviewable_hits(mtc):
  paginator = mtc.get_paginator('list_hits')
  all_hits = []
  for i, batch in enumerate(paginator.paginate(PaginationConfig={'PageSize': 100})):
      print("Request hits page %i" % (i + 1))
      all_hits.extend(batch['HITs'])
  return all_hits

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)
  hits = get_all_reviewable_hits(mtc)
  print (len(hits))
