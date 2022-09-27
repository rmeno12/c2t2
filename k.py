import subprocess

r = subprocess.run("pwd", shell=True, capture_output=True)
print(r.stdout)
