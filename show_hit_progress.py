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
    print 'Checking HIT %d / %d' % (idx + 1, len(hit_ids))
    try:
      hit = mtc.get_hit(hit_id)[0]
    except:
      print 'Can\'t find hit id: %d' % (hit_id)
      continue
    total = int(hit.MaxAssignments)
    completed = 0
    for a in mtc.get_assignments(hit_id):
      s = a.AssignmentStatus
      if s == 'Submitted' or s == 'Approved' or s == 'Rejected':
        completed += 1
    counter.update([(completed, total)])

  for (completed, total), count in counter.most_common():
    print '%d / %d: %d' % (completed, total, count)

