import argparse, json

import simpleamt
import sys
import os

def process_assignments(mtc, hit_id, status):
  results = []
  page_number = 1
  while True:
    try:
      assignments = mtc.get_assignments(hit_id, page_number = page_number, page_size=100)
      if len(assignments) == 0:
        return results
    except:
      print >> sys.stderr, ('Bad hit_id %s' % str(hit_id))
      return results
    for a in assignments:
      if a.AssignmentStatus in status:
        try:
          output = json.loads(a.answers[0][0].fields[0])
        except ValueError as e:
          print >> sys.stderr, ('Bad data from assignment %s (worker %s)'
              % (a.AssignmentId, a.WorkerId))
          mtc.reject_assignment(a.AssignmentId, feedback='Invalid results')
          continue
        results.append({
          'assignment_id': a.AssignmentId,
          'hit_id': hit_id,
          'worker_id': a.WorkerId,
          'output': json.loads(a.answers[0][0].fields[0]),
          'submit_time': a.SubmitTime,
        })
    page_number += 1
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
    print json.dumps(assignment_result)

