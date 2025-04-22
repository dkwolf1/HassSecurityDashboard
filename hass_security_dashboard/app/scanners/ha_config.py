import yaml
def check():
 try:
  with open('/config/configuration.yaml') as f:
   y = yaml.safe_load(f)
  return {'status': 'ok', 'log': 'Config parsed successfully'}
 except Exception as e:
  return {'status': 'fail', 'log': str(e)}