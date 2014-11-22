import argparse, json

from boto.mturk.price import Price

import boto_utils, utils

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[utils])
  parser.add_argument('--hit_properties_file', type=argparse.FileType('r'))
  parser.add_argument('--html_template')
  parser.add_argument('--input_json_file', type=argparse.FileType('r'))
  args = parser.parse_args()

  mtc = boto_utils.get_mturk_connection_from_args(args)

  hit_properties = json.load(args.hit_properties_file)
  hit_properties['reward'] = Price(hit_properties['reward'])
  boto_utils.setup_qualifications(hit_properties)

  frame_height = hit_properties.pop('frame_height')
  env = utils.get_jinja_env()
  template = env.get_template(args.html_template)

  hit_ids = []
  for i, line in enumerate(args.input_json_file):
    hit_input = json.loads(line.strip())

    # In a previous version I removed all single quotes from the json dump.
    # TODO: double check to see if this is still necessary.
    template_params = { 'input': json.dumps(hit_input) }
    html = template.render(template_params)
    html_question = HTMLQuestion(html, frame_height)
    hit_properties['question'] = html_question

    # This error handling is kinda hacky.
    # TODO: Do something better here.
    launched = False
    while not launched:
      try:
        print 'Trying to launch HIT %d' % (i + 1)
        boto_hit = mtc.create_hit(**hit_properties)
        launched = True
      except MTurkRequestError as e:
        print e
    hit_id = boto_hit[0].HITId
    hit_ids.append(hit_id)

  # TODO: Should the hit ids file be mandatory?
  if options.hit_ids_file is not None:
    with open(options.hit_ids_file, 'w') as f:
      for hit_id in hit_ids:
        f.write('%s\n' % hit_id)

