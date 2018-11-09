#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import sys
import md5
import httplib
from datetime import datetime

#
# COMPLETE WITH YOUR DATA
#
# Subdomain
requestUri = '/en/rapi/cacheSettings/www.example.com./1'

# General settings of a domain
# requestUri = '/en/rapi/cacheSettings/ALL:example.com./1'

api_key    = '';
secret     = '';

#
# REQUEST SPECIFIC DATA
#
requestMethod      = 'GET'
requestContentType = 'application/json'
requestDate        = datetime.now().strftime("%y-%m-%dT%H:%M:%S")

# For listing the body is empty
# The md5 of the empty string should be: d41d8cd98f00b204e9800998ecf8427e
requestBody = ''

#
# PREPARE THE AUTHORIZATION KEY
#
signing_string        = md5.new(requestBody).hexdigest() + '#' + requestMethod + '#' + requestUri + '#' + requestContentType + '#' + requestDate
datekey_hexmac        = hmac.new('MYRA'+secret, msg=requestDate, digestmod=hashlib.sha256).hexdigest()
signingkey_hexmac     = hmac.new(datekey_hexmac, msg='myra-api-request', digestmod=hashlib.sha256).hexdigest()
signature             = hmac.new(signingkey_hexmac, msg=signing_string, digestmod=hashlib.sha512).digest()
request_authorization = 'MYRA ' + api_key + ':' + base64.b64encode(signature)

#
# UNCOMMENT FOR DEBUG
#
#print 'Signing string: ' + signing_string
#print 'DateKey: ' + datekey_hexmac
#print 'SigningKey: ' + signingkey_hexmac
#print 'Signature: ' + base64.b64encode(signature).decode()
#print request_authorization

#
# EXECUTE THE REQUEST
#
headers = {
    "Content-Type": requestContentType,
    "Date": requestDate,
    "Authorization": request_authorization
}

conn = httplib.HTTPSConnection("api.myracloud.com")
conn.request(requestMethod, requestUri, requestBody, headers)

r1   = conn.getresponse()
data = r1.read()

conn.close()

#
# TEST OUTPUT
#
print r1.status
print r1.reason
print data

