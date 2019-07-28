import argparse, json

import boto3
from jinja2 import Environment, FileSystemLoader


"""
A bunch of free functions that we use in all scripts.
"""


def get_jinja_env(config):
  """
  Get a jinja2 Environment object that we can use to find templates.
  """
  return Environment(loader=FileSystemLoader('.'))


def json_file(filename):
  with open(filename, 'r') as f:
    return json.load(f)


def get_parent_parser():
  """
  Get an argparse parser with arguments that are always needed
  """
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('--prod', action='store_false', dest='sandbox',
                      default=True,
                      help="Whether to run on the production AMT site.")
  parser.add_argument('--hit_ids_file')
  parser.add_argument('--config', default='config.json',
                      type=json_file)
  return parser


def get_mturk_connection_from_args(args):
  """
  Utility method to get an MTurkConnection from argparse args.
  """
  aws_access_key = args.config.get('aws_access_key')
  aws_secret_key = args.config.get('aws_secret_key')
  return get_mturk_connection(sandbox=args.sandbox,
                              aws_access_key=aws_access_key,
                              aws_secret_key=aws_secret_key)


def get_mturk_connection(sandbox=True, aws_access_key=None,
                         aws_secret_key=None):
  """
  Get a boto mturk connection. This is a thin wrapper over boto3.client; 
  the only difference is a boolean flag to indicate sandbox or not.
  """
  kwargs = {}
  if aws_access_key is not None:
    kwargs['aws_access_key_id'] = aws_access_key
  if aws_secret_key is not None:
    kwargs['aws_secret_access_key'] = aws_secret_key

  if sandbox:
    host = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
  else:
    host='https://mturk-requester.us-east-1.amazonaws.com'
  return boto3.client('mturk', endpoint_url=host, **kwargs)


def setup_qualifications(hit_properties, mtc):
  """
  Replace some of the human-readable keys from the raw HIT properties
  JSON data structure with boto-specific objects.
  """
  qual = []
  if 'Qualification_id' in hit_properties and 'Qualification_comparator' in hit_properties and 'Qualification_integer' in hit_properties:
    comparator = hit_properties['Qualification_comparator']
    if comparator == '>': 
        c = 'GreaterThan'
    elif comparator == '=': 
        c = 'EqualTo'
    elif comparator == '<': 
        c = 'LessThan'
    else:
        print("The 'qualification comparator' is not one of the designated values ('<', '=', '>').")
    qual.append({
        'QualificationTypeId': hit_properties['Qualification_id'],
        'Comparator': c,
        'IntegerValues': int(hit_properties['Qualification_integer']),
        'RequiredToPreview': False,
    })
    del hit_properties['Qualification_id']
    del hit_properties['Qualification_comparator']
    del hit_properties['Qualification_integer']
  if 'Country' in hit_properties:
    qual.append({
        'QualificationTypeId': '00000000000000000071',
        'Comparator': 'In',
        'LocaleValues': [{'Country': country} for country in hit_properties['Country']],
    })
    del hit_properties['Country']

  if 'Hits_approved' in hit_properties:
    qual.append({
        'QualificationTypeId': '00000000000000000040',
        'Comparator': 'GreaterThan',
        'IntegerValues': [hit_properties['Hits_approved']],
    })
    del hit_properties['Hits_approved']

  if 'Percent_approved' in hit_properties:
    qual.append({
        'QualificationTypeId': '000000000000000000L0',
        'Comparator': 'GreaterThan',
        'IntegerValues': [hit_properties['Percent_approved']],
    })
    del hit_properties['Percent_approved']

  hit_properties['QualificationRequirements'] = qual
