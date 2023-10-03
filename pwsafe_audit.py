import re
from fuzzywuzzy import fuzz

class pwsafe_entity:

    def __init__(self, principal, credential):
        self.principal = principal
        self.credential = credential
    def length(self):
        return len(self.credential)
    def reuse(self):
#        return self.principal in self.credential
        pattern = re.escape(self.principal)
#        print (pattern)

        overlapping_pattern = rf"(?=(.{5,})).*{pattern}"
#        print (overlapping_pattern)

        usernamecheck= re.search(pattern,self.credential)
#       print(usernamecheck)
        simplematch = re.findall(overlapping_pattern, self.credential)
        print(simplematch)
    #extended check
        lenMin = 5
        if overlapcheck or usernamecheck: 
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
                            similar_substring.add(substring1)

        if similar_substring:
            print("Fuzzy check failed")
            print(similar_substring)
            return True
        return False


def main():
    entity1 = pwsafe_entity("username", "password123")
    entity2 = pwsafe_entity("email@example.com", "securepassword")

    print(f"Length of credential 1: {entity1.length()}")
    print(f"Length of credential 2: {entity2.length()}")

    print(entity1.reuse())

    print(entity2.reuse())

if __name__ == "__main__":
    main()
