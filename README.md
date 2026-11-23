# eLabFTW Python API Showcase

[eLabFTW REST API v2 Documentation](https://doc.elabftw.net/api/v2/)

Repository dimostrativa delle funzionalità base delle API v2 di **eLabFTW** in Python, organizzata in ordine cronologico dalla prima verifica di connessione fino alla creazione di un esperimento a partire da un template.

## Prerequisiti

- Python 3.8+
- Librerie Python: `requests`, `python-dotenv`
- File `.env` nella root del progetto con:

```env
ELAB_URL=https://your-elabftw-instance.example.com
ELAB_API_KEY=your_api_key_here
```

## Struttura cronologica

1. **`01_connection_test/test_elab.py`**  
   Verifica la lettura delle variabili d'ambiente dal file `.env` e interroga `GET /api/v2/experiments` per confermare che l'autenticazione funzioni correttamente.
   ```bash
   python 01_connection_test/test_elab.py
   ```

2. **`02_inspect_templates/inspect_templates.py`**  
   Recupera i template disponibili (`GET /api/v2/experiments_templates`), individua il template `IV_K2470`, ne estrae `extra_fields` e `body_html` e salva la struttura in `02_inspect_templates/template_structure.json`.
   ```bash
   python 02_inspect_templates/inspect_templates.py
   ```

3. **`03_prepare_experiment/prepare_experiment.py`**  
   Scarica il template selezionato (`template_id = 6`), popola i campi personalizzati (`extra_fields`) con dati di prova e salva il payload pronto in `03_prepare_experiment/prepared_experiment.json`.
   ```bash
   python 03_prepare_experiment/prepare_experiment.py
   ```

4. **`04_create_experiment/create_experiment.py`**  
   Legge `03_prepare_experiment/prepared_experiment.json` e invia la richiesta `POST /api/v2/experiments` per creare l'esperimento su eLabFTW (include `CREATE_EXPERIMENT` per eseguire eventualmente un dry-run).
   ```bash
   python 04_create_experiment/create_experiment.py
   ```

5. **`05_get_team_id/get_team_id.py`**  
   Interroga `GET /api/v2/users/me` per recuperare il profilo dell'utente autenticato e stampare l'ID e il nome dei team a cui appartiene.
   ```bash
   python 05_get_team_id/get_team_id.py
   ```

6. **`06_create_team_experiment/create_team_experiment.py`**  
   Recupera dinamicamente l'ID del team `"Axial Lab"`, carica `03_prepare_experiment/prepared_experiment.json` e prepara/invia la richiesta `POST /api/v2/experiments` con lettura aperta al team (`canread`) e scrittura riservata al creatore (`canwrite`). Include `CREATE_EXPERIMENT` per eseguire il dry-run.
   ```bash
   python 06_create_team_experiment/create_team_experiment.py
   ```
