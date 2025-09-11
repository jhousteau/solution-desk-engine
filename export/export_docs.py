#!/usr/bin/env python3
"""
Document Export Runner
Simple interface to run the conversion scripts from the export folder.
"""

import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python export_docs.py <format> [options]")
        print("Formats: docx, pdf, googledocs")
        print("\nExamples:")
        print(
            "  python export_docs.py docx --file opportunity/9-contract/client-daf-sow-pov.md --verbose"
        )
        print("  python export_docs.py pdf --phase 9-contract --verbose")
        print("  python export_docs.py googledocs --verbose --create-index")
        sys.exit(1)

    format_type = sys.argv[1].lower()
    remaining_args = sys.argv[2:]

    # Map format to script
    scripts = {
        "docx": "export/scripts/convert_to_docx.py",
        "pdf": "export/scripts/convert_to_pdf.py",
        "googledocs": "export/scripts/convert_to_googledocs.py",
    }

    if format_type not in scripts:
        print(
            f"Error: Unknown format '{format_type}'. Choose: {', '.join(scripts.keys())}"
        )
        sys.exit(1)

    script_path = Path(scripts[format_type])
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Run the conversion script
    cmd = ["poetry", "run", "python", str(script_path)] + remaining_args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
