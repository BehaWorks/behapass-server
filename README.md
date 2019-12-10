# Logger
Základný logger na logovanie pohybu vo VR spolu so stavom ovládaču napísaný vo [Flask-u](https://palletsprojects.com/p/flask/) s využitím [flask_restplus](https://flask-restplus.readthedocs.io/en/stable/).

Ako úložisko slúži [MongoDb](https://www.mongodb.com/).

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

V kofigurácii musí byť URL nastavená na adresu stroja (```172.*```) na ktorom beží Docker z pohľadu kontajnera, ```localhost``` dá len adresu kontajnera. Adresa sa dá zistiť príkazom ```hostname -I``` v kontajneri. 

Pri spúšťaní treba prepojiť lokálny súborový systém a porty s kontajnerom: 
```
docker run -p 5000:5000 -v <C:/cesta/k/repozitaru>:/logger --name behapass-server behapass-server
```
```<C:/cesta/k/repozitaru>``` treba nahradiť skutočnou cestou, mala by sa končiť ```/logger```. Dvojbodka tam musí byť.
Pri vytváraní konfigurácie v Idei treba dať do _Bind ports_ to čo je v prepínači ```-p``` a do Bind mounts to čo je vo ```-v```. 
