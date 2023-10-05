from fuzzywuzzy import fuzz


def fuzzy_match(str1, str2):
    similarity_ratio = fuzz.ratio(str1, str2) / 100
    similarity_portion = str1[:int(len(str1)*similarity_ratio)]
    return similarity_portion, similarity_ratio
    
str1 = 'teSt'
str2 = 't#st object'

print(fuzzy_match(str1,str2))
