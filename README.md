# Logger
Základný logger na logovanie pohybu vo VR spolu so stavom ovládaču napísaný vo [Flask-u](https://palletsprojects.com/p/flask/)s využitím [flask_restplus](https://flask-restplus.readthedocs.io/en/stable/).

Ako úložisko slúži [MongoDb](https://www.mongodb.com/)

Inštaláciu je možné vykonať prikazom: `pip install -e .`

Dokumentácia je k dispozícií na adrese `<URL_PREFIX>/documentation`
Štruktúra údajov v API je inšpirovaná údajmi z [OpenVR](https://github.com/ValveSoftware/openvr/wiki/IVRCompositor::WaitGetPoses).

Konfigurácia je v súbore `config/config.py` podľa predlohy `config-default.py`

Vstupným bodom je súbor `logger.py`, no do produkcie odporúčame použiť niektorý z produkčných Python serverov, napríklad [Gunicorn](https://gunicorn.org/) 