"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from utils.validators import validate_postcode, validate_dutchbanknumber
from django import forms

class PostalCodeValidationTest(TestCase):
    """
        Tests the validate_postcode function
    """
    valid_postcodes = (
        ('1000 AA', '1000AA'),
        ('1000 aa', '1000AA'),
        ('1000aa', '1000AA'),
        ('9999zz','9999ZZ'),
        ('1000AA', '1000AA'),
        (' 1000 AA', '1000AA'),
        (' 1000aa ', '1000AA'),
    )
    
    invalid_postcodes = (
        '0123 AA',
        '0123aa',
        '0123 aa',
        '012 aa',
        '1000 a',
        '1000a',
        ' 1000 A',
        'AA',
        'A'
        ' a',
        '0000',
    )
    
    def test_valids(self):
        """
            Tests that the output of the validate_postcode function has the expected result
        """
        for postcode, expected_result in self.valid_postcodes:
            self.failUnlessEqual(validate_postcode(postcode), expected_result)
            
    def test_invalids(self):
        """
            Tests that the validate_postcode throws the right error on invalid input
        """
        for postcode in self.invalid_postcodes:
            self.assertRaises(forms.ValidationError, validate_postcode, postcode)

class DutchBankNumberValidationTest(TestCase):
    """
        Test the validate_dutchbanknumber function
    """
    
    valid_numbers = (
        ('p555', 'P555'),
        ('P123', 'P123'),
        ('305242318', '305242318'),
        ('P8073472', 'P8073472'),
        ('150262655', '150262655'),
    )
    
    invalid_numbers = (
        '555',
        '123',
        '305242317',
    )
    
    # special cases which do go through the elfproof but should be considered invalid
    special_invalid_numbers = (
        '111111110',
        '000000000',
        '999999999',
    )
    
    def test_valids(self):
        """
            Tests that the output of the validate_dutchbanknumber function has the expected result
        """
        for number, expected_result in self.valid_numbers:
            self.failUnlessEqual(validate_dutchbanknumber(number), expected_result)
    
    def test_invalids(self):
        """
            Tests that the validate_dutchbanknumber function throws the right error in invalid input
        """
        for number in self.invalid_numbers:
            self.assertRaises(forms.ValidationError, validate_dutchbanknumber, number)
            
    def test_specialcases(self):
        """
            Tests that the special cases also throw the right error
        """
        for number in self.special_invalid_numbers:
            self.assertRaises(forms.ValidationError, validate_dutchbanknumber, number)
        