class DoubleLinkedList(object):

    start = None
    end = None

    def __len__(self):
        cur_ref = self.start
        startlen = 0
        endlen = 0
        while cur_ref is not None:
            startlen += 1
            cur_ref = cur_ref['next']
        cur_ref = self.end
        while cur_ref is not None:
            endlen += 1
            cur_ref = cur_ref['last']
        return startlen

    def _append(self, data, start=True):
        new_ref = {'data': data, 'last': None, 'next': None}
        if start:
            if self.start is None:
                self.start = self.end = new_ref
            else:
                new_ref['last'] = self.end
                new_ref['next'] = None
                self.end['next'] = new_ref
                self.end = new_ref
        else:
            if self.start is None:
                self.start = self.end = new_ref
            else:
                new_ref['next'] = self.start
                new_ref['last'] = None
                self.start['last'] = new_ref
                self.start = new_ref

    def appendright(self, data):
        self._append(data)

    def appendleft(self, data):
        self._append(data, False)

    def _extend(self, data, start=True, flip=False):
        if not getattr(data, '__iter__'):
            raise TypeError('{} is not iterable'.format(type(data)))
        if flip:
            data = data[::-1]
        for item in data:
            if start:
                self.appendleft(item)
            else:
                self.appendright(item)

    def extendright(self, data, flip=False):
        self._extend(data, False, flip=flip)

    def extendleft(self, data, flip=True):
        self._extend(data, True, flip=flip)

    def remove(self, value, remall=False, start=True):
        removes = []
        if hasattr(value, '__iter__'):
            removes.extend(value)
        else:
            removes.append(value)
        for value in removes:
            if start:
                cur_ref = self.start
            elif not start:
                cur_ref = self.end
            while cur_ref is not None:
                if cur_ref['data'] == value:
                    if start:
                        if cur_ref['last']:
                            cur_ref['last']['next'] = cur_ref['next']
                            cur_ref['next']['last'] = cur_ref['last']
                        else:
                            self.start = cur_ref['next']
                            if len(self) >= 1:
                                cur_ref['next']['last'] = None
                            else:
                                cur_ref['data'] = None
                    else:
                        if cur_ref['next']:
                            cur_ref['next']['last'] = cur_ref['last']
                            cur_ref['last']['next'] = cur_ref['next']
                        else:
                            self.start = cur_ref['last']
                            if len(self) >= 1:
                                cur_ref['last']['next'] = None
                            else:
                                cur_ref['data'] = None
                if remall:
                    if start:
                        cur_ref = cur_ref['next']
                    else:
                        cur_ref = cur_ref['last']

    def _pop(self, start=True):
        if len(self) > 0:
            if start:
                popval = self.start['data']
                self.remove(popval)
            else:
                popval = self.end['data']
                self.remove(popval, start=False)
            return popval
        else:
            raise IndexError('pop from empty list.')

    def popleft(self):
        return self._pop(False)

    def popright(self):
        return self._pop()

    def __str__(self):
        cur_ref = self.start
        retstr = '['
        while cur_ref:
            retstr = retstr + str(cur_ref['data']) + ', '
            cur_ref = cur_ref['next']
        retstr = retstr[:len(retstr)-2] + ']'
        return retstr

    def show(self):
        cur_ref = self.start
        while cur_ref is not None:
            print(cur_ref['last']['data'] if cur_ref['last'] else None,
                  cur_ref['data'],
                  cur_ref['next']['data'] if cur_ref['next'] else None)
            cur_ref = cur_ref['next']


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
            if self.isfull():
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
    def __init__(self, qtype='f', maxsize=None):
        Queue.__init__(self, qtype, maxsize)
        pass
