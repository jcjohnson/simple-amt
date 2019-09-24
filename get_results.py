import argparse, json

import simpleamt
import sys
import os
import re

def process_assignments(mtc, hit_id, status):
  results = []
  paginator = mtc.get_paginator('list_assignments_for_hit')
  try:
    for a_page in paginator.paginate(HITId=hit_id, PaginationConfig={'PageSize': 100}):
        for a in a_page['Assignments']:
          if a['AssignmentStatus'] not in status:
            continue
          answer = json.loads(re.search(r'<FreeText>(?P<answer>.*?)</FreeText>', a['Answer'])['answer'])
          results.append({
           'assignment_id': a['AssignmentId'],
            'hit_id': hit_id,
            'worker_id': a['WorkerId'],
            'output': answer,
            'submit_time': str(a['SubmitTime']),
          })
  except mtc.exceptions.RequestError:
    print('Bad hit_id %s' % str(hit_id), file=sys.stderr)
    return results

  return results

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  parser.add_argument('--output_file')
  parser.add_argument('--rejected', action='store_true', dest='rejected',
                      default=False,
                      help="Whether to also fetch the rejected hits.")
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)

  results = []
  status = ['Approved', 'Submitted']
  if args.rejected:
    status = ['Approved', 'Submitted', 'Rejected']

  if args.hit_ids_file is None:
    for hit in mtc.get_all_hits():
      results += process_assignments(mtc, hit.HITId, status)
  elif args.output_file != None and os.path.isfile(args.output_file):
    hit_dict = {}
    for line in open(args.output_file, 'r'):
      output = json.loads(line)
      hit_dict[output['hit_id']] = output
    for line in open(args.hit_ids_file, 'r'):
      hit_id = line.strip()
      if hit_id in hit_dict:
        results += output
      else:
        results += process_assignments(mtc, hit_id, status)
  else:
    with open(args.hit_ids_file, 'r') as f:
      for line in f:
        hit_id = line.strip()
        results += process_assignments(mtc, hit_id, status)

  for assignment_result in results:
    print(json.dumps(assignment_result))

