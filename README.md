# ase_charging_station_part_2

## Steps to run

### 1. Important note:
The file *firebase.json* is required for this application to run. However, it is not included in this GitHub repository because Firebase requires a Google account linked to a phone number, and this file contains a key associated with that account.

We will provide the file via email.

Please create a folder named *secret* at the root level of the project and place the file inside.
```bash
# Linux instructions:
# cd to this repository
mkdir secret
mv <path-to-the-downloaded-file> secret/
```

### 2. Create a virtual environment and activate it:
```bash
python -m venv ase-env
source ./ase-env/bin/activate  # On Linux
.\ase-env\Scripts\activate # on Windows
```

### 3. Install dependencies and setup project paths:
```bash
pip install -e .
```

### 4. Run tests:
```bash
pytest
```

### 5. Calculate Test Coverate
```bash
coverage run -m pytest
coverage report
```

### 6. Start the Flask app:
```bash
python main.py
```

### 7. Open webapp in browser:
`http://127.0.0.1:5000`
