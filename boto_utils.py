from boto.mturk.connection import MTurkConnection
from boto.mturk.qualification import *


def get_mturk_connection_from_args(args):
  """
  Utility method to get an MTurkConnection from argparse args.
  """
  return get_mturk_connection(sandbox=args.sandbox,
                              aws_key_file=args.aws_key_file)


def get_mturk_connection(sandbox=True, aws_key_file=None):
  kwargs = {}
  if aws_key_file is not None:
    with open(aws_key_file, 'r') as f:
      kwargs.update(json.load(f))

  if sandbox:
    host = 'mechanicalturk.sandbox.amazonaws.com'
  else:
    host='mechanicalturk.amazonaws.com'
  return MTurkConnection(host=host, **kwargs)


def setup_qualifications(hit_properties):
  """
  Replace some of the human-readable keys from the raw HIT properties
  JSON data structure with boto-specific objects.
  """
  qual = Qualifications()
  if 'country' in hit_properties:
    qual.add(LocaleRequirement('EqualTo',
      hit_properties['country']))
    del hit_properties['country']

  if 'hits_approved' in hit_properties:
    qual.add(NumberHitsApprovedRequirement('GreaterThan',
      hit_properties['hits_approved']))
    del hit_properties['hits_approved']

  if 'percent_approved' in hit_properties:
    qual.add(PercentAssignmentsApprovedRequirement('GreaterThan',
      hit_properties['percent_approved']))
    del hit_properties['percent_approved']

  hit_properties['qualifications'] = qual
