import argparse
from collections import Counter

import simpleamt


if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  args = parser.parse_args()

  mtc = simpleamt.get_mturk_connection_from_args(args)

  if args.hit_ids_file is None:
    parser.error('Must specify hit_ids_file')

  with open(args.hit_ids_file, 'r') as f:
    hit_ids = [line.strip() for line in f]

  counter = Counter()
  for idx, hit_id in enumerate(hit_ids):
    print('Checking HIT %d / %d' % (idx + 1, len(hit_ids)))
    try:
      hit = mtc.get_hit(HITId=hit_id)['HIT']
    except:
      print('Can\'t find hit id: %s' % (hit_id))
      continue
    total = int(hit['MaxAssignments'])
    completed = 0
    paginator = mtc.get_paginator('list_assignments_for_hit')
    for a_page in paginator.paginate(HITId=hit_id, PaginationConfig={'PageSize': 100}):
        for a in a_page['Assignments']:
            if a['AssignmentStatus'] in ['Submitted', 'Approved', 'Rejected']:
                completed += 1
    counter.update([(completed, total)])

  for (completed, total), count in counter.most_common():
    print('%d / %d: %d' % (completed, total, count))
