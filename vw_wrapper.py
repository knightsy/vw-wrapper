# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 15:09:54 2015

@author: Peter Knight

may need string cleaning function to stop invalid examples going through to vw
"""


#import pyodbc
import socket
import collections
import string




def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
    
def remove_specials(string_to_clean, replacement_char='_'):
    
    clean_string = string_to_clean.replace("\n",replacement_char)
    clean_string = clean_string.replace(":",replacement_char)
    clean_string = clean_string.replace("|",replacement_char)
    return clean_string
    
def remove_null_keys(dict_to_clean):
    cleaned = []
    for i,j in dict_to_clean.items():
        if j != None and j != 'None': cleaned.append((i,j))
    return dict(cleaned)
    
def fill_key_spaces(dict_to_clean):
    return_dict = {}
    for key, value in dict_to_clean.items():
        return_key = string.replace(key,' ','_')
        return_dict[return_key] = value
    return return_dict
    



def parse_string(x):
    lambda x: x.isalpha() and x or x.isdigit() and \
    int(x) or x.isalnum() and x or \
    len(set(string.punctuation).intersection(x)) == 1 and \
    x.count('.') == 1 and float(x) or x   
    
    return x
       
       


def pynetcat(hostname, port, content):
    
#    reply = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(2048)
        if data == "":
            break
#        print "Received:", repr(data)
#        reply = repr(data) 
        reply = data
#    print "Connection closed."
    s.close()
    return reply
       




def json_to_vw(json_input):

    #setup special vw attributes prefixed with undersores in the input dictionary
    label = ''
    if "_label" in json_input:
        label = str(json_input["_label"])
    tag = ''
    if "_tag" in json_input:
        tag = str(json_input["_tag"])
    weight = ''    
    if "_weight" in json_input:
        weight = str(json_input["_weight"])
    text = ''    
    if "_text" in json_input:
        text = str(json_input["_text"])
    
    # remove special features from dictionary
    json_input.pop("_label", None)
    json_input.pop("_tag", None)
    json_input.pop("_weight", None)
    json_input.pop("_text", None)

    # flatten the dictionary - this is a short term kludge to deal with nested attributes
    json_input = flatten(json_input)
    json_input = fill_key_spaces(json_input)

    vw_example = label + ' ' + weight + ' ' + tag + '| '
    #print type(json_input)

    for i in json_input:
        value = json_input[i]
        separator = ':'
        if isinstance(value,basestring):
            separator = '_'
            value = value.replace(' ','_') 
#            print value
        vw_example += i + separator + str(value) + ' '
        
    vw_example += ' |text ' + text + "\n"
    
    return vw_example
    


def vw_replyline_to_json(vw_reply, has_tag = 'No'): 
     #this only accepts strings - for multiple examples, loop over this function
    _tag = ''
    vw_reply_dict = {} 
    vw_reply_list = vw_reply.split()
    if has_tag == 'Yes': 
        _tag = vw_reply_list[-1]
        del vw_reply_list[-1]
        vw_reply_dict["_tag"] = _tag
#    print vw_reply_list
    counter = 0
    for j in vw_reply_list:
        counter += 1
        vw_reply_dict[str(counter)] = j
    return vw_reply_dict
           
    
def tests():
    # to be resolved:
    #should the pynetcat function even b in here?
    #pynetcat probably needs to detect OS and adapt accordingly

    
    #json_in = ({ "weight":0.0001 , "ns1":{"location":"New York", "f2":3.4}, "label":0,"_tag":"1234", "_text": "yo dawg it be some text"})
#    json_in = ({  "ns1":{"location":"New York", "f2":3.4}, "_label":0,"_tag":"1234", "_text": "yo dawg it be some text"})
#    json_in = ({  "ns1":{"shopping":8, "sport":1}, "_label":1 , "_tag":"wassup"})
    json_in = ({  "ns1":{"shopping":1, "sport":8}, "_label":0 , "_tag":"wassup"})
    vw_example =  json_to_vw(json_in)
    print vw_example
#    pynetcat('localhost',26542, vw_example)
#
#    reply = pynetcat('localhost',26542, vw_example)
#    print reply
#
#    print vw_replyline_to_json(reply, "Yes")
    
    i = 0
    while i < 1:
        reply = pynetcat('localhost',26542, vw_example)
        print reply
        print vw_replyline_to_json(reply, "Yes")
        i += 1



if __name__ == '__main__':
    tests()
