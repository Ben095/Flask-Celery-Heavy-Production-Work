import lepl.apps.rfc3696

str = 'u003egetflat@flattummytea.com'


email_validator = lepl.apps.rfc3696.Email()
if not email_validator(str):
    pass
else:
    print "EMAILS HERE", str.decode( 'unicode-escape' )