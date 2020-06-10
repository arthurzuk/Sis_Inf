import tempfile
import os
import subprocess
import hashed_psw

path = input('Insira o path do executável MySQL Server: ')
path = path.replace('\\','\\\\')

tmp = tempfile.NamedTemporaryFile(delete=False)

psw = b"ALTER USER 'root'@'localhost' IDENTIFIED BY '" + bytes(hashed_psw.get_psw()) + b"';"
#psw = b"ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';"

try:
    tmp.write(psw)
    tmp.close()
    subprocess.call('mysqld --defaults-file="C:\\ProgramData\\MySQL\\MySQL Server 8.0\\my.ini" --init-file="'+tmp.name+'" --console', cwd=path)
finally:
    os.remove(tmp.name)
