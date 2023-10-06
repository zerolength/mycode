#!/usr/bin/env python3
"""Friday Warmup | Returning Data From Complex JSON"""

import requests
import random
#URL= "https://opentdb.com/api.php?amount=10&category=32&difficulty=medium&type=boolean&encode=url3986"
URL= "https://opentdb.com/api.php?amount=10&category=31"
URL_base = "https://opentdb.com/api.php?"

def main():

    amountq= input("number of Q:")
    categs = requests.get('https://opentdb.com/api_category.php').json()
    print(categs)
    categ= input("categ as num:")
    FULL_URL= URL+ "amount="+amountq+"&category="+categ



    # data will be a python dictionary rendered from your API link's JSON!
    data= requests.get(FULL_URL).json()
    results = data['results']
#    print (data)
    for p in results:
        print(p['question'])
        answers = p['incorrect_answers']
        answers.append(p['correct_answer'])
        #answers 
        print(answers)
        random.shuffle(answers)
        i=1
        for answer in answers:
            print(f"{i}: {answer}")
            i+=1

if __name__ == "__main__":
    main()

