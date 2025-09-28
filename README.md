# Get Shot at by a Nine Year Old Similator

[![Build & Release](https://github.com/TheCrazy8/Get-Shot-at-by-a-Nine-Year-Old-Similator/actions/workflows/build-release.yml/badge.svg)](../../actions/workflows/build-release.yml)

yeah thats it :3

## Releases

Download the latest Windows standalone executable from the **Releases** page. Each time a tag starting with `v` (e.g. `v1.0.0`) is pushed, GitHub Actions will:

1. Install dependencies (pygame & pyinstaller)
2. Run the PyInstaller build script (`exe machine.py`)
3. Upload the versioned `.exe` as an artifact
4. Publish / update a GitHub Release attaching the executable

### Creating a new release

From local machine (example for version 1.2.0):

```bash
git tag v1.2.0
git push origin v1.2.0
```

Within a few minutes the release will appear with `RiftOfMemories-v1.2.0.exe`.

### Non-Windows users

Use the Itch.io version (Linux / macOS users can also run from source: install Python 3.11+, `pip install -r requirements.txt`, then run `python "Rift of Memories and Regrets.py"`).

---

**NOTE:** USE THE ITCH.IO VERSION (IF NO WINDOWS SYSTEM) OR WINDOWS VERSION, AS WINDOWS VERSION IS THE MAIN VERSION
