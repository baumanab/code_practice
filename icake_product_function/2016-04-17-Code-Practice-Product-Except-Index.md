---
layout: article
title: Reverse Polish Notation Script
modified: {}
categories: posts
excerpt: Python code to make calculations in RPN
tags: 
  - code_practice
comments: true
published: true
image: 
  feature: null
  teaser: null
  thumb: null
---


## The challenge


[Interview Cake Problem 2](https://www.interviewcake.com/question/python/product-of-other-numbers)

Write a function get_products_of_all_ints_except_at_index() that takes a list of integers and returns a list of the products.

Example: ```[1, 7, 3, 4] --> [84, 12, 28, 21]```

I'm trying out test driven development (TDD) focusing on the use of doctest and pytest vs using unittest.  The specificatons are pretty straight forward, the input must be an array where the elements are numbers.  I suppose you could do this with a multidimensional array, but it would be much more efficient to leverage numpy or PANDAS for this, vs. writing our own function.  The description calls for integers, but there is no reason why this fuction couldn't operate on floats.

What tests would be useful for developing this function?

1. Test for a the return of an accurate result
2. Test that if any element is a string that an exception is raised
3. Test that function can handle zeroes

There are two scenarios for item 2:
- string * number ('3' * 5 --> '33333')
- string * string ('3' * '5' --> TypeError)

A validator could be written where the array can be check for all elements are ints or all elements are numbers or no elements are strings.  I dont want to get too far out of scope of the challenge. So, I will validate input and check for the return of a failed validation, which should cover both cases.  Just for learning purposes though I will write a third test that makes sure a type error is raised for > 1 string.

### Write the test file and tests


```python
%%writefile prod_except_index.py

def product_except_index(num_list):
    """Accepts a list (1D array) of numbers and returns a list
    of the products for all products at each position excepting the
    current postion.  Example: product_except_index([1, 7, 3, 4]) = [84, 12, 28, 21]
    """
    pass
```

    Overwriting prod_except_index.py
    


```python
%%writefile test_prod_except_index.py

import pytest
from prod_except_index import *


def test_product_accuracy():
    assert product_except_index([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert product_except_index([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_valid_input_gt_one_string():
    with pytest.raises(TypeError):
        product_except_index([1, '7', 3, '4'])

def test_product_input_with_zeroes():
    assert product_except_index([0,0,0]) == [0,0,0]


```

    Overwriting test_prod_except_index.py
    

### Test the Function


```python
!py.test test_prod_except_index.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 4 items
    
    test_prod_except_index.py FFFF
    
    ================================== FAILURES ===================================
    ____________________________ test_product_accuracy ____________________________
    
        def test_product_accuracy():
    >       assert product_except_index([1, 7, 3, 4]) == [84, 12, 28, 21]
    E       assert None == [84, 12, 28, 21]
    E        +  where None = product_except_index([1, 7, 3, 4])
    
    test_prod_except_index.py:7: AssertionError
    _____________________ test_product_valid_input_one_string _____________________
    
        def test_product_valid_input_one_string():
    >       assert product_except_index([1, '7', 3, 4]) == "Invalid input, non-number in array"
    E       assert None == 'Invalid input, non-number in array'
    E        +  where None = product_except_index([1, '7', 3, 4])
    
    test_prod_except_index.py:10: AssertionError
    ___________________ test_product_valid_input_gt_one_string ____________________
    
        def test_product_valid_input_gt_one_string():
            with pytest.raises(TypeError):
    >           product_except_index([1, '7', 3, '4'])
    E           Failed: DID NOT RAISE
    
    test_prod_except_index.py:14: Failed
    _______________________ test_product_input_with_zeroes ________________________
    
        def test_product_input_with_zeroes():
    >       assert product_except_index([0,0,0]) == [0,0,0]
    E       assert None == [0, 0, 0]
    E        +  where None = product_except_index([0, 0, 0])
    
    test_prod_except_index.py:17: AssertionError
    ========================== 4 failed in 0.16 seconds ===========================
    

### Result

Yay it failed, this is what we want. If this had passed, something would be seriously wrong.

### Re-write the function


```python
%%writefile prod_except_index.py

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
            
```

    Overwriting prod_except_index.py
    


```python
!py.test test_prod_except_index.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 4 items
    
    test_prod_except_index.py ....
    
    ========================== 4 passed in 0.05 seconds ===========================
    

### Result

The tests passed which is good, but the functiion uses two loops which means it scales at the less than ideal O(n^2). I'm going to investigate the following approaches.

- Use PANDAS series with pop method (applied to series)
- Use numpy delete method with numpy vectorized prodcut function
- Use pop method on list but calculate product with numpy vectorized product function
- Compare the timing of each approach the Interview Cake published solution 

### Setup the functions


```python
%%writefile prod_except_index.py

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
```

    Overwriting prod_except_index.py
    

### Test the functions


```python
%%writefile test_prod_except_index_np_pop.py

import pytest
from prod_except_index import *


def test_product_accuracy():
    assert product_except_index_np_pop([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert product_except_index_np_pop([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_input_with_zeroes():
    assert product_except_index_np_pop([0,0,0]) == [0,0,0]

```

    Overwriting test_prod_except_index_np_pop.py
    


```python
!py.test test_prod_except_index_np_pop.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 3 items
    
    test_prod_except_index_np_pop.py ...
    
    ========================== 3 passed in 18.72 seconds ==========================
    


```python
%%writefile test_prod_except_index_np_del.py

import pytest
from prod_except_index import *


def test_product_accuracy():
    assert product_except_index_np_del([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert product_except_index_np_del([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_input_with_zeroes():
    assert product_except_index_np_del([0,0,0]) == [0,0,0]

```

    Overwriting test_prod_except_index_np_del.py
    


```python
!py.test test_prod_except_index_np_del.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 3 items
    
    test_prod_except_index_np_del.py ...
    
    ========================== 3 passed in 2.50 seconds ===========================
    


```python
%%writefile test_prod_except_index_pd.py

import pytest
from prod_except_index import *


def test_product_accuracy():
    assert product_except_index_pd([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert product_except_index_pd([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_input_with_zeroes():
    assert product_except_index_pd([0,0,0]) == [0,0,0]

```

    Overwriting test_prod_except_index_pd.py
    


```python
!py.test test_prod_except_index_pd.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 3 items
    
    test_prod_except_index_pd.py ...
    
    ========================== 3 passed in 2.45 seconds ===========================
    


```python
%%writefile test_icake_solution.py

import pytest
from prod_except_index import *


def test_product_accuracy():
    assert get_products_of_all_ints_except_at_index([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert get_products_of_all_ints_except_at_index([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_input_with_zeroes():
    assert get_products_of_all_ints_except_at_index([0,0,0]) == [0,0,0]

```

    Overwriting test_icake_solution.py
    


```python
!py.test test_icake_solution.py
```

    ============================= test session starts =============================
    platform win32 -- Python 2.7.11, pytest-2.8.5, py-1.4.31, pluggy-0.3.1
    rootdir: C:\Users\vhim98198\Downloads\icake_product_function, inifile: 
    collected 3 items
    
    test_icake_solution.py .F.
    
    ================================== FAILURES ===================================
    _____________________ test_product_valid_input_one_string _____________________
    
        def test_product_valid_input_one_string():
    >       assert get_products_of_all_ints_except_at_index([1, '7', 3, 4]) == "Invalid input, non-number in array"
    E       assert ['777777777777', 12, '7777', '777'] == 'Invalid input, non-number in array'
    E        +  where ['777777777777', 12, '7777', '777'] = get_products_of_all_ints_except_at_index([1, '7', 3, 4])
    
    test_icake_solution.py:10: AssertionError
    ===================== 1 failed, 2 passed in 2.50 seconds ======================
    

### Compare time to run using cell magics

- Compare with a small list (n = 4)
- Compare with a larger (n = 100) list


```python
import numpy as np
import pandas as pd
```


```python
from prod_except_index import *  
```


```python
%load_ext memory_profiler
```


```python
small_list = [1, 7, 3, 4]
```


```python
%%timeit
product_except_index(small_list)
```

    10000 loops, best of 3: 28.3 µs per loop
    


```python
%%timeit
product_except_index_np_del(small_list)
```

    1000 loops, best of 3: 438 µs per loop
    


```python
%%timeit
product_except_index_np_pop(small_list)
```

    10000 loops, best of 3: 170 µs per loop
    


```python
%%timeit
product_except_index_pd(small_list)
```

    1000 loops, best of 3: 1.6 ms per loop
    


```python
%%timeit
get_products_of_all_ints_except_at_index(small_list)
```

    100000 loops, best of 3: 9.03 µs per loop
    


```python
np.random.seed(0)
```


```python
large_list = np.random.randint(10, size = 100 )
large_list = list(large_list)
```


```python
%%timeit
product_except_index(large_list)
```

    100 loops, best of 3: 5.61 ms per loop
    


```python
%%timeit
product_except_index_np_del(large_list)
```

    100 loops, best of 3: 13.7 ms per loop
    


```python
%%timeit
product_except_index_np_pop(large_list)
```

    100 loops, best of 3: 7.5 ms per loop
    


```python
%%timeit
product_except_index_pd(large_list)
```

    10 loops, best of 3: 26.4 ms per loop
    


```python
%%timeit
get_products_of_all_ints_except_at_index(large_list)
```

    1000 loops, best of 3: 253 µs per loop
    

### Result

The Interview Cake function is the clear winner.
