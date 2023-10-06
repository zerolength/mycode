#!/usr/bin/python3

"""tracking the iss using
   api.open-notify.org/astros.json | Alta3 Research"""

# notice we no longer need to import urllib.request or json
import requests
from datetime import datetime
from dateutil import tz
import reverse_geocode

## Define URL
MAJORTOM = 'http://api.open-notify.org/astros.json'
POS= 'http://api.open-notify.org/iss-now.json'
def main():
    """runtime code"""

    ## Call the webservice
    groundctrl = requests.get(MAJORTOM)
    pos = requests.get(POS)
    # send a post with requests.post()
    # send a put with requests.put()
    # send a delete with requests.delete()
    # send a head with requests.head()

    ## strip the json off the 200 that was returned by our API
    ## translate the json into python lists and dictionaries
    #print(groundctrl)
    helmetson = groundctrl.json()
    poisson = pos.json()
    ## display our Pythonic data
    print("\n\nConverted Python data")
    print(poisson)

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Los_Angeles')
    coords = poisson['iss_position']['longitude'], poisson['iss_position']['latitude']

    print('\n\nISS(nasa) in Space: \n Lon:', poisson['iss_position']['longitude'], 'Lat:', poisson['iss_position']['latitude'])
    print (reverse_geocode.search(coords))

    people = helmetson['people']
    print(people)

    sortedp = sorted(people, key =lambda x: x.get('craft'))
    for  astro in sortedp:
        print (f"{astro['name']} in {astro['craft']}")
        


if __name__ == "__main__":
    main()

