import re
from thefuzz import fuzz
from thefuzz import process
#stregnth testing module
from password_strength import PasswordPolicy, PasswordStats
#for color
import crayons

#fucntion for similar string test , str1 is the smaller/left
def fuzzycheck(str1, str2)
    tokenS_ratio = fuzz.token_set_ratio(str1, str2)
    ratio = fuzz.ratio(str1, str2)
    match = process.exractOne(str1, str2)

#function for strengh teting, pstrength_test(pwsafe_entity, policy)
def pstrength_test(pwsafe_entity, policy):
    policy.test(pwsafe_entity.credential)
    PasswordStats(pwsafe_entity.credential)

#class for password safe entry, pwsafe(self,principal,credential,link,description, reuse.(), length())
class pwsafe_entity:

    def __init__(self, principal, credential, link, description):
        self.principal = principal
        self.credential = credential
        self.link = link
        self.descr = description
    def length(self):
        return len(self.credential)
    #check for password reusing username
    def reuse(self):
#        return self.principal in self.credential
        pattern = re.escape(self.principal)
#        print (pattern)

        overlapping_pattern = rf"(?=(.{5,})).*{pattern}"
#        print (overlapping_pattern)

        renamecheck= re.search(pattern,self.credential)
#        print(' '.join(renamecheck))
        simplematch = re.findall(overlapping_pattern, self.credential)
        print(simplematch)
#        matchestostr = ' '.join(simplematch)
#        concat = [self.principal, self.credential]
#        print(f"the username is {crayons.red(concat)}")
#        print(f"WARNING:username match password: {crayons.red(matchestostr)}")
        #extended check
        lenMin = 5
        if renamecheck or simplematch: 
            print("simplecheck for username failed")
            return True
        similar_substring = []
        for i in range (len(self.principal)):
            for j in range(i+lenMin, len(self.principal)+1):
                substring1 = self.principal [i:j]

                for k in range(len(self.credential)):
                    for l in range(k + lenMin, len (self.credential)+1):
                        substring2 = self.credential[k:l]

                        similarity = fuzz.ratio(substring1, substring2)

                        if similarity >= 80:
                            similar_substring.append(substring1)

        if similar_substring:
            print("Fuzzy check failed")
            print(similar_substring)
            return True
        return False


def main():
    #assigning test entry
    entity1 = pwsafe_entity("username", "password123username","link","desc")
    entity2 = pwsafe_entity("email@example.com", "securepassword","example.com","email")

    print(f"Length of credential 1: {entity1.length()}")
    print(f"Length of credential 2: {entity2.length()}")

    print(entity1.reuse())
    print("e2")
    print(entity2.reuse())

if __name__ == "__main__":
    main()
