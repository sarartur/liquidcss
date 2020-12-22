import time
import subprocess


while True:
    _ = subprocess.check_output(['sh', 'liquid', 'stage', '--all'])
    print(_)
    _ = subprocess.check_output(['sh', 'liquid', 'deploy', '--all'])
    print('ran')
    time.sleep(3)