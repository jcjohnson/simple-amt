import argparse

import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()],
              description="Delete HITs")
  parser.add_argument('--worker_ids_file')
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)
  worker_ids = []
  with open(args.worker_ids_file, 'r') as f:
    worker_ids = [line.strip() for line in f]

  print ('This will block %d workers with IDs with sandbox=%s'
         % (len(worker_ids), str(args.sandbox)))
  print 'Continue?'
  s = raw_input('(Y/N): ')
  if s == 'Y' or s == 'y':
    for worker_id in worker_ids:
      try:
        mtc.block_worker(worker_id, "provided bad data")
      except:
        print 'Failed to block: %s' % (worker_id)
  else:
    print 'Aborting'
