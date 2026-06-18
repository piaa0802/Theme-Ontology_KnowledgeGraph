import os
import csv

# CSV-Datei erstellen (w = write = überschreiben/neu erstellen)
csv_file = open("output.csv", "w", newline="", encoding="utf-8")
# CSV-Writer-Objekt erstellen (damit wir Zeilen schreiben können)
writer = csv.writer(csv_file)

# Spaltenüberschriften 
writer.writerow(["Work", "Theme", "Type"])

# Ordner in dem die txt. Dateien liegen 
folder = "literature"

# geht durch alle Dateien im Ordner 
for filename in os.listdir(folder):
    
    if filename.endswith(".txt"):
        
        filepath = os.path.join(folder, filename)
        
        print("Verarbeite Datei:", filename)
        
        # Datei öffnen und einlesen
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines() # gesamte Datei als Liste von Zeilen 
            
            # Variablen speichern den aktuellen Zustand
            current_title = None
            current_theme_type = None  # major / minor / choice
            
            # jede Zeile durchgehen 
            for i in range(len(lines)):
                
                line = lines[i].strip() # Leerzeichen & Zeilenumbrüche entfernen
                
                # Titel erkennen
                if line == ":: Title":
                    current_title = lines[i+1].strip() # Der eigentliche Titel steht in der nächsten Zeile
                
                # Theme-Kategorien erkennen
                elif line == ":: Major Themes":
                    current_theme_type = "major" 
                
                elif line == ":: Minor Themes":
                    current_theme_type = "minor"
                
                elif line == ":: Choice Themes":
                    current_theme_type = "choice"
                
                # einzelne Themes erkennen 
                elif "[" in line and current_title and current_theme_type:
    
                    # nur den Theme-Namen nehmen 
                    theme = line.split("[")[0].strip()
    
                    # unnötiges rausfiltern
                    if theme.startswith("Note:"):
                        continue
    
                    #print(f"{current_title} → {theme} ({current_theme_type})")
                    # in CSV schreiben 
                    writer.writerow([current_title, theme, current_theme_type]) 
# CSv schließen                 
csv_file.close()