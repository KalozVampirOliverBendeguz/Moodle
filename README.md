
# A következő dokumentáció bemutatja, hogyan lehet futtatni és használni a "Moodle_rf" Flask alkalmazást.

## Előfeltételek

- Python 3.6.
- XAMPP (for local database access, version 8.2.12 used)


## Telepítés

- Klónozzuk le a Moodle_rf projektet a GitHubról.
- Navigáljunk a projekt en belül a Moodle-2.-Beadando mappába a terminálban.
- Következő parancs futtatása:
```bash
pip install -r requirements.txt
```
- Indítsuk el a XAMPP-ot, majd bizonyosodjunk meg róla hogy az Apache és a MySQL is fut.
- Nyissuk meg a phpMyAdmin-t.
- Hozzunk létre egy adatbázist "moodle" névvel "utf8mb4_general_ci" 
- Majd importáljuk be az SQL fájlt ami megvan adva a "moodle" adatbázisba

## Futtatás
```bash
cd Moodle-2.-Beadando
```
```bash
python runserver.py
```
- Ezután a böngészőben a localhost:5555 címen tudjuk elérni az alkalmazást
- Belépéshez a "Tibor22" felhasználónevet a "password" jelszó kombinációt, vagy a "Geza32" felhasználónevet a "password" jelszó kombinációt használja



