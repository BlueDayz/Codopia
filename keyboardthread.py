import threading


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        inp = ''
        while inp != 'x':
            print('New fungus (f), new plant (p), new animal (a), exit (x): ')
            inp = input()
            self.input_cbk(inp)  # waits to get input + Return
