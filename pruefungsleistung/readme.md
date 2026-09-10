# Sales Order Data Warehouse

ELT-Pipeline und Data Warehouse basierend auf PostgreSQL, Docker und Python. Das System setzt eine Medallion-Architektur um (Staging, Core 3NF, Data Mart Sternschema).

## Datenquelle

Die Pipeline verarbeitet den Superstore-Sales-Datensatz. Die Quelldatei liegt bereits im Repository unter `raw_data/sales_order_item.csv`.

## Voraussetzungen

- Docker und Docker Compose
- Python 3.12+

## Installation und Ausführung

1. `.env`-Datei im Hauptverzeichnis anlegen und Zugangsdaten eintragen.
2. Docker-Container starten:
   ```bash
   docker compose up -d
   ```
3. Python-Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. Pipeline ausführen:
   ```bash
   python main.py
   ```

## Umgebungsvariablen (`.env`)

Folgende Schlüssel müssen in der `.env` definiert werden:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `PGADMIN_DEFAULT_EMAIL`
- `PGADMIN_DEFAULT_PASSWORD`

## Repository-Struktur

- `main.py`: Orchestrierung der Pipeline
- `docker-compose.yml`: Konfiguration PostgreSQL 18 & pgAdmin 4
- `.env`: Umgebungsvariablen (lokal, nicht im Repository)
- `.gitignore`: Steuerung der von Git zu ignorierenden Dateien und Pfade
- `requirements.txt`: Python-Bibliotheken (`pandas`, `SQLAlchemy`, `psycopg2-binary`, `python-dotenv`)
- `raw_data/`: Dateispeicher für CSV-Rohdaten (`sales_order_item.csv`)
- `data/`: Dateispeicher für verarbeitete Exporte und temporäre Dateiablagen
- `archive/`: Enthält abgelöste Entwicklungsstände und archivierte Skripte früherer Iterationen
- `init-db/`: SQL-Skripte für Schemata- und Tabellenerstellung
- `scripts/lib_py/`: Python-Skripte (`load_staging.py`, `normalisierung.py`)
- `scripts/sql/`: SQL-Transformationsskripte (`truncate_core.sql`, `truncate_staging.sql`, `load_core-mart.sql`, `mart_kpi-update.sql`)
- `doc/`: Visuelle Abbildungen der Prozesse und Architektur sowie SQL-Validierungsskripte (`sql_validierung.txt`)

## Schnittstellen und Zugangsdaten

- **PostgreSQL:** `127.0.0.1:5432` (Benutzer: Wert aus `POSTGRES_USER` in `.env`, Datenbank: Wert aus `POSTGRES_DB` in `.env`)
- **pgAdmin Web-Interface:** `http://localhost:8080` (E-Mail: Wert aus `PGADMIN_DEFAULT_EMAIL` in `.env`, Passwort: Wert aus `PGADMIN_DEFAULT_PASSWORD` in `.env`)

## pgAdmin Server einrichten

1. Web-Interface unter `http://localhost:8080` öffnen und einloggen.
2. **"Add New Server"** auswählen.
3. Reiter **"Connection"** ausfüllen:
   - **Host name / address:** `postgres`
   - **Port:** `5432`
   - **Maintenance database:** Wert aus `POSTGRES_DB` in `.env`
   - **Username:** Wert aus `POSTGRES_USER` in `.env`
   - **Password:** Wert aus `POSTGRES_PASSWORD` in `.env`

## Quellen und Inspirationen

- **Superstore Sales Datensatz:** Anonymisierter Beispieldatensatz für E-Commerce-Analysen und Data-Warehouse-Prototypen.
- **Medallion-Architektur:** Schichtenmodell (Bronze, Silber, Gold) zur strukturierten Datenveredelung nach Databricks.
- **Data-Warehouse-Architekturen (Inmon vs. Kimball):**
  - *Bill Inmon:* Enterprise-Data-Warehouse-Ansatz mit relationaler 3NF im Core-Layer als *Single Source of Truth*.
  - *Ralph Kimball:* Dimensionales Modellieren (Sternschema) im Gold-Layer für performante OLAP-Analysen.
- **C4-Modell:** Standardisiertes Framework zur hierarchischen Visualisierung von Software- und Datenarchitekturen nach Simon Brown.