import tldextract


def isDomain( str ):
    t_parse = tldextract.extract( str )
    if t_parse.subdomain == '' and t_parse.domain != '' and t_parse.suffix != '':
        return True
    else:
        return False
