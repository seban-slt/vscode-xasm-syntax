# Tester Instructions – XASM Syntax Extension for VS Code

Thanks for helping test the **XASM syntax highlighting extension**!
This guide explains how to install the extension and what to check.

---

## 1. Install the Extension

1. Download the `.vsix` package from the GitHub release page or from `dist/`.
2. Open VS Code.
3. Go to **Extensions** (Ctrl+Shift+X).
4. Click the **"…"** menu in the Extensions panel → **Install from VSIX…**.
5. Select the `.vsix` file.

---

## 2. Open the Example Project

1. Clone or download this repo.
2. Open the `example/` folder in VS Code.
3. Ensure you see `.vscode/launch.json`, `.vscode/tasks.json`, and `.vscode/settings.json` in the project.

---

## 3. Syntax Highlighting Check

Open the file `examples/hello_world.xsm` (or any `.asx` / `.xsm` file) and check:

- CPU instructions (e.g. `lda`, `sta`) → **light blue, bold**
- Directives (e.g. `org`, `equ`) → **yellow, italic**
- Pseudo instructions (e.g. `mwa`, `mvy`) → **pink**
- Labels at column 0 → **green**
- Hex numbers (`$2000`) → **purple**

Report if colors don’t appear or look odd.

---

## 4. Build & Run Test

- **Build only**: Press `Ctrl+Shift+B`.
  - Should run `xasm` and produce a `.xex` file in the same folder.

- **Run only**:
  - `Ctrl+Shift+P` → *Tasks: Run Task* → `run (emulator)`
  - Emulator (`atari800` on Linux/macOS, Altirra on Windows if `.xex` is associated) should launch with the `.xex`.

- **Build & Run**:
  - `Ctrl+Shift+P` → *Tasks: Run Task* → `build & run`
  - Should assemble and immediately launch emulator.

---

## 5. Launch Configurations

Try the VS Code **Run and Debug** panel:

- Select **Build & Run (detached)** and press **Ctrl+F5** → should build and launch emulator *detached* (no debugger session hanging).
- Select **Run only (detached)** → should launch emulator directly.

---

## 6. macOS Specific

- Confirm that `atari800` runs correctly.
- On Apple Silicon: check that `/opt/homebrew/bin` in PATH is enough for VS Code to find `atari800`.
- If not, let us know the actual install path.

---

## 7. Report Back

Please note:
- OS and version (Linux, macOS Intel, macOS M1/M2, Windows).
- VS Code version.
- Did syntax highlighting look correct?
- Did tasks/launch configs work?
- Any errors in the VS Code terminal?

---

Thank you for testing!
