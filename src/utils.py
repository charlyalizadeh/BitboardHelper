def get_coord(index, shape):
    i = int(index / shape[1])
    j = index - i * shape[1]
    return (i, j)


def get_index(i, j, shape):
    return i * shape[1] + j
