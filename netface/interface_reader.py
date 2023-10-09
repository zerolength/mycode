import netifaces


def ifaces(seq):
#    for i in netifaces.interfaces():
#        try:
#            print( netifaces.ifaddresses(i))
    #        print(netifaces.ifaddresses(i)[netifaces.AF_LINK])
    #        print(netifaces.ifaddresses(i)[netifaces.AF_LINK][0]['addr'])
    #        print(netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'])
    #    except:
    #        print('placehodler')
    print (netifaces.ifaddresses(seq)[netifaces.AF_LINK][0]['addr'])
    print (netifaces.ifaddresses(seq)[netifaces.AF_INET][0]['addr'])
def main():
    
    print (netifaces.interfaces())
    seq=   input ("seq")
    na = netifaces.interfaces()[int(seq)]
    ifaces(na)


if __name__ == "__main__":
    main()

