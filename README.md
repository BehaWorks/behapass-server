# BehaPass - server
Tento repozitár obsahuje serverovú časť aplikácie BehaPass. 
Ide o najdokonalejší spôsob prihlasovania, aký tu kedy bol a zároveň jediný, ktorý budete odteraz potrebovať.

_Vitajte na začiatku novej éry._

Jeho základ tvorí [Flask](https://palletsprojects.com/p/flask/) aplikácia s využitím [flask_restplus](https://flask-restplus.readthedocs.io/en/stable/).

Ako primárne úložisko slúži [MongoDb](https://www.mongodb.com/) a ako dočasné úložisko slúži [Redis](https://redis.io/).

Vyžaduje sa Python 3 alebo novší. Na nainštalovanie všetkých závislostí z requirements.txt odporúčame použiť nástroj `pip`.

## Spustenie  
1. Skontrolovať závislosti, najmä Python 3 a pip, prípadne si vytvoriť a aktivovať Python virtual enviroment.  
2. Pullnúť tento repozitár.  
3. Inštaláciu vykonať prikazom: `pip install -e .` z koreňového priečinku tohto repozitára.  
4. Nastaviť konfiguráciu v súbore `server/config/config.py` podľa predlohy `server/config/default.py` najmä pripojenie k MongoDB.  

Primárnym spúšťačom je súbor `logger.py`, no do produkcie odporúčame použiť niektorý z produkčných Python serverov, napríklad [Gunicorn](https://gunicorn.org/). 

Dokumentácia je k dispozícií na adrese `<URL_PREFIX>/documentation`
Štruktúra údajov v API je inšpirovaná údajmi z [OpenVR](https://github.com/ValveSoftware/openvr/wiki/IVRCompositor::WaitGetPoses).

## Vizualizácie
Na adrese `/visualisations` je možné zobraziť vizualizácie nalogovaných dát. Vizualizácie sú rozdelené podľa mena používateľa. Každý používateľ má niekoľko sessions. Jedna session reprezenuje jeden pohyb.

Na opätovné spustenie animácie grafu treba obnoviť stránku.

## Spúšťanie v Dockeri
Treba mať nainštalovaný [Docker](https://docker.com). Na Windowse je to komplikovanejšie, s W10 Home Edition to nefunguje, ale W10 Education je pre [študentov FIIT zadarmo](http://msdnaa.fiit.stuba.sk/). 

V konfigurácii musí byť URL nastavená na adresu stroja (```172.*```) na ktorom beží Docker z pohľadu kontajnera, ```localhost``` dá len adresu kontajnera. Adresa sa dá zistiť príkazom ```hostname -I``` v kontajneri. 

Pri spúšťaní treba prepojiť lokálny súborový systém a porty s kontajnerom: 
```
docker run -p 8000:8000 -v <C:/cesta/k/repozitaru>:/logger --name behapass-server behapass-server
```
```<C:/cesta/k/repozitaru>``` treba nahradiť skutočnou cestou, mala by sa končiť ```/logger```. Dvojbodka tam musí byť.
Pri vytváraní konfigurácie v Idei treba dať do _Bind ports_ to čo je v prepínači ```-p``` a do Bind mounts to čo je vo ```-v```. 

### Parametre docker imageu
[Premenné prostredia](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) (pri spustení):   
- ```port``` - port na ktorom má počúvať aplikácia v docker containeri. Default: ```8000```. Tento port treba otvoriť pri spúšťaní kontajneru. Príklad na spustenie na inom porte (port 1234):
```
docker run -p 1234:1234 -v <C:/cesta/k/repozitaru>:/logger --name behapass-server --env "port"="1234" behapass-server
```
 - ```db_host``` a ```db_port``` - adresa a port, na ktorých počúva databáza. Default: ```172.17.0.1``` a ```27017```
 - ```redis_host``` a ```redis_port``` - adresa a port Redis-u, do ktorého sa ukladajú pohyby počas registrácie používateľa. Default: ```172.17.0.1``` a ```6379```
 - ```registration_expire``` - doba v sekundách, po ktorej sa odstránia pohyby z nedokončených registrácií. Automaticky sa odstránia iba pohyby, dáta používateľa ostávajú v perzistentnom úložisku. Default: ```600```


Premenná pri builde: ```copy``` - čo všetko sa má skopírovať do imageu. Pri vývoji odporúčame použiť možnosť ```requirements.txt``` a prepojiť lokálne súbory cez ```-v```. V produkcii netreba zadávať nič a defaultne sa nakopíruje všetko. Iné hodnoty spravia chyby. 