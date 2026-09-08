# Tester Instructions - XASM Syntax Extension for VS Code

Thanks for helping test the **XASM syntax highlighting extension**. This guide explains how to install the extension and what to check.

## 1. Install the Extension

1. Download the `.vsix` package from the GitHub release page or from `dist/`.
2. Open VS Code.
3. Go to **Extensions** (`Ctrl+Shift+X`).
4. Open the `...` menu in the Extensions panel and choose **Install from VSIX...**.
5. Select the `.vsix` file.

## 2. Open the Example Project

1. Clone or download this repository.
2. Open the `example/` folder in VS Code.
3. Verify that `.vscode/launch.json`, `.vscode/tasks.json`, and `.vscode/settings.json` are present.

## 3. Syntax Highlighting Check

Open `example/example.xsm` (or any `.asx` / `.xsm` file) and check the highlighting.

The example workspace settings use the following colors:

- CPU instructions (for example `lda`, `sta`) - light blue, bold
- Directives (for example `org`, `equ`) - yellow, italic
- XASM pseudo-instructions (for example `mwa`, `mvy`) - pink
- Labels at column 0 - green
- Hex numbers (`$2000`) - purple

These colors come from `example/.vscode/settings.json`; the extension itself does not force a color theme.

## 4. Snippet Check

Open an XASM source file and type:

```text
stereo
```

Select **Detect Stereo Routine** from completion suggestions (or trigger snippet completion manually). The complete stereo-detection routine should be inserted.

Use `Tab` to move through editable placeholders. Renaming `?loop` or `?mono` should update the corresponding mirrored occurrence automatically.

## 5. Build & Run Test

### Build only

Press `Ctrl+Shift+B`.

VS Code should run `xasm` and produce a `.xex` file next to the active source file.

### Run only

Use:

**Command Palette -> Tasks: Run Task -> run (emulator)**

Platform behavior:

- **Linux:** runs `atari800 -run ...` directly.
- **macOS:** opens the `.xex` using the application associated with `.xex` files and waits for the application to close.
- **Windows:** opens the `.xex` using the application associated with `.xex` files (for example Altirra) and waits for it to close.

### Build & Run

Use:

**Command Palette -> Tasks: Run Task -> build & run**

The source should be assembled first and the resulting `.xex` launched afterwards.

## 6. Launch Configurations

Open the VS Code **Run and Debug** panel.

- **Build & Run (detached)** - runs the compile task first, then launches the emulator without keeping a VS Code debug session attached.
- **Run only (detached)** - launches the existing `.xex` without compiling it first.

Please test both configurations.

## 7. macOS Specific

The example configuration uses the macOS `open` command rather than hard-coding an emulator. Please verify that:

- `.xex` is associated with the intended Atari emulator;
- `run (emulator)` opens the correct application;
- both detached launch configurations work with paths containing spaces;
- Intel and Apple Silicon Macs behave consistently, if available for testing.

## 8. Report Back

Please include:

- OS and version (Linux, macOS Intel/Apple Silicon, Windows);
- VS Code version;
- whether syntax highlighting works correctly;
- whether snippet insertion and placeholder mirroring work;
- whether build/run tasks work;
- whether detached launch configurations work;
- relevant errors from the VS Code terminal or Output panel.

Thank you for testing!
