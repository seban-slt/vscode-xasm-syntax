#!/usr/bin/env python3
"""Build VS Code snippets from human-friendly XASM source files.

Snippet Source Format v1
------------------------
Each .xsm file in extension/snippets-src/ defines one snippet. Metadata is
stored in a contiguous comment header at the top of the file:

    ; @name Detect Stereo Routine
    ; @prefix stereo
    ; @description Detect presence of a second POKEY
    ; @placeholder detect_stereo
    ; @placeholder ?loop

The rest of the file is ordinary XASM source. The generator converts literal
'$' characters to VS Code snippet-safe form, preserves tabs, numbers
placeholders in declaration order, mirrors repeated placeholder occurrences,
and appends the final $0 cursor stop automatically.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
EXTENSION_DIR = SCRIPT_DIR.parent
DEFAULT_SOURCE_DIR = EXTENSION_DIR / "snippets-src"
DEFAULT_OUTPUT = EXTENSION_DIR / "snippets" / "xasm.json"

META_RE = re.compile(r"^\s*;\s*@([A-Za-z][A-Za-z0-9_-]*)(?:\s+(.*?))?\s*$")
KNOWN_DIRECTIVES = {"name", "prefix", "description", "placeholder"}
REQUIRED_DIRECTIVES = ("name", "prefix", "description")

# Characters considered part of an XASM-ish token for placeholder boundaries.
TOKEN_CHARS = set("_?$")


@dataclass
class SnippetSource:
    path: Path
    name: str
    prefix: str
    description: str
    placeholders: list[str]
    body: list[str]


def is_token_char(char: str) -> bool:
    return char.isalnum() or char in TOKEN_CHARS


def has_placeholder_boundaries(text: str, start: int, value: str) -> bool:
    """Return True if a literal match does not sit inside a larger token."""
    end = start + len(value)

    if value and is_token_char(value[0]) and start > 0:
        if is_token_char(text[start - 1]):
            return False

    if value and is_token_char(value[-1]) and end < len(text):
        if is_token_char(text[end]):
            return False

    return True


def find_placeholder(text: str, value: str, start: int) -> int | None:
    """Find the next boundary-safe occurrence of *value* in *text*."""
    pos = text.find(value, start)
    while pos != -1:
        if has_placeholder_boundaries(text, pos, value):
            return pos
        pos = text.find(value, pos + 1)
    return None


def escape_literal(text: str) -> str:
    """Escape ordinary source text for the VS Code snippet parser.

    json.dumps() performs JSON escaping later. Here we only escape characters
    that have meaning to the snippet parser itself.
    """
    return text.replace("\\", "\\\\").replace("$", "\\$")


def escape_placeholder_default(text: str) -> str:
    """Escape text used inside ${N:default}."""
    return (
        text.replace("\\", "\\\\")
        .replace("$", "\\$")
        .replace("}", "\\}")
    )


def parse_source(path: Path) -> tuple[SnippetSource | None, list[str]]:
    errors: list[str] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return None, [f"{path}: cannot read file: {exc}"]

    metadata: dict[str, str] = {}
    placeholders: list[str] = []

    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1

    header_seen = False
    while index < len(lines):
        match = META_RE.match(lines[index])
        if not match:
            break

        header_seen = True
        directive = match.group(1).lower()
        value = (match.group(2) or "").strip()

        if directive not in KNOWN_DIRECTIVES:
            errors.append(
                f"{path}:{index + 1}: unknown metadata directive '@{directive}'"
            )
        elif not value:
            errors.append(
                f"{path}:{index + 1}: '@{directive}' requires a value"
            )
        elif directive == "placeholder":
            if value in placeholders:
                errors.append(
                    f"{path}:{index + 1}: duplicate placeholder '{value}'"
                )
            else:
                placeholders.append(value)
        else:
            if directive in metadata:
                errors.append(
                    f"{path}:{index + 1}: duplicate '@{directive}' directive"
                )
            else:
                metadata[directive] = value

        index += 1

    if not header_seen:
        errors.append(f"{path}: missing snippet metadata header")

    # A blank separator between metadata and XASM body is formatting only.
    while index < len(lines) and not lines[index].strip():
        index += 1

    body = lines[index:]

    # Metadata belongs only in the header. Catch accidental/late directives,
    # including typos that otherwise would silently end up in the snippet.
    for line_no, line in enumerate(body, start=index + 1):
        match = META_RE.match(line)
        if match:
            errors.append(
                f"{path}:{line_no}: metadata directives must be in the header"
            )

    for directive in REQUIRED_DIRECTIVES:
        if directive not in metadata:
            errors.append(f"{path}: missing required '@{directive}' directive")

    if not body:
        errors.append(f"{path}: snippet body is empty")

    if errors:
        return None, errors

    return (
        SnippetSource(
            path=path,
            name=metadata["name"],
            prefix=metadata["prefix"],
            description=metadata["description"],
            placeholders=placeholders,
            body=body,
        ),
        [],
    )


def transform_body(snippet: SnippetSource) -> tuple[list[str], list[str]]:
    """Convert ordinary XASM lines to VS Code snippet body lines."""
    errors: list[str] = []
    seen = [0] * len(snippet.placeholders)
    output: list[str] = []

    for line in snippet.body:
        pos = 0
        converted: list[str] = []

        while pos < len(line):
            candidates: list[tuple[int, int, int]] = []

            for placeholder_index, value in enumerate(snippet.placeholders):
                found = find_placeholder(line, value, pos)
                if found is not None:
                    # Earliest match wins; for ties, prefer the longest value,
                    # then declaration order for deterministic output.
                    candidates.append((found, -len(value), placeholder_index))

            if not candidates:
                converted.append(escape_literal(line[pos:]))
                pos = len(line)
                break

            found, _negative_length, placeholder_index = min(candidates)
            value = snippet.placeholders[placeholder_index]
            converted.append(escape_literal(line[pos:found]))

            tabstop = placeholder_index + 1
            if seen[placeholder_index] == 0:
                converted.append(
                    f"${{{tabstop}:{escape_placeholder_default(value)}}}"
                )
            else:
                converted.append(f"${tabstop}")

            seen[placeholder_index] += 1
            pos = found + len(value)

        if pos == 0 and not line:
            # Empty source line.
            converted.append("")

        output.append("".join(converted))

    for placeholder_index, count in enumerate(seen):
        if count == 0:
            errors.append(
                f"{snippet.path}: placeholder "
                f"'{snippet.placeholders[placeholder_index]}' does not occur in snippet body"
            )

    # Final cursor position is intentionally implicit in source format v1.
    output.append("$0")
    return output, errors


def validate_collection(snippets: Iterable[SnippetSource]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    by_name: dict[str, Path] = {}
    by_prefix: dict[str, list[Path]] = {}

    for snippet in snippets:
        if snippet.name in by_name:
            errors.append(
                f"duplicate snippet name '{snippet.name}': "
                f"{by_name[snippet.name]} and {snippet.path}"
            )
        else:
            by_name[snippet.name] = snippet.path

        by_prefix.setdefault(snippet.prefix, []).append(snippet.path)

    for prefix, paths in sorted(by_prefix.items()):
        if len(paths) > 1:
            joined = ", ".join(str(path) for path in paths)
            warnings.append(f"prefix '{prefix}' is used by multiple snippets: {joined}")

    return errors, warnings


def build_document(snippets: list[SnippetSource]) -> tuple[dict[str, object], list[str]]:
    document: dict[str, object] = {}
    errors: list[str] = []

    for snippet in snippets:
        body, body_errors = transform_body(snippet)
        errors.extend(body_errors)
        document[snippet.name] = {
            "prefix": snippet.prefix,
            "body": body,
            "description": snippet.description,
        }

    return document, errors


def render_json(document: dict[str, object]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate VS Code XASM snippets from snippets-src/*.xsm"
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help=f"source directory (default: {DEFAULT_SOURCE_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"generated JSON file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate sources and fail if the generated file is out of date",
    )
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    output_path = args.output.resolve()

    source_paths = sorted(source_dir.rglob("*.xsm")) if source_dir.is_dir() else []
    if not source_paths:
        print(f"ERROR: no .xsm snippet sources found in {source_dir}", file=sys.stderr)
        return 1

    snippets: list[SnippetSource] = []
    errors: list[str] = []

    for path in source_paths:
        snippet, parse_errors = parse_source(path)
        errors.extend(parse_errors)
        if snippet is not None:
            snippets.append(snippet)

    collection_errors, warnings = validate_collection(snippets)
    errors.extend(collection_errors)

    document, transform_errors = build_document(snippets)
    errors.extend(transform_errors)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Snippet generation aborted with {len(errors)} error(s); output was not modified.",
            file=sys.stderr,
        )
        return 1

    rendered = render_json(document)

    if args.check:
        try:
            current = output_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            current = ""
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: cannot read {output_path}: {exc}", file=sys.stderr)
            return 1

        if current != rendered:
            print(
                f"ERROR: generated snippets are out of date: {output_path}\n"
                f"Run: python3 {Path(__file__).resolve()}",
                file=sys.stderr,
            )
            return 1

        print(f"OK: {len(snippets)} snippet(s) validated; generated file is up to date.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(output_path)
    except OSError as exc:
        print(f"ERROR: cannot write {output_path}: {exc}", file=sys.stderr)
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        return 1

    print(f"Generated {len(snippets)} snippet(s): {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
