# Contributing to XASM Syntax Highlighting

Contributions are welcome: grammar fixes, example-project improvements, documentation, and especially reusable XASM snippets.

## Adding a Snippet

Snippet contributors do not need to know the VS Code snippet JSON format.

Add one `.xsm` file to `extension/snippets-src/`. One source file defines one snippet. Subdirectories are allowed.

### Snippet Source Format v1

Metadata is stored in a contiguous XASM comment header at the top of the file:

```asm
; @name Detect Stereo Routine
; @prefix stereo
; @description Stereo detect routine (2nd POKEY presence check)
; @placeholder detect_stereo
; @placeholder ?loop
; @placeholder ?mono
```

The supported directives are:

- `@name` - snippet name displayed by VS Code; required and unique.
- `@prefix` - text used to trigger the snippet; required.
- `@description` - short description displayed by VS Code; required.
- `@placeholder` - optional editable value. It may be specified more than once.

Everything after the metadata header is ordinary XASM source code.

### Placeholders

Placeholder numbers are assigned automatically in declaration order:

```asm
; @placeholder routine_name
; @placeholder ?loop
```

The first occurrence of each value becomes an editable tab stop. Later occurrences mirror the same value automatically.

For example:

```asm
; @name Simple Loop
; @prefix simpleloop
; @description Insert a simple XASM loop
; @placeholder ?loop

?loop
	dex
	bne	?loop
```

When the inserted `?loop` is renamed in VS Code, both occurrences change together.

A placeholder can also be a numeric value or address, for example:

```asm
; @placeholder $2000
```

The generator uses boundary-aware matching so a placeholder such as `loop` is not replaced inside a larger identifier such as `main_loop_counter`.

### Important Rules

- Write normal XASM. Do not write `${1:...}`, `$0`, `\\$`, or any other VS Code-specific snippet syntax.
- Use ordinary XASM hexadecimal notation such as `$d40a` and `#$ff`. The generator escapes `$` automatically.
- Use real tab characters if that is how you want the inserted code formatted. JSON `\t` escaping is handled automatically.
- Metadata directives must be at the top of the file.
- The first textual occurrence of a declared placeholder is its primary editable location.
- The final `$0` cursor stop is appended automatically.

## Generate the Snippet JSON

From the repository root:

```bash
python3 extension/tools/build_snippets.py
```

On systems where Python is installed under another command, use for example:

```powershell
py -3 extension/tools/build_snippets.py
```

The generated file is:

```text
extension/snippets/xasm.json
```

It is a generated artifact and must not be edited manually. Please include the regenerated file in the same pull request as the `.xsm` source change.

To validate the sources and verify that the generated file is current:

```bash
python3 extension/tools/build_snippets.py --check
```

The generator refuses to overwrite a valid output file if source validation fails.

## Validation

The generator reports errors for conditions such as:

- missing `@name`, `@prefix`, or `@description`;
- unknown metadata directives;
- duplicate snippet names;
- duplicate placeholder declarations;
- placeholders that never occur in the snippet body.

Duplicate prefixes are allowed but produce a warning because VS Code can present more than one completion for the same prefix.

## Testing the Extension

After regenerating snippets, package the extension with:

```bash
./make-vsix.sh
```

or use the usual VS Code Extension Development Host workflow if you are working directly on the extension.

Before submitting a pull request, at minimum run:

```bash
python3 extension/tools/build_snippets.py --check
```
