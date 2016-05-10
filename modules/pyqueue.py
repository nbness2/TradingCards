

class Queue:
    def __init__(self, qtype='f', maxsize=None):
        if qtype.lower()[0] in 'lf':
            self.qtype = qtype
        else:
            raise TypeError('qtype must be (l) or (f)')
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = 0
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        if self.maxsize > 0:
            if self.full():
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

    def isfull(self):
        return len(self) == self.maxsize if self.maxsize <= 0 else False

class DEQueue(Queue):
    def __init__(self, maxsize=None):
        pass