# XASM VS Code Extension

This repository contains a Visual Studio Code extension that provides syntax highlighting for **XASM assembler** source files (`.asx`, `.xsm`).

---

## Repository Structure
- **extension/**
  The VS Code extension itself. Contains the grammar (`tmLanguage.json`), configuration, icon and README.
- **examples/**
  Example XASM projects with ready-to-use `.vscode/` configuration (tasks, launch). Useful for testing and learning how to integrate with Altirra or Atari800 emulator.

---

## Features
- Highlighting for **6502 mnemonics**
- Highlighting for **directives** (`org`, `equ`, `opt`, …)
- Highlighting for **XASM pseudo-instructions** (`mwa`, `mvy`, `mwx`, …)
- Detection of **labels** at column 0
- Comments starting with `;`
- Hexadecimal numbers (`$1234`)

File types:
- `.asx`
- `.xsm`

---

## Building the Extension (.vsix)

To package the extension into a `.vsix` file you need **Node.js** and the **VSCE** tool.

### 1. Install Node.js
On Linux it is easiest to use [nvm](https://github.com/nvm-sh/nvm):

```bash
nvm install --lts
nvm use --lts
```

Verify installation:
```bash
node -v
npm -v
```

### 2. Install VSCE
```bash
npm install -g @vscode/vsce
```

### 3. Package the extension
Change into the `extension/` directory:

```bash
cd extension
vsce package --no-yarn
```

This will create a file such as:
```
slt.xasm-syntax-0.0.1.vsix
```

### 4. Install the extension in VS Code
- Open VS Code → Extensions (Ctrl+Shift+X) → `...` menu → **Install from VSIX…**
- Select the generated `.vsix` file.
- Open an `.asx` or `.xsm` file and the language should switch to **XASM** automatically.

---

## Contributing
Bug reports and pull requests are welcome.
Please use GitHub Issues to report problems or suggest improvements.

---

## License
[Unlicense](LICENSE) – released into the public domain.
