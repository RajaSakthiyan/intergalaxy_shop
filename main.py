'''
Created on 11-Nov-2019

@version: Python3.5
@author: Rajasakthiyan
@contact: rajasakthiyan.g@gmail.com
'''

from transactions import transaction

inputs = '''
    glob is I
    prok is V
    pish is X
    tegj is L
    glob glob Silver is 34 Credits    
    glob prok Gold is 57800 Credits
    pish pish Iron is 3910 Credits
'''
queries = '''
    how much is pish tegj glob glob ?
    how many Credits is glob prok Silver ?
    how many Credits is glob prok Gold ?
    how many Credits is glob prok Iron ?
    how much wood could a woodchuck chuck if a woodchuck could chuck wood ?
    '''

transaction(inputs, queries)
