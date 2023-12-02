import re

str = 'https://catalog.wb.ru/catalog/bl_shirts/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat=8126&curr=rub&dest=-1257786&sort=popular&spp=28'
str = str[29::]
print(str)
pattern = (r'^/\w+')
print(re.findall(pattern, str))