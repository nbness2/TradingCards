try:
    from time import perf_counter as pc

except ImportError:
    try:
        from time import clock as pc

    except:
        raise ImportError('Failed to import perf_counter and clock from time module')


def randint(min_int=0, max_int=100, draw_amt=1):
    return weightchoice(range(min_int, max_int+1), draw_amt=draw_amt)


def randstring(strlen):
    ostr = ''
    for char in randint(32, 1024, strlen):
        ostr += chr(char)
    return ostr


def weightchoice(input_list, weight_list=None, draw_amt=1, max_precision=3):
    global seed_time
    pop_list = []
    try:
        draw_amt = int(draw_amt)
    except:
        raise TypeError('draw_amt must be convertable to int()')
    if draw_amt < 1:
        raise ValueError('You can\'t have less than 1 draw')
    if not weight_list:
        pop_list = input_list
    else:
        weight_sum = round(sum(weight_list), max_precision)

        if not len(input_list) == len(weight_list):
            raise ValueError('The length of input list {0} and weight list {1} must be equal'.format(len(input_list),
                                                                                                     len(weight_list)))
        if not weight_sum == 1:
            raise ValueError('The sum of all weights ({0}) must equal 1'.format(weight_sum))

        for inp, weight in zip(input_list, weight_list):
            for i in range(int(weight*(10**max_precision))):
                pop_list.append(inp)

    draws = []

    for x in range(draw_amt):
        seed = int(seed_time * (2**31)+.3)
        seed_offset = int(pc()*512-pc()+.3)
        seed_time = pc() - (seed_time_mod*pc()*x)
        result = pop_list[~(int(seed_time*seed)^seed_offset)%len(pop_list)]
        if draw_amt == 1:
            return result
        else:
            draws.append(result)

    return draws

seed_time = pc() * 16
seed_time_mod = seed_time*2
