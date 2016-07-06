from modules.pylinkedlists import DoubleLinkedList


class Queue:
    def __init__(self, queue_type='f', maxsize=None):
        if queue_type.lower()[0] in 'lf':
            self.queue_type = queue_type
        else:
            raise TypeError('invalid queue type {}'.format(queue_type))
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = 0
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, data):
        if self.isfull():
            raise ValueError('Queue is full')
        self.queue.append(data)

    def get(self):
        if self.queue_type == 'f':
            return self.queue.pop(0)
        elif self.queue_type == 'l':
            return self.queue.pop()
        else:
            raise TypeError('invalid queue type {}'.format(self.queue_type))

    def empty(self):
        return not bool(self.queue)

    def isfull(self):
        return len(self) == self.maxsize if self.maxsize > 0 else False


class DEQueue(Queue):
    def __init__(self, queue_type='f', maxsize=None):
        Queue.__init__(self, queue_type, maxsize)
        self.queue = DoubleLinkedList()

    def popleft(self):
        return self.queue.popleft()

    def pop(self):
        return self.queue.pop()

    def putleft(self, data):
        if self.isfull():
            raise ValueError('Queue is full')
        self.queue.appendleft(data)
