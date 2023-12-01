import requests
from bs4 import BeautifulSoup
import json
import time


cookies = {
    'sgID': 'f2f3db6c-f937-4488-b5f9-53556f70088b',
    '_abck': '3E5A01341DDF845520DEE6223E460CD8~0~YAAQNDUQAnWzbW+LAQAAs5QSnwrV0Ov335OV4bMoRNvTEu2CcMXrGgG1/nx/F+9Guf1Z7nLwcv3PTVwgr6MvWOG5w2nSuRYVlPFcf6F+jwyFz7BFmVFIf0koW9HhQNcHG801Szucgzd4kI9dq8p1fj3kZWo16y1pZQ4vGd3Z3RdRncwzoWpSj71ElBtF0TY1lMcTd9Y/eZkIjOnIn/CQMOP4oC7hS0AXhjUwQWR2luFiz6vMtxkE6+mxA3tacQcljXBUzX7booLJs/VkNWTI/6cqcWlqAd6d3Tv7fLdcxczKG1hanH3/boBfV34gfAw/uBnO7jjtCXbARJqZo8UjJnnJKvhjG4dpsU+Uo3Yu+a+IMvIu10cKppDJ3Lv02GNNWygDmIFBv/6sqP3lTAQX6Q2WmrLKQRyT73IuhzI=~-1~-1~-1',
    'ak_bmsc': '24AAD7993EF69FD9494C965DCE32BA19~000000000000000000000000000000~YAAQNDUQAmGzbW+LAQAAjQgSnxW8THHq8PtdMUgtv8BsPgXcn2twc6Hzw3bab8LkK5PSoXcgRFdqDkZRXZYWAzIF+VOWiLfbdJn90w1m1/Ea5v/EbgAycGZu4P/FhltGian9i+AWMOAaNwA1qrcxC87tgtNsOSNGKh+ecPkDHj/XKds0b9pJfrEFnW/nRFa/kM/4ZdKF1ki/kt+Ow+ApgPoANYdZMGQHzRLM4MG35tVlv9Kt1RQTg37ufpxC0mpEQdeTkyCuNIJEaFULKJZwfTEfSJfYrCwpT9tbilOcJS9DcgGzoxOrPFOhhXBHZMdSEroDKzlbdZz2C0GUohvDvSENYTpmOvXx8WBxhHWpLG5MP+qqPTqfYwFsrBpdSIN4MXSWnWYXSXauhnrysixSk//hgB8XstWFr1Kcerq+ijoQVyP1hTJCGeOXpRuCBA0AFV+RFI5UjmATaqZ6SLxluNjpnOETqS0FTZ8NpOr0RGj4QoPQvEFmdjXINqIpp5aWV3oc8wUg',
    'bm_sz': '992D52210388DC7DA05739720547FD44~YAAQNDUQAlyzbW+LAQAAlwESnxVXjevR1pYqsT+I30tZBtmSTHWaMaV88oky3egYp/oAN/Q6rqNc82IkgEqYDfq4vA0Gb/pDv8IQ2TYQbKIZ/W8HgsWp0hHcSE0SxbQOdLKHAhSpCPfy9h2s99abajRN/1H931vPDIDs1Dnutt3CIjge3rfbEaOVIFiborzx6EA7cjJi5Y9OZGpaejSfuhPANfMa0LKGa/QG6TRTixXPniMm6jsfbWpYsrdoyC10stLQXWCkMyCsbEcBoitk3R/NVzYqbTabfc0tHUWZgZZed9ncpNRG~4534583~4600630',
    'loyal-user': '{^%^22date^%^22:^%^222023-11-05T10:40:40.697Z^%^22^%^2C^%^22isLoyal^%^22:false}',
    'fsrndid': 'true',
    '_gcl_au': '1.1.1179955440.1699180841',
    '_ga_5M34ZH84YZ': 'GS1.1.1699180843.1.1.1699181000.52.0.0',
    '_ga': 'GA1.2.407080330.1699180843',
    '_ga_XGRRHHKH0P': 'GS1.1.1699180843.1.1.1699180993.59.0.0',
    '__q_state_9u7uiM39FyWVMWQF': 'eyJ1dWlkIjoiOGRmNjBkMGQtN2U1Yy00N2IyLWFkZTgtYzJmMzRkOTYyOTg3IiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJtZXNzZW5nZXJFeHBhbmRlZCI6ZmFsc2UsInByb21wdERpc21pc3NlZCI6ZmFsc2UsImNvbnZlcnNhdGlvbklkIjoiMTI2MDg4NjgwMjc0ODgwMjIzOCJ9',
    'RT': 'z=1&dm=www.similarweb.com&si=94091a8d-28c8-4b1a-a09c-a812337f1660&ss=lolcee4b&sl=3&tt=sqj&obo=2&rl=1&ld=3gv3&r=3l62szwn&ul=3gv3',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Nov+05+2023+13^%^3A43^%^3A14+GMT^%^2B0300+(^%^D0^%^9C^%^D0^%^BE^%^D1^%^81^%^D0^%^BA^%^D0^%^B2^%^D0^%^B0^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=95ab6d0a-7b29-4024-9e92-62dfbd02f98b&interactionCount=1&landingPath=NotLandingPage&groups=C0003^%^3A1^%^2CC0004^%^3A1^%^2CC0002^%^3A1^%^2CC0001^%^3A1&geolocation=RU^%^3BRYA&AwaitingReconsent=false',
    '_pk_id.1.fd33': '10e802c1942ed092.1699180844.',
    '_pk_ses.1.fd33': '1',
    '_gid': 'GA1.2.2004953993.1699180844',
    'fs_lua': '1.1699180995071',
    'fs_uid': '^#WA0BV^#a9f37ac6-beba-47d5-b42c-a0d51313f7b5:d8ca3e51-edb7-4501-a2b9-e5db4d4b34e7:1699180844586::3^#/1730716843',
    'OptanonAlertBoxClosed': '2023-11-05T10:41:08.572Z',
    'bm_sv': '627188A67DBA50DB822184C9485163C7~YAAQNDUQApKzbW+LAQAABnYUnxVxSoxj1Ap6Jvz6MVctERd0KqZZ2erCc5YN48hQe57AHlvLTCoVTzPMYqj+DbkO1e3rckF/aCJrhQdc6vP0dl+NPPNCmTv/pU9gZDSAxTrf/av87EjI/U4+YifyBeTykhZyg8IWx2fEQffopHZz8Lf58WYMGctd7fyIowZoZnwhK59ivnZnUz2W/PopTk5561jEQsjIhzh5e0HBa9yaRV8ntRJrVZATSbwlJsG1Nsx/3Q==~1',
    'dicbo_id': '^%^7B^%^22dicbo_fetch^%^22^%^3A1699180879842^%^7D',
    '_clck': '9lg8n5^|2^|fgg^|0^|1404',
    '_clsk': '1914o2b^|1699180997304^|2^|1^|x.clarity.ms/collect',
    'mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel': '^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^22^%^24device^%^3A18b9f129aeca1c-0c8c2f5cc841f7-d5c5429-15f900-18b9f129aeea1e^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2218b9f129aeca1c-0c8c2f5cc841f7-d5c5429-15f900-18b9f129aeea1e^%^22^%^2C^%^22sgId^%^22^%^3A^%^20^%^22f2f3db6c-f937-4488-b5f9-53556f70088b^%^22^%^2C^%^22site_type^%^22^%^3A^%^20^%^22lite^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22https^%^3A^%^2F^%^2Fwww.similarweb.com^%^2F^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22www.similarweb.com^%^22^%^2C^%^22session_id^%^22^%^3A^%^20^%^22c2cee849-f807-4091-aaec-02db2c7141d7^%^22^%^2C^%^22session_first_event_time^%^22^%^3A^%^20^%^222023-11-05T10^%^3A41^%^3A21.229Z^%^22^%^2C^%^22url^%^22^%^3A^%^20^%^22https^%^3A^%^2F^%^2Fwww.similarweb.com^%^2F^%^22^%^2C^%^22language^%^22^%^3A^%^20^%^22en-us^%^22^%^2C^%^22section^%^22^%^3A^%^20^%^22home^%^22^%^2C^%^22sub_section^%^22^%^3A^%^20^%^22^%^22^%^2C^%^22sub_sub_section^%^22^%^3A^%^20^%^22^%^22^%^2C^%^22Fullstory^%^20Session^%^22^%^3A^%^20null^%^2C^%^22last_event_time^%^22^%^3A^%^201699181000378^%^2C^%^22is_sw_user^%^22^%^3A^%^20false^%^2C^%^22first_time_visitor^%^22^%^3A^%^20false^%^2C^%^22cookies^%^22^%^3A^%^20^%^22accepted^%^22^%^7D',
    '_gat_UA-42469261-1': '1',
    '_uetsid': 'db2288d07bc711eeb5abd964d8c320b5',
    '_uetvid': 'db2290b07bc711ee8b51a3e3544107d1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.similarweb.com/',
    'Cookie': 'sgID=f2f3db6c-f937-4488-b5f9-53556f70088b; _abck=3E5A01341DDF845520DEE6223E460CD8~0~YAAQNDUQAnWzbW+LAQAAs5QSnwrV0Ov335OV4bMoRNvTEu2CcMXrGgG1/nx/F+9Guf1Z7nLwcv3PTVwgr6MvWOG5w2nSuRYVlPFcf6F+jwyFz7BFmVFIf0koW9HhQNcHG801Szucgzd4kI9dq8p1fj3kZWo16y1pZQ4vGd3Z3RdRncwzoWpSj71ElBtF0TY1lMcTd9Y/eZkIjOnIn/CQMOP4oC7hS0AXhjUwQWR2luFiz6vMtxkE6+mxA3tacQcljXBUzX7booLJs/VkNWTI/6cqcWlqAd6d3Tv7fLdcxczKG1hanH3/boBfV34gfAw/uBnO7jjtCXbARJqZo8UjJnnJKvhjG4dpsU+Uo3Yu+a+IMvIu10cKppDJ3Lv02GNNWygDmIFBv/6sqP3lTAQX6Q2WmrLKQRyT73IuhzI=~-1~-1~-1; ak_bmsc=24AAD7993EF69FD9494C965DCE32BA19~000000000000000000000000000000~YAAQNDUQAmGzbW+LAQAAjQgSnxW8THHq8PtdMUgtv8BsPgXcn2twc6Hzw3bab8LkK5PSoXcgRFdqDkZRXZYWAzIF+VOWiLfbdJn90w1m1/Ea5v/EbgAycGZu4P/FhltGian9i+AWMOAaNwA1qrcxC87tgtNsOSNGKh+ecPkDHj/XKds0b9pJfrEFnW/nRFa/kM/4ZdKF1ki/kt+Ow+ApgPoANYdZMGQHzRLM4MG35tVlv9Kt1RQTg37ufpxC0mpEQdeTkyCuNIJEaFULKJZwfTEfSJfYrCwpT9tbilOcJS9DcgGzoxOrPFOhhXBHZMdSEroDKzlbdZz2C0GUohvDvSENYTpmOvXx8WBxhHWpLG5MP+qqPTqfYwFsrBpdSIN4MXSWnWYXSXauhnrysixSk//hgB8XstWFr1Kcerq+ijoQVyP1hTJCGeOXpRuCBA0AFV+RFI5UjmATaqZ6SLxluNjpnOETqS0FTZ8NpOr0RGj4QoPQvEFmdjXINqIpp5aWV3oc8wUg; bm_sz=992D52210388DC7DA05739720547FD44~YAAQNDUQAlyzbW+LAQAAlwESnxVXjevR1pYqsT+I30tZBtmSTHWaMaV88oky3egYp/oAN/Q6rqNc82IkgEqYDfq4vA0Gb/pDv8IQ2TYQbKIZ/W8HgsWp0hHcSE0SxbQOdLKHAhSpCPfy9h2s99abajRN/1H931vPDIDs1Dnutt3CIjge3rfbEaOVIFiborzx6EA7cjJi5Y9OZGpaejSfuhPANfMa0LKGa/QG6TRTixXPniMm6jsfbWpYsrdoyC10stLQXWCkMyCsbEcBoitk3R/NVzYqbTabfc0tHUWZgZZed9ncpNRG~4534583~4600630; loyal-user={^%^22date^%^22:^%^222023-11-05T10:40:40.697Z^%^22^%^2C^%^22isLoyal^%^22:false}; fsrndid=true; _gcl_au=1.1.1179955440.1699180841; _ga_5M34ZH84YZ=GS1.1.1699180843.1.1.1699181000.52.0.0; _ga=GA1.2.407080330.1699180843; _ga_XGRRHHKH0P=GS1.1.1699180843.1.1.1699180993.59.0.0; __q_state_9u7uiM39FyWVMWQF=eyJ1dWlkIjoiOGRmNjBkMGQtN2U1Yy00N2IyLWFkZTgtYzJmMzRkOTYyOTg3IiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJtZXNzZW5nZXJFeHBhbmRlZCI6ZmFsc2UsInByb21wdERpc21pc3NlZCI6ZmFsc2UsImNvbnZlcnNhdGlvbklkIjoiMTI2MDg4NjgwMjc0ODgwMjIzOCJ9; RT=z=1&dm=www.similarweb.com&si=94091a8d-28c8-4b1a-a09c-a812337f1660&ss=lolcee4b&sl=3&tt=sqj&obo=2&rl=1&ld=3gv3&r=3l62szwn&ul=3gv3; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Nov+05+2023+13^%^3A43^%^3A14+GMT^%^2B0300+(^%^D0^%^9C^%^D0^%^BE^%^D1^%^81^%^D0^%^BA^%^D0^%^B2^%^D0^%^B0^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=95ab6d0a-7b29-4024-9e92-62dfbd02f98b&interactionCount=1&landingPath=NotLandingPage&groups=C0003^%^3A1^%^2CC0004^%^3A1^%^2CC0002^%^3A1^%^2CC0001^%^3A1&geolocation=RU^%^3BRYA&AwaitingReconsent=false; _pk_id.1.fd33=10e802c1942ed092.1699180844.; _pk_ses.1.fd33=1; _gid=GA1.2.2004953993.1699180844; fs_lua=1.1699180995071; fs_uid=^#WA0BV^#a9f37ac6-beba-47d5-b42c-a0d51313f7b5:d8ca3e51-edb7-4501-a2b9-e5db4d4b34e7:1699180844586::3^#/1730716843; OptanonAlertBoxClosed=2023-11-05T10:41:08.572Z; bm_sv=627188A67DBA50DB822184C9485163C7~YAAQNDUQApKzbW+LAQAABnYUnxVxSoxj1Ap6Jvz6MVctERd0KqZZ2erCc5YN48hQe57AHlvLTCoVTzPMYqj+DbkO1e3rckF/aCJrhQdc6vP0dl+NPPNCmTv/pU9gZDSAxTrf/av87EjI/U4+YifyBeTykhZyg8IWx2fEQffopHZz8Lf58WYMGctd7fyIowZoZnwhK59ivnZnUz2W/PopTk5561jEQsjIhzh5e0HBa9yaRV8ntRJrVZATSbwlJsG1Nsx/3Q==~1; dicbo_id=^%^7B^%^22dicbo_fetch^%^22^%^3A1699180879842^%^7D; _clck=9lg8n5^|2^|fgg^|0^|1404; _clsk=1914o2b^|1699180997304^|2^|1^|x.clarity.ms/collect; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^22^%^24device^%^3A18b9f129aeca1c-0c8c2f5cc841f7-d5c5429-15f900-18b9f129aeea1e^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2218b9f129aeca1c-0c8c2f5cc841f7-d5c5429-15f900-18b9f129aeea1e^%^22^%^2C^%^22sgId^%^22^%^3A^%^20^%^22f2f3db6c-f937-4488-b5f9-53556f70088b^%^22^%^2C^%^22site_type^%^22^%^3A^%^20^%^22lite^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22https^%^3A^%^2F^%^2Fwww.similarweb.com^%^2F^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22www.similarweb.com^%^22^%^2C^%^22session_id^%^22^%^3A^%^20^%^22c2cee849-f807-4091-aaec-02db2c7141d7^%^22^%^2C^%^22session_first_event_time^%^22^%^3A^%^20^%^222023-11-05T10^%^3A41^%^3A21.229Z^%^22^%^2C^%^22url^%^22^%^3A^%^20^%^22https^%^3A^%^2F^%^2Fwww.similarweb.com^%^2F^%^22^%^2C^%^22language^%^22^%^3A^%^20^%^22en-us^%^22^%^2C^%^22section^%^22^%^3A^%^20^%^22home^%^22^%^2C^%^22sub_section^%^22^%^3A^%^20^%^22^%^22^%^2C^%^22sub_sub_section^%^22^%^3A^%^20^%^22^%^22^%^2C^%^22Fullstory^%^20Session^%^22^%^3A^%^20null^%^2C^%^22last_event_time^%^22^%^3A^%^201699181000378^%^2C^%^22is_sw_user^%^22^%^3A^%^20false^%^2C^%^22first_time_visitor^%^22^%^3A^%^20false^%^2C^%^22cookies^%^22^%^3A^%^20^%^22accepted^%^22^%^7D; _gat_UA-42469261-1=1; _uetsid=db2288d07bc711eeb5abd964d8c320b5; _uetvid=db2290b07bc711ee8b51a3e3544107d1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    'TE': 'trailers',
}


with open ('source.txt') as file:
    src = file.read()
    src = src.replace('\n', ' ')
    res_src = src.split(' ')
for url in res_src:
    time.sleep(5)
    response = requests.get(f'https://www.similarweb.com/website/{url[8::]}/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    views = soup.find('p', class_="engagement-list__item-value").text
    print(views)