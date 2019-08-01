import argparse, json

import os
import simpleamt
import sys

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  parser.add_argument('--hit_properties_file', type=argparse.FileType('r'))
  parser.add_argument('--html_template')
  parser.add_argument('--input_json_file', type=argparse.FileType('r'))
  args = parser.parse_args()

  mtc = simpleamt.get_mturk_connection_from_args(args)

  hit_properties = json.load(args.hit_properties_file)
  hit_properties['Reward'] = str(hit_properties['Reward'])
  simpleamt.setup_qualifications(hit_properties, mtc)

  frame_height = hit_properties.pop('FrameHeight')
  env = simpleamt.get_jinja_env(args.config)
  template = env.get_template(args.html_template)

  if args.hit_ids_file is None:
    print('Need to input a hit_ids_file')
    sys.exit()
  if os.path.isfile(args.hit_ids_file):
    print('hit_ids_file already exists')
    sys.exit()

  with open(args.hit_ids_file, 'w') as hit_ids_file:
    for i, line in enumerate(args.input_json_file):
      hit_input = json.loads(line.strip())

      # In a previous version I removed all single quotes from the json dump.
      # TODO: double check to see if this is still necessary.
      template_params = { 'input': json.dumps(hit_input) }
      html_doc = template.render(template_params)
      html_question = '''
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
          <HTMLContent>
            <![CDATA[
              <!DOCTYPE html>
              %s
            ]]>
          </HTMLContent>
          <FrameHeight>%d</FrameHeight>
        </HTMLQuestion>
      ''' % (html_doc, frame_height)
      hit_properties['Question'] = html_question

      # This error handling is kinda hacky.
      # TODO: Do something better here.
      launched = False
      while not launched:
        try:
          boto_hit = mtc.create_hit(**hit_properties)
          launched = True
        except Exception as e:
          print(e)
      hit_id = boto_hit['HIT']['HITId']
      hit_ids_file.write('%s\n' % hit_id)
      print('Launched HIT ID: %s, %d' % (hit_id, i + 1))


