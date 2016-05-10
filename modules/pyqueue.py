class DLL(object):
    start = None
    end = None

    def append(self, data):
        new_ref = {'data': data, 'last': None, 'next': None}
        if self.start is None:
            self.start = self.end = new_ref
        else:
            new_ref['last'] = self.end
            new_ref['next'] = None
            self.end['next'] = new_ref
            self.end = new_ref

    def remove(self, value):
        removes = []
        removes.extend(value)
        for value in removes:
            cur_ref = self.start
            while cur_ref is not None:
                if cur_ref['data'] == value:
                    if cur_ref['last'] is not None:
                        cur_ref['last']['next'] = cur_ref['next']
                        cur_ref['next']['last'] = cur_ref['last']
                    else:
                        self.start = cur_ref['next']
                        cur_ref['next']['last'] = None
                cur_ref = cur_ref['next']

    def show(self):
        cur_ref = self.start
        while cur_ref is not None:
            print(cur_ref['last']['data'] if cur_ref['last'] != None else None,
                  cur_ref['data'],
                  cur_ref['next']['data'] if cur_ref['next'] != None else None)
            cur_ref = cur_ref['next']

DEList = DLL()
for x in range(10):
    DEList.append(x)
DEList.remove([1, 7, 3, 8, 'a'])
DEList.show()


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