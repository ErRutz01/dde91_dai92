Sales Order Data Warehouse

ETL-Pipeline und Data Warehouse basierend auf PostgreSQL, Docker und Python. Das System setzt eine Medallion-Architektur um (Staging, Core 3NF, Data Mart Sternschema).

Voraussetzungen:
- Docker und Docker Compose
- Python 3.12+

Installation und Ausführung:
1. Docker installieren
2. Docker-Container starten:
   docker compose up -d
3. Datenbank im Container erstellen:
   docker exec -it pruefungsleistung-postgres-1 createdb -U EricRutz12 sales_order_item
4. Python-Abhängigkeiten installieren:
   pip install -r requirements.txt
5. ETL-Pipeline ausführen:
   python main.py

Repository-Struktur:
- main.py: Orchestrierung der Pipeline
- docker-compose.yml: Konfiguration PostgreSQL 18 & pgAdmin 4
- .env: Umgebungsvariablen
- requirements.txt: Python-Bibliotheken (pandas, SQLAlchemy, psycopg2-binary)
- raw_data/: Dateispeicher für CSV-Rohdaten (sales_order_item.csv)
- data/: Dateispeicher für verarbeitete Daten
- init-db/: SQL Skripte für Schemata und Tabellenerstellung
- scripts/lib_py/: Python-ETL-Skripte (load_staging.py, normalisierung.py, load_data_mart.py)

Schnittstellen und Zugangsdaten:
- PostgreSQL: 127.0.0.1:5432 (Benutzer: EricRutz12, Datenbank: sales_order_item)
- pgAdmin Web-Interface: http://localhost:8080 (E-Mail: ericrutz780@outlook.de, Passwort: 4hFd98Tm!120101)