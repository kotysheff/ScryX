# ScryX

ScryX is a desktop viewer and render-QC tool for CG/VFX image sequences. It is designed for OpenEXR, PNG, JPEG, and TIFF, with AOV inspection and detection of missing frames, corrupted files, invalid pixel values, and alpha issues.

> **Status:** exploratory prototype and development MVP. The application core and complete GUI are not finished yet.

---
## Project structure

```text
.
├── README.md
├── LICENSE.md
├── requirements.txt
├── .gitignore
├── dataset/                 # Test sequences and corrupted samples
├── docs/                   # Requirements, research, and development notes
├── spikes/                 # Experimental scripts and GUI prototypes
└── src/                    # Application source and modules
```

- [Project documentation and knowledge base](docs/README.md)
- [Project specification](docs/thesis_passport.md)
- [Development journal](docs/project_journal.md)
- [EXR metadata spike](spikes/01_read_exr.py)
- [Qt/QML testing](spikes/gui_test/main.py)
- [GitHub repository](https://github.com/kotysheff/ScryX)

---
## How to start

### 1. Clone and enter the repository

```bash
git clone https://github.com/kotysheff/ScryX.git
cd ScryX
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Inspect an EXR file

```bash
python spikes/01_read_exr.py dataset/full_sequence/010000.exr
```

### 5. Run the GUI QT/QML test prototype

```bash
python spikes/gui_test/main.py
```

---
## License

ScryX uses the [MIT License](LICENSE.md).
