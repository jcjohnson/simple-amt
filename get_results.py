import argparse, json

import simpleamt

def process_assignments(mtc, hit_id):
  results = []
  assignments = mtc.get_assignments(hit_id)
  for a in assignments:
    if a.AssignmentStatus in ['Approved', 'Submitted']:
      try:
        output = json.loads(a.answers[0][0].fields[0])
      except ValueError as e:
        print >> sys.stderr, ('Bad data from assignment %s (worker %s)'
            % (a.AssignmentId, a.WorkerId))
        continue
      results.append({
        'assignment_id': a.AssignmentId,
        'hit_id': hit_id,
        'worker_id': a.WorkerId,
        'output': json.loads(a.answers[0][0].fields[0]),
      })
  return results

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)
  
  results = []

  if args.hit_ids_file is None:
    for hit in mtc.get_all_hits():
      results += process_assignments(mtc, hit.HITId)
  else:
    with open(args.hit_ids_file, 'r') as f:
      for line in f:
        hit_id = line.strip()
        results += process_assignments(mtc, hit_id)

  for assignment_result in results:
    print json.dumps(assignment_result)

