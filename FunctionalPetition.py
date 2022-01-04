##################################################################################################
                            ### API TEST  v0.1 2022-01-03 ####
                              #PERFORMS FUNCTIONAL TESTING
##################################################################################################

import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import csv
import string

###################### USER MANUALLY INSERT auth_token :: 
auth_token = 'YbwwFwyA1k18fg5d0fDyCepbghOks9uC9OxZXrctW+hdUpx/cb+uSEQb6oFrXrnFNJM4+Y51249X7m8lMu66JkUCqc/q1HdtCdJGcmqtV+m4/f1dMS071UGIGO5Qm3nAGTHQWIzWHvFd9EPJ7o8yT7ekGOiBVpVMjX2J1bsH341SOEyf6Djye+AGhqAN438BUiLSrgRiOvaQljFvEzjIsTSioCCtq7liw3YX0zj+XURyzjKWtEF/foK9IRsRJmB3c9xkf7CWNNRaq8RSFS9XqXNA6u09XPNgO7eLOw270OW/bjGgQKNMSc5kPNGGbXzyil6ooRUheB6unrkUyxXa4xYGJ/ITJAEzCPyBIxp6YIINGX72NAZ6MyAPrcdBblnPHespUw4M2N54Z2MvoDXpdyT8p8BTmcmDjKB3DW07H7/kksgAkp9ZqLC2DPO9lgXaq6o6FXndHUJJIoW0hIrxzu1aFuu44zmCMezCTkYfCcgdXbG3Sl1j0sYUQVx22fYd+MhglMU0V7lsUIKJouFWOrLu+MUTwPhqxSwf5FVS+rTyyzM3c70zbQUneSAD13m+PNaGN2hLb3CaML5mYfFe/r3Qn8gcms9FXN9VEORseo9YK4rqkLHuSUXaecyok+SsZJ4XqQ4T59v6bs5c4M37vq4RxbtQwXXnu4BbuJZ7EpCGdb+yU2MARlLNE3c60+B3LE2AFrEWcFU3QytJadxBDATkf13Nk/H3ec2v6qG0J7ttxmTBAmf6As/99HgeAGwBUixUiXAuK/z1Naa4KK7fwaD1vZ9sY8a2P0dD9usqYjV3F6oA8Qzg3mqunUFm6ssF0LX2AdOutwwHK1D3x3Pf5hXyQT3cGStHP0kv+6Vm1KTzIV8+IZCoh27Q7Ovn78hMsi/3jcI1xmUa29mJYh4S/Fu1GcU5PZ9yA4FGFVsOSrv0w7j3UJ6KADpIs2OrbD9KmLF6nGTv1e40McLS3ZauZBRRr3bmj+dZTwodrZIQdxtVJvS9V6xfB8RduGkcwAdPzOjbvUVhO6TOWG9BT3ejWyvcRZaYn3AdMqWcSc4a2ky5WqxdNGsK2u7fbp6F7R1RljQqIr2shM5e07ggHP5nV0lWp2gk8YaZ7wNx/CFTvoNfn4P6PaCy2mJ2DcvCIuRj'
######################

# Opening CSV file
df = pd.read_csv(r'CoreResources.Location.csv')
_ids = df.iloc[:, 0]
_enterpriseIds = df.iloc[:, 1]

# Prepare petitions
baseUrl = 'https://localhost:44337/api/v1/enterprises/'
responses = []
expectRes = []
testName = []
urls = []
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " +  auth_token

# 3 OK Found
for i in range(0,3,1):    
    url = baseUrl + _enterpriseIds[i] + '/locations/' + _ids[i]
    urls.append(url)
    expectRes.append('200')
    testName.append('OK')    

# 3 Not Found 
for i in range(4,7,1):    
    url = baseUrl + _ids[i] + '/locations/' + _enterpriseIds[i]    
    urls.append(url)
    expectRes.append('404')
    testName.append('NOT FOUND')

############# SINGULAR TEST
# Bad Request 
url = baseUrl + '1' + '/locations/' + '2'        
urls.append(url)
expectRes.append('400')
testName.append('BAD REQUEST')    

############# Execute petitions
for url in urls:
    resp = requests.get(url, headers=headers, verify = False)
    responses.append(resp)

# Not Authorized
url = baseUrl + _enterpriseIds[0] + '/locations/' + _ids[0]
headers["Authorization"] = "Bearer " +  string.ascii_letters
resp = requests.get(url, headers=headers, verify = False)
responses.append(resp)
expectRes.append('401')
testName.append('NOT AUTHORIZED')   

print(len(urls),len(responses),len(expectRes),len(testName))
#Write to a CSV File
with open('TestResults.csv', 'w', newline = '') as f:
    fnames = ['Test Performed',
        'Expected Response',
        'Responses',
        'Responses.text']

    writer = csv.DictWriter(f, fieldnames = fnames)
    i = 0
    writer.writeheader()
    for i in range(0,len(responses)):
        writer.writerow({'Test Performed' : testName[i], 
                         'Expected Response' : expectRes[i], 
                         'Responses' : responses[i], 
                         'Responses.text' : responses[i].text})
f.close()

# Display results
okcount = 0
failcount = 0
for i in range(0,len(testName)):    
    if int(expectRes[i]) == responses[i].status_code:
        okcount = okcount + 1
    else:
        failcount = failcount + 1 
        print('\n','Fail at :', i + 1)
print('#'*100)
print("# Tests Passed: ", okcount, "   <->    # Failed Tests: ", failcount)
print('#'*100)