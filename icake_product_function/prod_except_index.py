
import numpy as np
import pandas as pd

def product_except_index_pd(num_list):
    """Accepts a list (1D array) of numbers and returns a list
    of the products for all products at each position excepting the
    current postion.  Example: product_except_index([1, 7, 3, 4]) = [84, 12, 28, 21]
    """
    
    out_list = list()
    num_series = pd.Series(num_list)
    
    for index, val in enumerate(num_list):
        if (num_series.dtype == 'int64') or (num_series.dtype == 'float64'):
            num_series[index] = 1
            product = num_series.product()     
            out_list.append(product)
            num_series[index] = val
        else:
            return "Invalid input, non-number in array"
    
    return out_list


def product_except_index_np_del(num_list):
    """Accepts a list (1D array) of numbers and returns a list
    of the products for all products at each position excepting the
    current postion.  Example: product_except_index([1, 7, 3, 4]) = [84, 12, 28, 21]
    """
    
    out_list = list()
    
    for index, val in enumerate(num_list):
        npX = np.array(num_list)
        if (npX.dtype == 'int32') or (npX.dtype == 'float64'):
            npX = np.delete(npX, index)
            product = np.prod(npX)        
            out_list.append(product)
        else:
            return "Invalid input, non-number in array"
    
    return out_list

def product_except_index_np_pop(num_list):
    """Accepts a list (1D array) of numbers and returns a list
    of the products for all products at each position excepting the
    current postion.  Example: product_except_index([1, 7, 3, 4]) = [84, 12, 28, 21]
    """
    
    out_list = list()
    
    for index, val in enumerate(num_list):
        num_list.pop(index)
        npX = np.array(num_list)
        if (npX.dtype == 'int32') or (npX.dtype == 'float64'):
            product = np.prod(npX)        
            out_list.append(product)
            num_list.insert(index, val)
        else:
            return "Invalid input, non-number in array"
    
    return out_list


def product_except_index(num_list):
    """Accepts a list (1D array) of numbers and returns a list
    of the products for all products at each position excepting the
    current postion.  Example: product_except_index([1, 7, 3, 4]) = [84, 12, 28, 21]
    """
    
    out_list = list()
    for index, val in enumerate(num_list):
        if isinstance(val, (int, long, float, complex)) == False:
            return "Invalid input, non-number in array"
        else:
            product = 1 # initialize product
            popped = num_list.pop(index)
            for item in num_list:
                product *= item
            out_list.append(product)
            num_list.insert(index, val)
        
        
    return out_list

# Interview Cake solution

def get_products_of_all_ints_except_at_index(int_list):

    # we make a list with the length of the input list to
    # hold our products
    products_of_all_ints_except_at_index = [None] * len(int_list)

    # for each integer, we find the product of all the integers
    # before it, storing the total product so far each time
    product_so_far = 1
    i = 0
    while i < len(int_list):
        products_of_all_ints_except_at_index[i] = product_so_far
        product_so_far *= int_list[i]
        i += 1

    # for each integer, we find the product of all the integers
    # after it. since each index in products already has the
    # product of all the integers before it, now we're storing
    # the total product of all other integers
    product_so_far = 1
    i = len(int_list) - 1
    while i >= 0:
        products_of_all_ints_except_at_index[i] *= product_so_far
        product_so_far *= int_list[i]
        i -= 1

    return products_of_all_ints_except_at_index