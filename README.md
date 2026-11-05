# ScryX

ScryX is a desktop viewer and render-QC tool for CG/VFX image sequences. The first release is planned to support OpenEXR, PNG and TIFF, AOV and pixel inspection, and technical checks with JSON and HTML reports.

> **Status:** exploratory prototype. The repository contains EXR and Qt/QML spikes and a Python package skeleton.

**Version**: 0.1.0.dev0

---
## Project structure

```text
.
├── README.md
├── LICENSE.md
├── pyproject.toml            # Project and dependency configuration
├── .gitignore
├── dataset/                 # Test sequences and corrupted samples
├── docs/                   # Requirements, research, and development notes
├── spikes/                 # Experimental scripts and GUI prototypes
└── src/                    # Application source and modules
```

- [Project documentation and knowledge base](docs/README.md)
- [Working requirements baseline](docs/requirements/REQUIREMENTS_BASELINE.md)
- [Historical project passport](docs/thesis_passport.md)
- [Development journal](docs/project_journal.md)
- [EXR metadata spike](spikes/01_read_exr.py)
- [Qt/QML testing](spikes/gui_test/main.py)

---
## How to start

### 1. Enter the repository

```bash
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
python -m pip install -e ".[dev,gui,spikes]"
```

This installs the current checkout from `pyproject.toml`. A clean installation of the candidate stack and support for the target platforms are still being verified.

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
