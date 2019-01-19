import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname='192.168.149.101', port=22, username='robot', password='wam')
except:
    print "connect failed"
    quit()

cmd = 'ls'
#cmd = 'ls -l;ifconfig'
stdin, stdout, stderr = ssh.exec_command(cmd)

result = stdout.read()

if not result:
    result = stderr.read()
ssh.close()

print(result.decode())