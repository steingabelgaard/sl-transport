import requests
import xmltodict
from dict2xml import dict2xml

login_url = 'https://services.techhouse.dk/webTourManager/1.12/MajorAccount.svc/basHttps'
url=        'https://services.techhouse.dk/webTourManager/1.12/Service.svc/basHttps'
host =      'services.techhouse.dk'

login_url = 'https://test-services.techhouse.dk/webTourManager/1.12/MajorAccount.svc/basHttps'
url=        'https://test-services.techhouse.dk/webTourManager/1.12/Service.svc/basHttps'
host =      'test-services.techhouse.dk'


soap_url =  'https://services.techhouse.dk/webTourManager/'

cookies = None

MAXREPEATREAD = 2

def login():
    global cookies
    global login_url
    global soap_url
    global host

    headers = { 'Content-Type':'text/xml;charset=UTF-8',
                'SOAPAction':soap_url+'IAuth/Login',
                'Host':host}

    xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager">
            <soapenv:Header/>
            <soapenv:Body>
                <web:Login>
                    <web:OwnerIDno>47</web:OwnerIDno>
                    <web:Alias>bus</web:Alias>
                    <web:AuthKey>66f59eee-41a8-46dc-bfa7-6d064a9d2a3c</web:AuthKey>
                </web:Login>
            </soapenv:Body>
        </soapenv:Envelope>"""

    #print(headers)
    r = requests.post(login_url, headers=headers, data=xml)

    #print (r.text)
    #print (r.status_code)
    if r.status_code == 200 :
        xdict = xmltodict.parse(r.text)
        authenticated = xdict['s:Envelope']['s:Body']['LoginResponse']['LoginResult']['a:Access']['b:IsAuthenticated']

        if authenticated == "true":
            cookies = r.cookies    
    return authenticated
    
def logoff():
    global cookies
    global login_url
    global soap_url
    global host

    headers = { 'Content-Type':'text/xml;charset=UTF-8',
                'SOAPAction':soap_url+'IAuth/Logoff',
                'Host':host}

    xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager">
            <soapenv:Header/>
            <soapenv:Body>
            </soapenv:Body>
        </soapenv:Envelope>"""

    #print(headers)
    r = requests.post(login_url, headers=headers, data=xml)

    #print (r.text)
    #print (r.status_code)
    if r.status_code == 200 :
        xdict = xmltodict.parse(r.text)
        authenticated = xdict['s:Envelope']['s:Body']['LogoffResponse']['LogoffResult']['a:Access']['b:IsAuthenticated']

        if authenticated == "false":
            cookies = None  

def repeatRead(req,m):
    repeat_read = MAXREPEATREAD
    ok = False

    while repeat_read:
        r = req()

        if r.status_code == 200 :
            xdict = xmltodict.parse(r.text)
           # x =dicttoxml(xdict)
            try:
                authenticated = xdict['s:Envelope']['s:Body'][m+'Response'][m+'Result']['a:Access']['b:IsAuthenticated']
            except:
                authenticated = "true"

            if authenticated == "true":
                repeat_read = False
                ok=True
            else:
                login()
                repeat_read = repeat_read -1
        else:
            login()
            repeat_read = repeat_read -1
    if ok:
        return xdict['s:Envelope']['s:Body'][m+'Response'][m+'Result']

def customer_Create(AccountNum,Name,Phone):
    c = 'ICustomer'
    m = 'Customer_Create'

    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
            <soapenv:Header/>
            <soapenv:Body>
                <web:Customer_Create>
                    <web:CustomerData>
                        <web1:AccountNum>""" + AccountNum + """</web1:AccountNum>
                        <web1:Name>""" + Name + """</web1:Name>
                        <web1:Phone>""" + Phone + """</web1:Phone>
                    </web:CustomerData>
                </web:Customer_Create>
            </soapenv:Body>
        </soapenv:Envelope>"""

        #print(url,headers,xml)
        r = requests.post(url, headers=headers, data=xml,cookies=cookies)

        return r

    return repeatRead(do_req,m)

def Customer_GetFromSearchPattern(pattern):
    c = 'ICustomer'
    m = 'Customer_GetFromSearchPattern'

    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
            <soapenv:Header/>
            <soapenv:Body>
                <web:Customer_GetFromSearchPattern>
                    <web:SearchTerm>"""+pattern+"""</web:SearchTerm>
                </web:Customer_GetFromSearchPattern>
            </soapenv:Body>
        </soapenv:Envelope>"""

        #print(url,headers,xml)
        r = requests.post(url, headers=headers, data=xml,cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tour_GetFromLastUpdated(GetFrom):
    c = 'ITour'
    m = 'Tour_GetFromLastUpdated'

    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:Tour_GetFromLastUpdated>
                        <web:GetFrom>"""+GetFrom+"""</web:GetFrom>
                    </web:Tour_GetFromLastUpdated>
                </soapenv:Body>
            </soapenv:Envelope>"""

        #print(url,headers,xml)
        r = requests.post(url, headers=headers, data=xml,cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tour_Get(IDno):
    c = 'ITour'
    m = 'Tour_Get'

    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:Tour_Get>
                        <web:IDno>"""+IDno+"""</web:IDno>
                    </web:Tour_Get>
                </soapenv:Body>
            </soapenv:Envelope>"""

        #print(url,headers,xml)
        r = requests.post(url, headers=headers, data=xml,cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tourPoint_CreateFromAddressWithLatLong(Name,Address1,ZipCode,Town,Country,Latitude,Longitude):
    #input : Name: xsd:string, Address1: xsd:string, ZipCode: xsd:string, Town: xsd:string, Country: xsd:string, Latitude: xsd:decimal, Longitude: xsd:decimal
    c = 'ITour'
    m = 'TourPoint_CreateFromAddressWithLatLong'
  
    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:TourPoint_CreateFromAddressWithLatLong>
                        <web:Name>"""+ Name +"""</web:Name>
                        <web:Address1>"""+ Address1 +"""</web:Address1>
                        <web:ZipCode>"""+ ZipCode +"""</web:ZipCode>
                        <web:Town>"""+ Town +"""</web:Town>
                        <web:Country>"""+ Country +"""</web:Country>
                        <web:Latitude>"""+ Latitude +"""</web:Latitude>
                        <web:Longitude>"""+ Longitude +"""</web:Longitude>
                    </web:TourPoint_CreateFromAddressWithLatLong>
                </soapenv:Body>
            </soapenv:Envelope>"""

        r = requests.post(url, headers=headers, data=xml.encode("utf-8"),cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tourPoint_CreateFromAddress2WithLatLong(Name,Address1,Address2,ZipCode,Town,Country,Latitude,Longitude):
    #input : Name: xsd:string, Address1: xsd:string, Address2: xsd:string, ZipCode: xsd:string, Town: xsd:string, Country: xsd:string, Latitude: xsd:decimal, Longitude: xsd:decimal
    c = 'ITour'
    m = 'TourPoint_CreateFromAddress2WithLatLong'
  
    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}
  
        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:TourPoint_CreateFromAddress2WithLatLong>
                        <web:Name>"""+ Name +"""</web:Name>
                        <web:Address1>"""+ Address1 +"""</web:Address1>
                        <web:Address2>"""+ Address2 +"""</web:Address2>
                        <web:ZipCode>"""+ ZipCode +"""</web:ZipCode>
                        <web:Town>"""+ Town +"""</web:Town>
                        <web:Country>"""+ Country +"""</web:Country>
                        <web:Latitude>"""+ Latitude +"""</web:Latitude>
                        <web:Longitude>"""+ Longitude +"""</web:Longitude>                        
                    </web:TourPoint_CreateFromAddress2WithLatLong>
                </soapenv:Body>
            </soapenv:Envelope>"""

        r = requests.post(url, headers=headers, data=xml.encode("utf-8"),cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tour_Create(Name,NoPersons,StartDateTime,EndDateTime):
    c = 'ITour'
    m = 'Tour_Create'
  
    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:Tour_Create>
                        <web:TourData>
                            <web1:AttPerson>JDa</web1:AttPerson>
                            <web1:EndDateTime>"""+ EndDateTime +"""</web1:EndDateTime>
                            <web1:Name>"""+ Name +"""</web1:Name>
                            <web1:NoPersons>"""+ NoPersons +"""</web1:NoPersons>
                            <web1:StartDateTime>"""+ StartDateTime +"""</web1:StartDateTime>
                            <web1:Status>10</web1:Status>
                        </web:TourData>
                    </web:Tour_Create>
                </soapenv:Body>
            </soapenv:Envelope>"""

        r = requests.post(url, headers=headers, data=xml.encode("utf-8"),cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tour_SetLocation_NewTourPoint(location,TourIDno,tp):
    #input : Name: xsd:string, Address1: xsd:string, Address2: xsd:string, ZipCode: xsd:string, Town: xsd:string, Country: xsd:string, Latitude: xsd:decimal, Longitude: xsd:decimal
    c = 'ITour'
    m = 'Tour_Set'+location+'_TourPoint'
  
    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        for key in dict(tp):  #remove all parms
            if key[0] == '@' : del tp[key]

        xloc = dict2xml(tp, wrap="web:"+location, newlines=False)
        
        for key in tp:
            if tp[key] == None : xloc=xloc.replace('<'+key+'>None</'+key+'>', '<'+key+'/>')

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:a="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:"""+m+""">
                        <web:TourIDno>"""+ TourIDno +"""</web:TourIDno>
                        """ + xloc + """
                    </web:"""+m+""">
                </soapenv:Body>
            </soapenv:Envelope>"""

        r = requests.post(url, headers=headers, data=xml.encode("utf-8"),cookies=cookies)

        return r

    return repeatRead(do_req,m)

def tour_SetCustomer(TourIDno,cus):
    c = 'ITour'
    m = 'Tour_SetCustomer'
  
    global cookies
    global url
    global soap_url
    global host

    def do_req():
        headers = { 'Content-Type':'text/xml;charset=UTF-8',
                    'SOAPAction': soap_url+c+'/'+m,
                    'Host':host}

        for key in dict(cus):  #remove all parms
            if key[0] == '@' : del cus[key]
            if key == 'b:PaymentTerm' : del cus[key]

        x = dict2xml(cus, wrap="web:Customer", newlines=False)
        
        for key in cus:
            if cus[key] == None : x=x.replace('<'+key+'>None</'+key+'>', '<'+key+'/>')

        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:b="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
                <soapenv:Header/>
                <soapenv:Body>
                    <web:"""+m+""">
                        <web:TourIDno>"""+ TourIDno +"""</web:TourIDno>
                        """ + x + """
                    </web:"""+m+""">
                </soapenv:Body>
            </soapenv:Envelope>"""

        r = requests.post(url, headers=headers, data=xml,cookies=cookies)

        return r

    return repeatRead(do_req,m)

def test() :
    headers = {'Content-Type':'text/xml;charset=UTF-8',
    'SOAPAction':'https://services.techhouse.dk/webTourManager/ITour/Tour_GetFromLastUpdated',
    'Host':'services.techhouse.dk'}

    xml2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
        <soapenv:Header/>
        <soapenv:Body>
            <web:Tour_GetFromLastUpdated>
                <web:GetFrom>2021-05-16T11:05:53.7550017+02:00</web:GetFrom>
            </web:Tour_GetFromLastUpdated>
        </soapenv:Body>
    </soapenv:Envelope>"""
    print(url,headers,xml2)
    r2 = requests.post(url, headers=headers, data=xml2,cookies=cookies)

    headers = {'Content-Type':'text/xml;charset=UTF-8',
    'SOAPAction':'https://services.techhouse.dk/webTourManager/ICustomer/Customer_Create',
    'Host':'services.techhouse.dk'}

    xml2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="https://services.techhouse.dk/webTourManager" xmlns:web1="http://schemas.datacontract.org/2004/07/webTourManager.Classes">
        <soapenv:Header/>
        <soapenv:Body>
            <web:Customer_Create>
                <web:CustomerData>
                    <web1:AccountNum>TEST456</web1:AccountNum>
                    <web1:Name>Test debitor2</web1:Name>
                    <web1:Phone>12345699</web1:Phone>
                </web:CustomerData>
            </web:Customer_Create>
        </soapenv:Body>
    </soapenv:Envelope>"""
    print(url,headers,xml2)

    r2 = requests.post(url, headers=headers, data=xml2,cookies=cookies)
    #print (r2.text)

    xpars = xmltodict.parse(r2.text)
    print (xpars['s:Envelope']['s:Body']['Customer_CreateResponse']['Customer_CreateResult']['a:Access']['b:IsAuthenticated'])
    print (xpars['s:Envelope']['s:Body']['Customer_CreateResponse']['Customer_CreateResult']['a:Content']['b:IDnos'])
    print (xpars['s:Envelope']['s:Body']['Customer_CreateResponse']['Customer_CreateResult']['a:Notifications']['b:NotificationItem']['b:Description'])

    def gen_dict_extract(key, var):
        if hasattr(var,'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in gen_dict_extract(key, d):
                            yield result

    for i in gen_dict_extract('b:IsAuthenticated',xpars):
        print(i)
    for i in gen_dict_extract('b:Description',xpars):
        print(i)

    res = customer_Create('TEST456','Test debitor2','12345699')
    print(res)
    print (res['a:Access']['b:IsAuthenticated'])
    print (res['a:Content']['b:IDnos'])
    print (res['a:Notifications']['b:NotificationItem']['b:Description'])
    print()

#print (res['a:Notifications']['b:NotificationItem']['b:Description'])
logoff()
login()

#tp1 = tourPoint_CreateFromAddress2WithLatLong('test3','Provevej 3','kontral','1111','hjemby','DK','9','11')

res = tour_GetFromLastUpdated('2022-07-06T00:00:00.00000+02:00')
print(res)

tour = tour_Create('Testtur6','45','2022-07-22T11:05:00.0000000+02:00','2022-07-22T11:35:00.0000000+02:00')
tourid = tour['a:Content']['b:TourIDno']
print(tour['a:Content']['b:TourIDno'])
cus = Customer_GetFromSearchPattern('42438838')
tour1 = tour_SetCustomer(tour['a:Content']['b:TourIDno'],cus['a:Content']['b:Customers']['b:CustomerItem'])
tp1 = tourPoint_CreateFromAddressWithLatLong('test6','Prøvevej 4','1111','hjemby','DK','55','11')
tour2 = tour_SetLocation_NewTourPoint('StartLocation',tour['a:Content']['b:TourIDno'],tp1)
camp1 = tourPoint_CreateFromAddress2WithLatLong('SL2022, Brandhøjgårdsvej','Brandhøjgårdsvej','Ind fra Hovedgaden/Hedehusene','2640','Hedehusene','DK','55.62675','12.18535')
tour3 = tour_SetLocation_NewTourPoint('EndLocation',tour['a:Content']['b:TourIDno'],camp1)

tour4 = tour_Get(tourid)
print(tour4)


res = tour_GetFromLastUpdated('2022-07-10T21:12:44.90432+02:00')
res = tour_GetFromLastUpdated('2022-07-06T00:00:00.00000+02:00')
print(res)
print (res['a:Access']['b:IsAuthenticated'])
print (res['a:Content']['b:TourIDnos'])
