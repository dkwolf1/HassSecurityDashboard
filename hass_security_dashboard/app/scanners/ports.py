import subprocess
def check():
 try:
  r = subprocess.check_output(['ss', '-tuln'], text=True)
  return {'status': 'ok', 'log': r}
 except Exception as e:
  return {'status': 'fail', 'log': str(e)}