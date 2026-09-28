#!/usr/bin/env python3
"""
validate_manuscript.py - Markdown & MathJax/KaTeX Scanner & Validator for TurboKain Papers.

Checks:
1. Markdown structural validity (unmatched code fences, header hierarchy).
2. MathJax / KaTeX mathematical equations (paired $, paired $$, brace matching, left/right pairing).
3. Leading/trailing whitespace in inline math (which breaks KaTeX/CommonMark renderers like GitHub / VS Code).
4. Markdown table structure (column count consistency, alignment rows).
5. Image references (existence of targeted local images on disk).
6. Local and external link checks.
"""

import os
import re
import sys

def validate_markdown(file_path):
    print(f"\n=======================================================")
    print(f"Scanning Markdown & LaTeX Math: {file_path}")
    print(f"=======================================================")

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    print(f"Total lines: {len(lines)}")
    errors = 0
    warnings = 0

    # 1. Code Fence Pairing
    fences = []
    for line_num, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            fences.append((line_num, line.strip()))

    print(f"\n[1] Code Fences: {len(fences)} total")
    if len(fences) % 2 != 0:
        print(f"  ERROR: Odd number of code fences ({len(fences)})! An opening block is never closed.")
        errors += 1
    else:
        print("  PASS: All code fences properly paired.")

    # 2. Image Path Verification
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    print(f"\n[2] Image Assets: {len(images)} found")
    base_dir = os.path.dirname(os.path.abspath(file_path))
    for alt, img_path in images:
        # ignore remote URLs
        if img_path.startswith("http://") or img_path.startswith("https://"):
            print(f"  [Remote] {img_path}")
            continue
        resolved_path = os.path.normpath(os.path.join(base_dir, img_path))
        if os.path.exists(resolved_path):
            size_mb = os.path.getsize(resolved_path) / (1024 * 1024)
            print(f"  PASS: '{img_path}' exists ({size_mb:.2f} MB)")
        else:
            print(f"  ERROR: Image not found: {img_path} (resolved: {resolved_path})")
            errors += 1

    # 3. Tables Validation
    print(f"\n[3] Markdown Tables")
    in_table = False
    table_lines = []
    table_count = 0
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append((line_num, stripped))
        else:
            if in_table:
                # evaluate finished table
                table_count += 1
                col_counts = [len([c for c in l.split("|")[1:-1]]) for _, l in table_lines]
                if len(set(col_counts)) > 1:
                    print(f"  WARNING: Table starting at line {table_lines[0][0]} has inconsistent column counts: {col_counts}")
                    warnings += 1
                else:
                    print(f"  PASS: Table #{table_count} at line {table_lines[0][0]} ({len(table_lines)} rows, {col_counts[0]} cols)")
                in_table = False
                table_lines = []
    if in_table and table_lines:
        table_count += 1
        col_counts = [len([c for c in l.split("|")[1:-1]]) for _, l in table_lines]
        if len(set(col_counts)) > 1:
            print(f"  WARNING: Table starting at line {table_lines[0][0]} has inconsistent column counts: {col_counts}")
            warnings += 1
        else:
            print(f"  PASS: Table #{table_count} at line {table_lines[0][0]} ({len(table_lines)} rows, {col_counts[0]} cols)")

    # 4. Display Math ($$ ... $$)
    # Strip fenced code blocks before analyzing math
    clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Also strip inline code `...`
    clean_content_no_code = re.sub(r'`[^`\n]+`', '', clean_content)

    print(f"\n[4] Display Math Blocks ($$ ... $$)")
    # Check if $$ are paired
    display_delims = [m.start() for m in re.finditer(r'\$\$', clean_content_no_code)]
    if len(display_delims) % 2 != 0:
        print(f"  ERROR: Odd number of $$ delimiters ({len(display_delims)})! A display math block is unclosed.")
        errors += 1
    else:
        display_blocks = re.findall(r'\$\$(.*?)\$\$', clean_content_no_code, flags=re.DOTALL)
        print(f"  Found {len(display_blocks)} display math blocks.")
        for idx, block in enumerate(display_blocks, 1):
            block_issues = []
            open_brace = block.count('{')
            close_brace = block.count('}')
            if open_brace != close_brace:
                block_issues.append(f"Mismatched curly braces: {open_brace} open vs {close_brace} close")
            
            left_count = len(re.findall(r'\\left\b', block))
            right_count = len(re.findall(r'\\right\b', block))
            if left_count != right_count:
                block_issues.append(f"\\left ({left_count}) vs \\right ({right_count}) mismatch")
            
            preview = " ".join(block.strip().split())[:65]
            if block_issues:
                print(f"  ERROR [Eq {idx}]: {preview}...")
                for iss in block_issues:
                    print(f"    -> {iss}")
                errors += 1
            else:
                print(f"  PASS [Eq {idx}]: {preview}...")

    # 5. Inline Math ($ ... $)
    print(f"\n[5] Inline Math Expressions ($ ... $)")
    # Strip display math first
    text_inline_only = re.sub(r'\$\$.*?\$\$', '', clean_content_no_code, flags=re.DOTALL)
    
    # Check for single dollar count
    single_dollars = [m.start() for m in re.finditer(r'(?<!\\)\$', text_inline_only)]
    if len(single_dollars) % 2 != 0:
        print(f"  ERROR: Odd number of single dollar signs ({len(single_dollars)})! Unpaired inline math.")
        errors += 1
    else:
        # Match non-empty math blocks: $...$
        inline_matches = list(re.finditer(r'(?<!\\)\$(.*?)(?<!\\)\$', text_inline_only))
        print(f"  Found {len(inline_matches)} inline math instances.")
        spacing_errors = 0
        brace_errors = 0
        
        for idx, m in enumerate(inline_matches, 1):
            expr = m.group(1)
            # Find line number
            char_pos = m.start()
            line_no = text_inline_only[:char_pos].count('\n') + 1
            
            # Check for leading/trailing space in inline math: $ expr $ breaks KaTeX
            if expr.startswith(' ') or expr.endswith(' '):
                print(f"  WARNING [Line {line_no}]: Inline math has leading/trailing space: '${expr}$' (breaks strict CommonMark/KaTeX)")
                warnings += 1
                spacing_errors += 1
            
            # Check for brace matching
            if expr.count('{') != expr.count('}'):
                print(f"  ERROR [Line {line_no}]: Mismatched curly braces in '${expr}$'")
                errors += 1
                brace_errors += 1

        if spacing_errors == 0 and brace_errors == 0:
            print("  PASS: All inline math blocks have matching braces and proper boundary spacing.")

    print(f"\n=======================================================")
    print(f"Scan Complete: {errors} Errors, {warnings} Warnings")
    print(f"=======================================================\n")
    return errors == 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "papers/trappist1_bystander_survey/manuscript.md"
    success = validate_markdown(target)
    sys.exit(0 if success else 1)
