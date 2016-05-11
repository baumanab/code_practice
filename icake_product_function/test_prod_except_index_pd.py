
import pytest
from prod_except_index import *


def test_product_accuracy():
    assert product_except_index_pd([1, 7, 3, 4]) == [84, 12, 28, 21]

def test_product_valid_input_one_string():
    assert product_except_index_pd([1, '7', 3, 4]) == "Invalid input, non-number in array"

def test_product_input_with_zeroes():
    assert product_except_index_pd([0,0,0]) == [0,0,0]