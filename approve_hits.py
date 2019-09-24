import argparse, json
import simpleamt
import re

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  parser.add_argument('-f', action='store_true', default=False)
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)

  approve_ids = []
  reject_ids = []

  if args.hit_ids_file is None:
    parser.error('Must specify --hit_ids_file.')

  with open(args.hit_ids_file, 'r') as f:
    hit_ids = [line.strip() for line in f]

  for hit_id in hit_ids:
    paginator = mtc.get_paginator('list_assignments_for_hit')
    try:
      for a_page in paginator.paginate(HITId=hit_id, PaginationConfig={'PageSize': 100}):
        for a in a_page['Assignments']:
          if a['AssignmentStatus'] == 'Submitted':
            try:
              # Try to parse the output from the assignment. If it isn't
              # valid JSON then we reject the assignment.
              json.loads(re.search(r'<FreeText>(?P<answer>.*?)</FreeText>', a['Answer'])['answer'])
              approve_ids.append(a['AssignmentId'])
            except ValueError as e:
              reject_ids.append(['AssignmentId'])
          else:
            print("hit %s has already been %s" % (str(hit_id), a['AssignmentStatus']))
    except mtc.exceptions.RequestError:
      continue

  print('This will approve %d assignments and reject %d assignments with '
         'sandbox=%s' % (len(approve_ids), len(reject_ids), str(args.sandbox)))
  print('Continue?')

  if not args.f:
    s = input('(Y/N): ')
  else:
    s = 'Y'
  if s == 'Y' or s == 'y':
    print('Approving assignments')
    for idx, assignment_id in enumerate(approve_ids):
      print('Approving assignment %d / %d' % (idx + 1, len(approve_ids)))
      mtc.approve_assignment(AssignmentId=assignment_id)
    for idx, assignment_id in enumerate(reject_ids):
      print('Rejecting assignment %d / %d' % (idx + 1, len(reject_ids)))
      mtc.reject_assignment(AssignmentId=assignment_id, RequesterFeedback='Invalid results')
  else:
    print('Aborting')
