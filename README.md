# XASM VS Code Extension

This repository contains a Visual Studio Code extension for **XASM assembler** source files (`.asx`, `.xsm`). It provides syntax highlighting, XASM snippets, and an example cross-platform build/run setup.

## Features

- Highlighting for **6502 mnemonics**
- Highlighting for **XASM directives** (`org`, `equ`, `opt`, ...)
- Highlighting for **XASM pseudo-instructions** (`mwa`, `mvy`, `mwx`, ...)
- Detection of labels at column 0, including XASM local labels such as `?loop`
- Comments starting with `;`
- Hexadecimal numbers (`$1234`)
- Snippets for reusable XASM routines
- Human-friendly snippet sources: snippets are written as normal `.xsm` files and converted to the VS Code JSON format automatically

Supported file types:

- `.asx`
- `.xsm`

## Repository Structure

```text
extension/
├── package.json
├── language-configuration.json
├── syntaxes/
│   └── xasm.tmLanguage.json
├── snippets-src/              # Human-edited XASM snippet sources
│   └── detect_stereo.xsm
├── snippets/
│   └── xasm.json              # Generated; do not edit directly
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

The `example/` directory contains ready-to-use VS Code configuration for compiling XASM source and launching an emulator on Linux, macOS, and Windows.

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

## Contributing

Bug reports, improvements, and new snippets are welcome. In particular, reusable XASM routines can be contributed without writing VS Code snippet JSON.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[Unlicense](LICENSE) - released into the public domain.
