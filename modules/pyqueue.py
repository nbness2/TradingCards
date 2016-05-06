

class Queue:
    def __init__(self, qtype='l', maxsize=0):
        if qtype.lower()[0] in 'lf':
            self.qtype = qtype
        else:
            raise TypeError('qtype must be (l) or (f)')
        if maxsize < 0:
            self.maxsize = 0
        else:
            self.maxsize = maxsize
        self.queue = []

    def put(self, item):
        if self.maxsize > 0:
            if len(self.queue) == self.maxsize:
                raise ValueError('Queue is full')
        self.queue.append(item)

    def get(self):
        if self.qtype == 'f':
            return self.queue.pop(0)
        elif self.qtype == 'l':
            return self.queue.pop(len(self.queue)-1)
        else:
            raise TypeError('Type must be (l) or (f)')

    def empty(self):
        return not bool(self.queue)