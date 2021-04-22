import subprocess
import os
from time import time

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush() # 자식 프로세스가 입력을 반드시 받게 함
    return proc

def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin = input_stdin,
        stdout = subprocess.PIPE
    )
    return proc

input_procs = []
hash_procs = []

for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

for proc in input_procs:
    proc.communicate()

for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())