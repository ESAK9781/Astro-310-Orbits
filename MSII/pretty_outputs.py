##############################
# pretty_outputs.py
# Author: Elijah Sakamoto
# Documentation: None
##############################



'''
Some utility functions (not related to anything astro or computational) that are intended to help
with readable output of the computational and astronautical results.
'''


# indent each line of a section of tests
def indent_section(section : str, indent_by : int):
    lines = section.split('\n')
    out_str = ""
    for line in lines:
        cur_line_str = ""
        for i in range(indent_by):
            cur_line_str += '\t'
        cur_line_str += line
        cur_line_str += '\n'
        out_str += cur_line_str
    
    return out_str