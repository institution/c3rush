import sys


class Log(object):
    def __init__(self, debug=True):
        self.debug = debug
    
    def __call__(self, *xs):
        if self.debug == True:
            sys.stderr.write(''.join(str(x) for x in xs) + '\n')




log = Log()
