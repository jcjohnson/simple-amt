import argparse, json
import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('--prod', action='store_false', dest='sandbox',
                      default=True,
                      help="Whether to run on the production AMT site.")
  parser.add_argument('--assignment_ids_file')
  parser.add_argument('--config', default='config.json', type=simpleamt.json_file)
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)

  if args.assignment_ids_file is None:
    parser.error('Must specify --assignment_ids_file.')

  with open(args.assignment_ids_file, 'r') as f:
    assignment_ids = [line.strip() for line in f]

  print ('This will reject %d assignments with '
         'sandbox=%s' % (len(assignment_ids), str(args.sandbox)))
  print 'Continue?'

  s = raw_input('(Y/N): ')
  if s == 'Y' or s == 'y':
    print 'Rejecting assignments'
    for idx, assignment_id in enumerate(assignment_ids):
      print 'Rejecting assignment %d / %d' % (idx + 1, len(assignment_ids))
      try:
        mtc.reject_assignment(assignment_id, feedback='Invalid results')
      except:
        print "Could not reject: %s" % (assignment_id)
  else:
    print 'Aborting'
