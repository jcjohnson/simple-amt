import argparse, json
import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)

  reject_ids = []

  if args.hit_ids_file is None:
    parser.error('Must specify --hit_ids_file.')

  with open(args.hit_ids_file, 'r') as f:
    hit_ids = [line.strip() for line in f]

  for hit_id in hit_ids:
    try:
        for a in mtc.get_assignments(hit_id):
            reject_ids.append(a.AssignmentId)
    except:
      print "Couldn't find hit_id: %s" % (hit_id)

  print ('This will reject %d assignments with '
         'sandbox=%s' % (len(reject_ids), str(args.sandbox)))
  print 'Continue?'

  s = raw_input('(Y/N): ')
  if s == 'Y' or s == 'y':
    print 'Rejecting assignments'
    for idx, assignment_id in enumerate(reject_ids):
      print 'Rejecting assignment %d / %d' % (idx + 1, len(reject_ids))
      try:
        mtc.reject_assignment(assignment_id, feedback='Invalid results')
      except:
        print "Could not reject: %s" % (assignment_id)
  else:
    print 'Aborting'
