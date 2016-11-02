import argparse

import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()],
              description="Delete HITs")
  parser.add_argument('--hit_id')
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)
  hit_id = args.hit_id

  print ('This will delete HIT with ID: %s with sandbox=%s'
         % (hit_id, str(args.sandbox)))
  print 'Continue?'
  s = raw_input('(Y/N): ')
  if s == 'Y' or s == 'y':
    try:
      mtc.disable_hit(hit_id)
    except:
      print 'Failed to disable: %s' % (hit_id)
  else:
    print 'Aborting'
