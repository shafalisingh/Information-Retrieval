import os
import codecs
import operator
from collections import defaultdict
import math

"""
function to find a list of unique words.

Arguments:
@:argument1 (string): filepath

Returns:
uniquewords: A set of unique words
"""

def find_unique_words(filepath):
    uniquewords = set([])
    for root,dirs,files in os.walk(filepath):
        for name in files:
            [uniquewords.add(x.encode('ascii','replace').lower()) for x in
             codecs.open(os.path.join(root, name),"r",encoding="utf-8-sig").read().split()]

    return sorted(uniquewords)

"""
Clean the list of unique words by removing (,(comma), .(fullstop),\(backslash),/(forward slash),
 : (colon) ;(semi-colons), ?(question-marks))

Arguments:
@:argument1 (set):unique_word_set

Returns:
clean_word_set: A set of clean unique words
"""
def clean_unique_word_set(unique_word_set):
    clean_word_set= set([])
    remove_characters=[",","/","\\","?",".",";",":","?","!",'"','"--','&','{','}']
    for word in unique_word_set:
        word=word.translate(None, ''.join(remove_characters))
        # removing empty strings
        if (word != ""):
            clean_word_set.add(word)

    return clean_word_set

"""
Find the list of total words and clean it by removing (,(comma), .(fullstop),\(backslash),/(forward slash),
 : (colon) ;(semi-colons), ?(question-marks))

Arguments:
@:argument1 (string):filepath

Returns:
list: totalwords_cleaned
"""
def find_total_words(filepath):
    total_words = []
    total_words_cleaned=[]
    for root, dirs, files in os.walk(filepath):
        for name in files:
            [total_words.append(x.encode('ascii', 'replace').lower()) for x in
             codecs.open(os.path.join(root, name), "r", encoding="utf-8-sig").read().split()]
    remove_characters = [",", "/", "\\", "?", ".", ";", ":", "?", "!", '"', '"--', '&', '{', '}','--']
    for word in total_words:
        word = word.translate(None, ''.join(remove_characters))
        # removing empty strings
        if (word != ""):
            total_words_cleaned.append(word)

    return (total_words_cleaned)
"""
The number of unique words in the database
@arguments(set):unique_word_set

Returns:
count of words occuring only once

"""
def find_only_occurence(unique_word_set):
    dic = {}
    count=0

    for word in unique_word_set:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1

    for k,v in dic.items():
        if(v==1):
            count=count+1

    return count
"""
Term Frequency:For 30 most frequent words in the database
@arguments(list):total_wordset

Returns:
dic of 30 most frequent words
"""
def term_frequency(total_wordset):
    dic = {}
    tf_dict={}
    for i in total_wordset:
        if i not in dic:
            dic[i] = 1
        elif i in dic:
            dic[i] += 1
    freq_dict =(sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=True)[:31])
    for k,v in freq_dict:
        freq_words = [keys for keys,values in freq_dict]
    for k,v in freq_dict:
        tf_dict[k]=v
    return tf_dict

"""
IDF,TF*IDF,PROBABILITY:For 30 most frequent words in the database
@arguments1(freq_items): list
@:argument2 (filepath): string

Returns:
dic of IDF of 30 most frequent words
dic of TF*IDF of 30 most frequent words
dic of PROBABILITY of 30 most frequent words

"""

def inv_doc_frequency(freq_items,filepath):
    word_tuple = []
    occurence_dict={}
    d = defaultdict(set)
    r= defaultdict(set)
    dic = {}
    tf_dict = {}
    Prob = {}
    idf_arr = {}

    for root, dirs, files in os.walk(filepath):
        for name in files:
            data = open(os.path.join(root, name)).read()
            for x in freq_items:
                if (data.count(x) > 0):
                    word_tuple.append((x, name))
    for k, v in word_tuple:
        d[k].add(v)
    for k, v in d.items():
        occurence_dict[k] = len(v)

    for i in total_wordset:
        if i not in dic:
            dic[i] = 1
        elif i in dic:
            dic[i] += 1
    freq_dict = (sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=True)[:31])

    for k, v in freq_dict:
        tf_dict[k] = v
        freq_words_list=(sorted(tf_dict.items(),key=lambda kv: kv[1],reverse=True))

    for k,v in freq_dict:
        prob=float(v)/len(total_wordset)
        Prob[k]=prob

    for k,v in occurence_dict.items():
        idf=math.log(float(len(files))/float(v))
        idf_arr[k]=idf

    tf_idf=dict((k, v * idf_arr[k]) for k, v in tf_dict.items() if k in idf_arr)

    average = float(len(total_wordset) / len(files))

    return (occurence_dict,Prob,idf_arr,tf_idf,average)



if __name__ == '__main__':
    filepath=raw_input("Enter the Data file path:")
    total_wordset = find_total_words(filepath)
    print("Length of Total wordset:" + repr(len(total_wordset)))
    unique_word_set = find_unique_words(filepath)
    clean_word_set=clean_unique_word_set(unique_word_set)
    print("Length of Unique wordset:" + repr(len(clean_word_set)))
    print("Words occuring only once:" + repr(find_only_occurence(total_wordset)))

    freq_items=term_frequency(total_wordset)
    print("List of Frequent words:"+repr(freq_items))
    occurence_dict, Prob, idf_arr, tf_idf, average = inv_doc_frequency(freq_items,filepath)
    print("Occurence Dictionary:"+repr(occurence_dict))
    print("Probability:" + repr(Prob))
    print("IDF Dictionary:"+ repr(idf_arr))
    print("TF*IDF Dictionary:"+repr(tf_idf))
    print("Average:"+repr(average))






