Sales Order Data Warehouse

ELT-Pipeline und Data Warehouse basierend auf PostgreSQL, Docker und Python. Das System setzt eine Medallion-Architektur um (Staging, Core 3NF, Data Mart Sternschema).

Datenquelle:
Die Pipeline verarbeitet den Superstore-Sales-Datensatz. Die Quelldatei liegt bereits im Repository unter raw_data/sales_order_item.csv.

Voraussetzungen:
- Docker und Docker Compose
- Python 3.12+

Installation und Ausführung:
1. Docker installieren
2. .env-Datei anlegen (Werte aus .env.example übernehmen)
3. Docker-Container starten:
   docker compose up -d
4. Python-Abhängigkeiten installieren:
   pip install -r requirements.txt
5. Pipeline ausführen:
   python main.py

Umgebungsvariablen (.env):
Folgende Schlüssel müssen in der .env definiert werden (siehe .env.example):
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_HOST
- POSTGRES_PORT
- PGADMIN_DEFAULT_EMAIL
- PGADMIN_DEFAULT_PASSWORD

Repository-Struktur:
- main.py: Orchestrierung der Pipeline
- docker-compose.yml: Konfiguration PostgreSQL 18 & pgAdmin 4
- .env: Umgebungsvariablen
- .env.example: Vorlage für Umgebungsvariablen
- requirements.txt: Python-Bibliotheken (pandas, SQLAlchemy, psycopg2-binary, python-dotenv)
- raw_data/: Dateispeicher für CSV-Rohdaten (sales_order_item.csv)
- init-db/: SQL Skripte für Schemata und Tabellenerstellung
- scripts/lib_py/: Python-Skripte (load_staging.py, normalisierung.py)
- scripts/sql/: SQL-Transformationsskripte (truncate_core.sql, truncate_staging.sql, load_core-mart.sql, mart_kpi-update.sql)
- doc/: Visuelle Abbildungen der Prozesse und Architektur sowie SQL-Validierungsskripte (sql_validierung.txt)

Schnittstellen und Zugangsdaten:
- PostgreSQL: 127.0.0.1:5432 (Benutzer: Wert aus POSTGRES_USER in .env, Datenbank: Wert aus POSTGRES_DB in .env)
- pgAdmin Web-Interface: http://localhost:8080 (E-Mail: Wert aus PGADMIN_DEFAULT_EMAIL in .env, Passwort: Wert aus PGADMIN_DEFAULT_PASSWORD in .env)

pgAdmin Server einrichten:
1. Web-Interface unter http://localhost:8080 öffnen und einloggen
2. "Add New Server" auswählen
3. Reiter "Connection" ausfüllen:
   - Host name / address: postgres
   - Port: 5432
   - Maintenance database: Wert aus POSTGRES_DB in .env
   - Username: Wert aus POSTGRES_USER in .env
   - Password: Wert aus POSTGRES_PASSWORD in .env