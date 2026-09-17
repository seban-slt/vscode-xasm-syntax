# XASM VS Code Extension

This repository contains a Visual Studio Code extension for **XASM assembler** source files (`.asx`, `.xsm`). It provides syntax highlighting, XASM snippets, project initialization, and a cross-platform build/run setup.

## Features

- Highlighting for **6502 mnemonics**
- Highlighting for **XASM directives** (`aln`, `org`, `equ`, `opt`, ...)
- Highlighting for **XASM pseudo-instructions** (`mwa`, `mvy`, `mwx`, ...)
- Detection of labels at column 0, including XASM local labels such as `?loop`
- Comments starting with `;`
- Hexadecimal numbers (`$1234`)
- Snippets for reusable XASM routines
- Human-friendly snippet sources: snippets are written as normal `.xsm` files and converted to the VS Code JSON format automatically
- **XASM: Initialize Project** command for creating ready-to-use `.vscode` build/run configuration

Supported file types:

- `.asx`
- `.xsm`

## Quick Start

After installing the extension:

1. Open your XASM project directory in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Run **XASM: Initialize Project**.
4. The extension creates the missing project files:

```text
.vscode/
├── tasks.json
├── launch.json
└── settings.json
```

Existing files are **never overwritten**. If any of these files already exist, they are left unchanged.

After initialization:

- `Ctrl+Shift+B` runs the default `compile (xasm)` task.
- **Tasks: Run Task -> build & run** compiles the active source and starts the emulator.
- **Build & Run (detached)** and **Run only (detached)** are available from the Run and Debug panel.

Platform behavior:

- **Linux:** uses `atari800`.
- **macOS:** opens `.xex` using the application associated with the file type.
- **Windows:** opens `.xex` using the application associated with the file type (for example Altirra).

The generated `settings.json` contains the example XASM token colors used by this repository. The extension itself does not force a color theme.

## Repository Structure

```text
extension/
├── package.json
├── extension.js                # Active extension code (project initializer)
├── language-configuration.json
├── syntaxes/
│   └── xasm.tmLanguage.json
├── snippets-src/               # Human-edited XASM snippet sources
│   └── detect_stereo.xsm
├── snippets/
│   └── xasm.json               # Generated; do not edit directly
├── templates/
│   └── project/
│       └── .vscode/            # Templates used by XASM: Initialize Project
├── tools/
│   └── build_snippets.py
└── images/

example/
├── .vscode/
│   ├── launch.json
│   ├── tasks.json
│   └── settings.json
└── example.xsm
```

The `example/` directory contains the same ready-to-use VS Code configuration that is installed by **XASM: Initialize Project**.

## Snippet Sources

Do **not** edit `extension/snippets/xasm.json` manually. It is generated from the `.xsm` files in `extension/snippets-src/`.

A snippet source is ordinary XASM with a small metadata header:

```asm
; @name Wait for VBL
; @prefix waitvbl
; @description Wait for the next vertical blank
; @placeholder ?wait

?wait
	lda	$d40b
	bne	?wait
```

Generate the VS Code snippet file with:

```bash
python3 extension/tools/build_snippets.py
```

Check that the committed generated file is up to date without modifying it:

```bash
python3 extension/tools/build_snippets.py --check
```

The generator handles VS Code-specific escaping, literal `$` characters, tab stops, mirrored placeholders, and the final cursor position automatically. See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete **Snippet Source Format v1**.

## Building the Extension (.vsix)

To package the extension from the repository, you need:

- Python 3
- Node.js
- VSCE (`@vscode/vsce`)

### Install Node.js

On Linux, using [nvm](https://github.com/nvm-sh/nvm) is convenient:

```bash
nvm install --lts
nvm use --lts
```

Verify the installation:

```bash
node -v
npm -v
```

### Install VSCE

```bash
npm install -g @vscode/vsce
```

### Build with the repository helper

From the repository root:

```bash
./make-vsix.sh
```

The script:

1. Generates and validates `extension/snippets/xasm.json`.
2. Bumps the extension patch version.
3. Packages the extension with VSCE.
4. Places the resulting `.vsix` in `dist/`.

You can also package manually from `extension/`, but regenerate snippets first if any file in `snippets-src/` has changed.

## Installing the Extension

1. Open VS Code.
2. Open **Extensions** (`Ctrl+Shift+X`).
3. Open the `...` menu and choose **Install from VSIX...**.
4. Select the generated `.vsix` file.
5. Open an `.asx` or `.xsm` file. VS Code should select **XASM** automatically.
6. Run **XASM: Initialize Project** if the project does not already contain its `.vscode` configuration.

## Contributing

Bug reports, improvements, and new snippets are welcome. In particular, reusable XASM routines can be contributed without writing VS Code snippet JSON.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[Unlicense](LICENSE) - released into the public domain.
