import subprocess
import time
args1 = ['./Streaming_to_CSV.py', '0', 'happy']
p1 = subprocess.Popen(args1)
time.sleep(5)
args2 = ['./Batch_Processing.py', '0']
p2 = subprocess.Popen(args2)
time.sleep(1000)
print('terminate child process')
p1.terminate()
p2.terminate()
