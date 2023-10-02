import re
def main():
    player=input("How should we call you?")

    word_type= ['noun','verb','adj']
    wordbank = dict.fromkeys(word_type, None)

    nouns = input("Now give me some nouns, only last 3 will be used:\n")
    nouns = re.split('; |, |\*|\n|\ ', nouns)
    nouns = nouns [-3:]
    
    verbs = input("Now give me some verbs, only last 3 will be used:\n")
    verbs = re.split('; |, |\*|\n|\ ', verbs)
    verbs = verbs [-3:]

  
    adjs = input("Now give me some adjectives, only last 2 will be used:\n")
    adjs = re.split('; |, |\*|\n|\ ', adjs)
    adjs = adjs [-2:]


    wordbank = {'noun':nouns, 'verb': verbs, 'adj': adjs}

    print(wordbank)

    print(f"Python is a {wordbank.get('adj')[1]} language that lets you {wordbank.get('verb')[1]} more {wordbank.get('noun')[2]} and integrate your {wordbank.get('noun')[1]} more effectively. You can learn to {wordbank.get('verb')[2]} Python and see alsmost {wordbank.get('adj')[0]} {wordbank.get('noun')[0]} in productivity and {wordbank.get('verb')[0]} maitenance costs.")
















if __name__ == "__main__":
    main()

