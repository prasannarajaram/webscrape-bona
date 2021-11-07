import re
from bs4 import BeautifulSoup as soup

#Check if the string starts with "The" and ends with "Spain":

txt = '''
(<div class="accordion__title">
                        Aqua
                        <div class="accordion__icon__plus accordion__icon--show">
<img alt="Expand Ingredient" src="/.resources/bona/themes/bona-us/img/global/accordion/plus-mark.png"/>
</div>
<div class="accordion__icon__minus">
<img alt="Expand Ingredient" src="/.resources/bona/themes/bona-us/img/global/accordion/minus-mark.png"/>
</div>
</div>, <div class="accordion__content">
<p>Water is a solvent. Water is used in a many different manufactured products and is considered to be a safe, organic substitute for harsher chemicals. Water is used as a way to dissolve other chemicals into a safe cleaning solution. The term “aqua” refers to water that is free from impurities.</p>
<p><strong>CAS Number:</strong> 7732-18-5</p>
</div>)
'''
print(type(txt))
x = soup(txt, 'lxml')
item = x.find(class_="accordion__title").text.strip()
item_desc = x.find(class_="accordion__content").find_all('p')
ingre_details = []
ingre_details.append(item)
for desc in item_desc:
    foo = desc.text
    foo = foo.replace("\xa0","").replace("CAS Number:","")
    ingre_details.append(foo)

print(ingre_details)