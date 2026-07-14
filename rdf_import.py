import os
import rdflib
import requests
import urllib3
from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.datatypes import Item
# NEU: Das Such-Werkzeug importieren
from wikibaseintegrator.wbi_helpers import search_entities 

# --- SSL-Patch für lokales HTTPS ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
old_request = requests.Session.request
def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)
requests.Session.request = new_request
# -----------------------------------

# 1. Wikibase Konfiguration
wbi_config['MEDIAWIKI_API_URL'] = 'https://localhost/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://localhost:8989/sparql'
wbi_config['WIKIBASE_URL'] = 'https://localhost'

P_HAS_THEME = 'P1'

login = wbi_login.Login(
    user=os.environ['WIKIBASE_USER'],
    password=os.environ['WIKIBASE_PASSWORD'],
)
wbi = WikibaseIntegrator(login=login)

item_cache = {}

def get_or_create_item(name):
    """Sucht erst im Cache, dann in der Wikibase und legt erst als letztes neu an."""
    
    # 1. Ist es schon im Kurzzeitgedächtnis (Cache) dieses Skripts?
    if name in item_cache:
        return item_cache[name]
    
    # 2. NEU: Wir fragen die Wikibase, ob sie das Item schon kennt (aus dem CSV-Versuch!)
    try:
        results = search_entities(search_string=name, language='en')
        if results:
            existing_id = results[0] # Wir nehmen die ID des ersten Treffers
            item_cache[name] = existing_id
            print(f"Wiederverwendet (aus CSV-Versuch): {name} ({existing_id})")
            return existing_id
    except Exception as e:
        pass # Falls die Suche fehlschlägt, machen wir einfach mit Punkt 3 weiter
    
    # 3. Wenn es wirklich nirgends existiert, legen wir es neu an
    item = wbi.item.new()
    item.labels.set(language='en', value=name)
    item = item.write()
    
    item_cache[name] = item.id
    print(f"Neu angelegt: {name} (ID: {item.id})")
    return item.id

print("Lese RDF-Datei ein...")
g = rdflib.Graph()
g.parse("knowledge_graph.rdf")

ns1 = rdflib.Namespace("http://example.org/")

# Wir gruppieren die Themen nach Werk, um Wikibase-Speichervorgänge zu sparen
works_dict = {}

for subject, predicate, obj in g.triples((None, ns1.hasTheme, None)):
    work_name = str(subject).split("/")[-1].replace("_", " ")
    theme_name = str(obj).split("/")[-1].replace("_", " ")
    
    if work_name not in works_dict:
        works_dict[work_name] = []
    works_dict[work_name].append(theme_name)

print("Starte den Import in Wikibase...")

# 3. Daten in Wikibase pushen
for work, themes in works_dict.items():
    work_qid = get_or_create_item(work)
    work_item = wbi.item.get(entity_id=work_qid)
    
    for theme in themes:
        theme_qid = get_or_create_item(theme)
        
        # claim erstellen: "has theme -> [Themen-ID]"
        claim = Item(value=theme_qid, prop_nr=P_HAS_THEME)
        work_item.claims.add(claim)
    
    # Das Werk mit allen angehängten Themen speichern
    work_item.write()
    print(f"> Erfolgreich verknüpft: '{work}' mit {len(themes)} Themen.")

print("RDF-Import komplett abgeschlossen!")