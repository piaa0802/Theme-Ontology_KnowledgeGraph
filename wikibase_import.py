import csv
from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.datatypes import Item, String

# 1. Konfiguration für Wikibase Cloud
wbi_config['MEDIAWIKI_API_URL'] = 'https://themeontology.wikibase.cloud/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'https://query.themeontology.wikibase.cloud/sparql'
wbi_config['WIKIBASE_URL'] = 'https://themeontology.wikibase.cloud'

# Deine IDs! (Stelle sicher, dass P1 und P2 stimmen)
P_HAS_THEME = 'P1'
P_THEME_TYPE = 'P2'

# 2. Login
login = wbi_login.Login(user='pgrafe', password='Wik.ibpilb1')
wbi = WikibaseIntegrator(login=login)

# Ein kleines Dictionary als Zwischenspeicher, um doppelte Anlagen zu vermeiden
item_cache = {}

def get_or_create_item(name):
    """Prüft ob ein Item existiert, ansonsten wird es neu in Wikibase angelegt."""
    if name in item_cache:
        return item_cache[name]
    
    # Neues leeres Item erstellen
    item = wbi.item.new()
    item.labels.set(language='en', value=name)
    # Item in die Datenbank schreiben
    item = item.write()
    
    item_cache[name] = item.id
    print(f"Neu angelegt: {name} (ID: {item.id})")
    return item.id

print("Starte Import...")

# 3. CSV einlesen und Daten pushen
with open("output.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Erst die Werte sicher holen (ohne direkt .strip() aufzurufen)
        work_raw = row.get("Work")
        theme_raw = row.get("Theme")
        type_raw = row.get("Type")

        # Wenn die Zeile komplett leer ist -> überspringen
        if not work_raw or not theme_raw:
            continue

        # Jetzt gefahrlos die Leerzeichen entfernen
        work = work_raw.strip()
        theme = theme_raw.strip()
        theme_type = type_raw.strip() if type_raw else ""

        # Items holen oder neu anlegen (gibt z.B. Q1, Q2 zurück)
        work_qid = get_or_create_item(work)
        theme_qid = get_or_create_item(theme)

        # Das Werk-Item zum Bearbeiten abrufen
        work_item = wbi.item.get(entity_id=work_qid)
        
        # Die eigentliche Verbindung erstellen: "has theme -> [Themen-ID]"
        claim = Item(value=theme_qid, prop_nr=P_HAS_THEME)
        
        # Den Qualifikator anfügen: "theme type -> major/minor"
        qualifier = String(value=theme_type, prop_nr=P_THEME_TYPE)
        claim.qualifiers.add(qualifier)

        # Die Verbindung dem Werk hinzufügen und speichern
        work_item.claims.add(claim)
        work_item.write()
        
        print(f"Verknüpft: {work} -> {theme} (Typ: {theme_type})")

print("Import abgeschlossen!")