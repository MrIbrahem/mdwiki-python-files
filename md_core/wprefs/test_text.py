import pywikibot
from wprefs.wpref_text import fix_page

text = """{{Infocaseta Tratament medical|Name=Demența cu corpi Lewy|Image=Lewy body in the substantia nigra from a person with Parkinson's disease.jpg|caption=[[Microfotografie|Imagine microscopică]] a unui [[corp Lewy]] (săgeată) într-un neuron al [[substanței negre]]; bară de scalare=20 microni (0,02 mm)|field=[[Neurologie]], [[psihiatrie]]|complications=|prevention=|treatment=|medication=[[Inhibitori ai acetilcolinesterazei]] precum [[donepezil]] și [[rivastigmină]];<ref name=Taylor2020Cognitive> Taylor JP ''et al.'' (2020), sec. "Cognitive impairment".</ref> [[melatonină]]<ref name=Taylor2020Sleep> Taylor JP ''et al.'' (2020), sec. "Sleep disturbances" ("Nocturnal sleep disturbances" and "Excessive Daytime Sleepiness" combined on final publication).</ref>|frequency=Aproximativ 0,4% din persoanele cu vârste de peste 65 de ani<ref name= Levin201662> Levin J ''et al.'' (2016), p. 62.</ref>|deaths=}}'''Demența cu corpi Lewy''' ('''DLB''') este un tip de [[demență]] însoțit de modificări ale somnului, comportamentului, [[Cogniție|gândirii]], mișcării și [[Sistem nervos vegetativ|funcțiilor involuntare ale organismului]].<ref name="Taylor2020">{{Citat revistă|dată=February 2020|titlu=New evidence on the management of Lewy body dementia|journal=Lancet Neurol|volum=19|număr=2|pagini=157–69|pmid=31519472|pmc=7017451|doi=10.1016/S1474-4422(19)30153-X}}</ref> Pierderea memoriei nu este întotdeauna un simptom incipient.<ref name="Tousi2017">{{Citat revistă|dată=October 2017|titlu=Diagnosis and management of cognitive and behavioral changes in dementia with Lewy bodies|journal=Curr Treat Options Neurol|volum=19|număr=11|pagină=42|pmid=28990131|doi=10.1007/s11940-017-0478-x}}</ref> Boala se agravează în timp și este de obicei diagnosticată atunci când declinul cognitiv interferează cu funcționarea zilnică normală.<ref name="McKeithConsensus2017">{{Citat revistă|dată=July 2017|titlu=Diagnosis and management of dementia with Lewy bodies: Fourth consensus report of the DLB Consortium|journal=Neurology|volum=89|număr=1|pagini=88–100|pmid=28592453|pmc=5496518|doi=10.1212/WNL.0000000000004058}}</ref><ref name="NINDS2020Book">{{Citat web|url= https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research |publisher= US National Institutes of Health |accessdate= March 18, 2020 |date= January 10, 2020 |titlu=Lewy body dementia: Hope through research|lucrare=National Institute of Neurological Disorders and Stroke|archivedate=April 30, 2021|archiveurl=https://web.archive.org/web/20210430175606/https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research}}</ref> Funcția [[Miocard|inimii]] și fiecare nivel al funcției gastrointestinale, de la mestecat până la [[defecație]], pot fi afectate, [[Constipație|constipația]] fiind unul dintre cele mai des întâlnite simptome.<ref name="Taylor2020" /><ref name="Palma2018">{{Citat revistă|dată=March 2018|titlu=Treatment of autonomic dysfunction in Parkinson disease and other synucleinopathies|journal=Mov Disord|volum=33|număr=3|pagini=372–90|pmid=29508455|pmc=5844369|doi=10.1002/mds.27344}}</ref> De asemenea, se poate manifesta hipotensiunea ortostatică.<ref name="Taylor2020" /> Boala poate afecta comportamentul; schimbările de dispoziție precum [[Depresie (stare)|depresia]] și [[Apatie|apatia]] sunt frecvente.<ref name="McKeithConsensus2017" />



"""
# ---
# ---
# ---
newtext = fix_page(text,
                   "Demența cu corpi Lewy",
                   move_dots=False,
                   infobox=True,
                   lang="ro")
pywikibot.showDiff(text, newtext)

# python3 core8/pwb.py wprefs/wpref_text
