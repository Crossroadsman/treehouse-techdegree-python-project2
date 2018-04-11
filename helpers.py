def flatten_list(nested):
    '''takes a list with an inner iterable and flattens it to a single list
    '''
    output_list = []
    for inner in nested:
        for element in inner:
            output_list.append(element)
    return output_list

