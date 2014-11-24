import argparse, os, os.path
import simpleamt

if __name__ == '__main__':
  parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
  parser.add_argument('--html_template', required=True)
  args = parser.parse_args()

  env = simpleamt.get_jinja_env(args.config)
  template = env.get_template(args.html_template)

  output_dir = args.config['rendered_template_directory']
  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  html = template.render({'input': ''})
  with open(os.path.join(output_dir, args.html_template), 'w') as f:
    f.write(html)

