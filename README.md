# 26. csapat - Moodle
Készítették:
- Tóth Olivér Bendegúz (GDKGBF)
- Horváth Kristóf Ervin (FI0P26)
- Prágai János Márk (FZZPH5)

## Környezet előkészítése:
### Telepítsd a Python programozási nyelvet a gépedre, ha még nincs telepítve. A Python letölthető a hivatalos weboldalról: https://www.python.org/downloads/
### Projekt klónozása: Klónozd le a projektet a GitHubról
### Függőségek telepítése:
-Telepítsd a projekt függőségeit a következő paranccsal a terminálban vagy parancssorban:
```bash
pip install -r requirements.txt
```
### Virtuális környezet létrehozása (opcionális, de ajánlott):
-Hozz létre egy virtuális környezetet a projekt mappájában a következő paranccsal:
```bash
python -m venv venv
```
### Aktiváld a virtuális környezetet:
-Windows:
```bash
venv\Scripts\activate
```
-Linux/macOS:
```bash
source venv/bin/activate
```
### Adatbázis konfiguráció:
-Hozz létre egy "moodle" nevű adatbázist, ahova a gyökérkönyvtárban megadott moodle.sql-t importáld be.
### Szerver indítása:
-Indítsd el a Flask fejlesztői szervert a következő paranccsal:
```bash
python runserver.py
```
### Hozzáférés a webes felülethez:
-Nyisd meg a böngésződet, és látogass el a következő címre: http://localhost:5555
