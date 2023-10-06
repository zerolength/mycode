import re
#csv file read
import csv
#fuzzy string compare
from thefuzz import fuzz, process
#stregnth testing module
from password_strength import PasswordPolicy, PasswordStats
#for color
import crayons


# Function for similar string test, str1 is the smaller/left
def fuzzycheck(str1, str2):
    tokenS_ratio = fuzz.token_set_ratio(str1, str2)
    ratio = fuzz.ratio(str1, str2)
    match = process.extractOne(str1, str2)
    check = ((ratio > 80) or (tokenS_ratio>80))
    return check, match, tokenS_ratio, ratio

# Function for checking if a password is common or matches bad passwords
def is_common_password(password):
    commonp_list = []
    common_passwords = ["password", "123456", "qwerty", "admin"]  # Add more common passwords
    for commonp in common_passwords:
        tokenS_ratio = fuzz.token_set_ratio (password, commonp)
        if tokenS_ratio >= 80:  # Use 80 instead of 0.8 for a ratio of 80 or higher
            commonp_list.append((tokenS_ratio, commonp))
    
    return commonp_list

# Function for strength testing, pstrength_test(pwsafe_entity, policy)
def pstrength_test(pwsafe_entity, policy):
    policy.test(pwsafe_entity.credential)
    PasswordStats(pwsafe_entity.credential)
#class for password safe entry, pwsafe(self,principal,credential,link,description, reuse.(), length())

def parse_password_file(filename):
    password_entries = []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            
            for row in reader:
                # Extract relevant fields and create pwsafe_entity instances
                username = row['Username']
                password = row['Password']
                url = row['URL']
                description = " ".join([row[key] for key in row.keys() if key not in ['Username', 'Password', 'URL']])
                
                password_entries.append(pwsafe_entity(username, password, url, description))

    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return password_entries

class pwsafe_entity:
    def __init__(self, principal, credential, link, description):
        self.principal = principal
        self.credential = credential
        self.link = link
        self.descr = description
    def length(self):
        return len(self.credential)
    #check for password reusing username
    def reuse_username(self):
#        return self.principal in self.credential
        pattern = re.escape(self.principal)

        overlapping_pattern = rf"(?=(.{5,})).*{pattern}"

        renamecheck= re.search(pattern,self.credential)
        
        simplematch = re.findall(overlapping_pattern, self.credential)
        if simplematch:
            print(f"WARNING: Found simple username match: {crayons.red(simplematch)}")

        lenMin = 5
        if renamecheck or simplematch: 
            print(f"simplecheck for username failed for {crayons.red(self.principal)}")
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
            longestmatch = max(similar_substring, key = len)
            print(f"WARNING: Fuzzy check failed: {crayons.red(longestmatch)}")
            return True
        return False
    #check if link or description is reused and give a warning when it does

    #check against common word match

    def is_common_or_bad_password(self):
        common_check = False
        commonp_lst= is_common_password(self.credential)
        if commonp_lst:
            common_check = True
        return common_check, commonp_lst
    # Check if the credential is reused in self' non-credential fields
    def reuse_identifier(self):
        check = False
        if fuzzycheck(self.credential, self.link)[0]:
            print (f"WARNING: Pass similiar to description: {crayons.red(fuzzycheck(self.credential, self.link)[1])}")
            check = True
        if fuzzycheck(self.credential, self.descr)[0]:
            print (f"WARNING: Pass similiar to description: {crayons.red(fuzzycheck(self.credential, self.descr)[1])}")
            check = True
            
            
        return check

    # Check if the credential is reused in other entities' non-credential fields
    def reuse_meta(self, other_entities):
        matches_global = []
        for entity in other_entities:
        
            if entity != self:  # Skip self
                matches = []
                if fuzzycheck(self.credential, entity.principal)[0]:
                    matches.append(f"Principal similar to {entity.principal}: {crayons.red(fuzzycheck(self.credential, entity.principal)[1])}")
                    check = True
                if fuzzycheck(self.credential, entity.credential)[0]:
                    matches.append(f"WARNING: reused Password for: {crayons.red(entity.desc)}")
                    check = True
                if fuzzycheck(self.credential, entity.link)[0]:
                    matches.append(f"Link similar to {entity.link}: {crayons.red(fuzzycheck(self.credential, entity.link)[1])}")
                    check = True
                if fuzzycheck(self.credential, entity.descr)[0]:
                    matches.append(f"Description similar to {entity.descr}: {crayons.red(fuzzycheck(self.credential, entity.descr)[1])}")
                    check = True
                if matches:
                    matches_global.append(matches)
                    print(f"WARNING: Matches found for credential '{self.credential}' against {entity.principal}, {entity.link}, and {entity.descr}:")
                    for match in matches:
                        print(match)
        if matches_global:
            return True
        return False

def main():
    #define password policy
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=2,  # need min. 2 uppercase letters
        numbers=2,  # need min. 2 digits
        special=2,  # need min. 2 special characters
        nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
    )

    #file import and convert to list of Class
    filename = "passwords.txt"  # Replace with the actual filename
    parsed_data = parse_password_file(filename)
    print (parsed_data)
    #ask for manual entry and append to list
    for entry in parsed_data:
        print(f"Username: {entry.principal}")
        print(f"Password: {entry.credential}")
        print(f"URL: {entry.link}")
        print(f"Description: {entry.descr}")
        print(f"Length of credential: {entry.length()}")
        print(f"Password Reuse Check: {entry.reuse_username()}")
        print(f"{entry.reuse_identifier()}")
        
        print("---")
    


    #assigning test entry
    entity1 = pwsafe_entity("username", "password123username","link","desc")
    entity2 = pwsafe_entity("email@example.com", "securepassword","example.com","email")
    entity3 = pwsafe_entity("je.ff@amazon.com", "Karsutoま0b$$eshun","amazon.co.jp","Amazon JP")    
    entity4 = pwsafe_entity('username','u5ername','username.com','big one')

    print(f"Length of credential 1: {entity1.length()}")
    print(f"Length of credential 2: {entity2.length()}")

    print(entity1.reuse_meta([entity2,entity3]))
    print(entity2.reuse_meta([entity1,entity2,entity3]))
    print(f"entity4 tested: {entity4.reuse_username()}")
    print(entity4.reuse_identifier())

    

if __name__ == "__main__":
    main()
