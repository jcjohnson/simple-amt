import argparse, json
from jinja2 import Environment, FileSystemLoader

"""
Small bits of code that don't fit anywhere else.
"""

def get_jinja_env():
  with open('config.json') as f:
    config = json.load(f)
  return Environment(loader=FileSystemLoader(config['template-directories']))

def get_parent_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--prod', action='store_false', dest='sandbox',
                      default=True)
  parser.add_argument('--hit_ids_file')
  parser.add_argument('--aws_key_file')
  return parser
