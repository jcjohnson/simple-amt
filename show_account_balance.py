import argparse
import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()],
              description="Show your AMT account balance.")
  args = parser.parse_args()
  mtc = simpleamt.get_mturk_connection_from_args(args)
  print mtc.get_account_balance()[0]
