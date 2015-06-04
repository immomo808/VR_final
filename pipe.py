import subprocess

args = ['ls', '-al']
p = subprocess.Popen(args)
print p.comunicate()


