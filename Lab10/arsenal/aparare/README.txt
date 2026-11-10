Laboratorul 10 – Funcții și excepții

Din rădăcina depozitului:
python3 -m arsenal.aparare.parse_auth arsenal/aparare/start/auth.log
python3 -m arsenal.aparare.detector arsenal/aparare/start/auth.log
python3 -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2
python3 -m arsenal.aparare.detector arsenal/aparare/start/auth.log --json
python3 -m pytest -q arsenal/aparare/test_detector.py
