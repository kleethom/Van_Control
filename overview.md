van_control/
├── main.py # Einstiegspunkt
├── config/
│ └── settings.yaml # Konfiguration (Sensoren, Intervalle, Cloud)
├── core/
│ ├── app.py # Hauptklasse, verbindet Sensoren, GUI, Cloud, Storage
│ ├── state.py # SystemState (Single Source of Truth)
│ └── scheduler.py # Zeitgesteuerte Tasks für Sensoren und Cloud
├── sensors/
│ ├── Test temperatur_dummy.py
│ ├── base_sensor.py
│ ├── victron_battery.py # Victron SmartShunt / Dummy
│ ├── temperature_dummy.py
│ ├── water_level_dummy.py # Beispiel für Wasserstandssensor
│ └── ...
├── storage/
│ ├── base_storage.py # Interface / Basis-Klasse für Speicherlösungen
│ └── sqlite_storage.py # SQLite-Datenbank für Historie
├── cloud/
│ ├── base_client.py
│ └── mqtt_dummy.py # Platzhalter für Cloud-Sync
├── gui/
│ ├── app.py # Kivy App Klasse
│ ├── screens/
│ │ ├── main_screen.py
│ │ ├── battery_screen.py
│ │ ├── battery_history_screen.py
│ │ ├── water_screen.py
│ │ ├── temperature_screen.py
│ │ └── settings_screen.py
│ └── van.kv # Layout Datei (KV-Sprache)
└── utils/
└── logger.py # Logging Utilities