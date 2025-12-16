#!/usr/bin/env python3
"""
PDF Conversion Script for [CLIENT] F&I Documentation
Converts markdown files to professionally styled PDFs using markdown-pdf library.
"""

import argparse
import json
import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from markdown_pdf import MarkdownPdf, Section
except ImportError:
    print("Error: markdown-pdf not installed. Run: poetry install")
    sys.exit(1)

try:
    from branding_manager import BrandingManager
except ImportError:
    print(
        "Error: branding_manager.py not found. Ensure it exists in the same directory."
    )
    sys.exit(1)

# Configuration
OPPORTUNITY_DIR = Path("../../opportunity")
OUTPUT_DIR = Path("../pdf")
BRANDING_DIR = Path("../../branding")
METADATA_DIR = Path("../_metadata")


class DocumentProcessor:
    """Processes markdown documents and converts them to PDF."""

    def __init__(self, output_dir: Path, verbose: bool = False, custom_css: str = None):
        self.output_dir = output_dir
        self.verbose = verbose
        self.conversion_log = []
        self.failed_conversions = []
        self.custom_css = custom_css

        # Setup logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Initialize branding manager
        self.branding = BrandingManager(BRANDING_DIR)

    def extract_metadata(self, content: str) -> Dict:
        """Extract metadata from markdown frontmatter."""
        metadata = {
            "title": "",
            "author": "Capgemini",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "phase": "",
            "document_type": "documentation",
        }

        # Extract YAML frontmatter
        if content.startswith("---"):
            try:
                end_marker = content.find("---", 3)
                if end_marker != -1:
                    frontmatter = content[3:end_marker].strip()
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip().strip("\"'")
                            if key in metadata:
                                metadata[key] = value
            except Exception as e:
                self.logger.warning(f"Error parsing frontmatter: {e}")

        # Extract title from first H1 if not in frontmatter
        if not metadata["title"]:
            h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if h1_match:
                metadata["title"] = h1_match.group(1).strip()

        return metadata

    def preprocess_content(self, content: str, file_path: Path) -> str:
        """Preprocess markdown content for better PDF conversion."""
        # Determine phase from file path
        phase = self.get_phase_from_path(file_path)

        # Add document header if not present
        if not content.startswith("#"):
            title = file_path.stem.replace("-", " ").title()
            content = f"# {title}\n\n{content}"

        # Add phase styling class with brand colors
        if phase:
            content = f'<div class="phase-header" data-phase="{phase}">\n\n{content}\n\n</div>'

        # Process Mermaid diagrams (placeholder for now)
        mermaid_pattern = r"```mermaid\n(.*?)\n```"
        mermaid_matches = re.findall(mermaid_pattern, content, re.DOTALL)
        if mermaid_matches:
            self.logger.info(
                f"Found {len(mermaid_matches)} Mermaid diagrams in {file_path}"
            )
            # For now, just wrap in a div for styling
            content = re.sub(
                mermaid_pattern,
                r'<div class="mermaid">\n```mermaid\n\1\n```\n</div>',
                content,
                flags=re.DOTALL,
            )

        # Add page breaks before major sections
        content = re.sub(
            r"^(#{1,2}\s)",
            r'<div class="page-break"></div>\n\n\1',
            content,
            flags=re.MULTILINE,
        )

        return content

    def get_phase_from_path(self, file_path: Path) -> Optional[str]:
        """Extract phase from file path."""
        path_parts = file_path.parts
        for part in path_parts:
            # Check against branding manager's phase definitions
            if (
                part.startswith(
                    ("0-", "1-", "2-", "3-", "4-", "5-", "6-", "7-", "8-", "9-")
                )
                and "-" in part
            ):
                return part
        return None

    def load_css(self, phase: str = None) -> str:
        """Load and return branded CSS content."""
        if self.custom_css:
            return self.custom_css

        # Generate branded CSS using branding manager
        return self.branding.generate_pdf_css(phase)

    def convert_file(self, input_path: Path, output_path: Path) -> bool:
        """Convert a single markdown file to PDF."""
        try:
            # Read markdown content
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract metadata and enhance with branding
            metadata = self.extract_metadata(content)
            phase = self.get_phase_from_path(input_path)
            title = metadata.get("title", input_path.stem.replace("-", " ").title())
            brand_metadata = self.branding.get_brand_metadata(title, phase)
            metadata.update(brand_metadata)

            # Preprocess content with branding
            processed_content = self.preprocess_content(content, input_path)

            # Load branded CSS
            css_content = self.load_css(phase)

            # Create PDF with enhanced metadata
            pdf = MarkdownPdf(toc_level=6, optimize=True)

            # Set document metadata
            pdf.meta = {
                "title": metadata["title"],
                "author": metadata["author"],
                "subject": metadata["subject"],
                "creator": metadata["creator"],
                "keywords": metadata["keywords"],
            }

            # Add document section with branded CSS
            section = Section(processed_content)
            pdf.add_section(section, user_css=css_content)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save PDF
            pdf.save(str(output_path))

            # Log success
            self.conversion_log.append(
                {
                    "input": str(input_path),
                    "output": str(output_path),
                    "status": "success",
                    "metadata": metadata,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            if self.verbose:
                self.logger.info(f"Converted: {input_path} -> {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {e}")
            self.failed_conversions.append(
                {
                    "input": str(input_path),
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return False

    def find_markdown_files(self, directory: Path) -> List[Path]:
        """Find all markdown files in directory."""
        if not directory.exists():
            self.logger.warning(f"Directory not found: {directory}")
            return []

        md_files = []
        for file_path in directory.rglob("*.md"):
            if file_path.is_file():
                md_files.append(file_path)

        return sorted(md_files)

    def create_output_structure(self, input_dir: Path, output_dir: Path) -> None:
        """Create output directory structure mirroring input."""
        # Create phase directories based on common phase patterns
        phase_patterns = [
            "0-source",
            "1-research",
            "2-requirements",
            "3-analysis",
            "4-business-case",
            "5-architecture",
            "6-solution-design",
            "7-implementation-plan",
            "8-proposal",
            "9-contract",
            "10-audit",
        ]

        for phase in phase_patterns:
            phase_dir = output_dir / phase
            phase_dir.mkdir(parents=True, exist_ok=True)

        # Create metadata directory
        METADATA_DIR.mkdir(parents=True, exist_ok=True)

    def process_directory(self, input_dir: Path, max_workers: int = 4) -> Dict:
        """Process all markdown files in directory."""
        # Find all markdown files
        md_files = self.find_markdown_files(input_dir)

        if not md_files:
            self.logger.warning(f"No markdown files found in {input_dir}")
            return {"total": 0, "successful": 0, "failed": 0}

        # Create output structure
        self.create_output_structure(input_dir, self.output_dir)

        # Process files
        successful = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all conversion tasks
            future_to_file = {}
            for md_file in md_files:
                # Calculate relative path from input directory
                rel_path = md_file.relative_to(input_dir)

                # Change extension to .pdf
                pdf_name = rel_path.with_suffix(".pdf")
                output_path = self.output_dir / pdf_name

                future = executor.submit(self.convert_file, md_file, output_path)
                future_to_file[future] = md_file

            # Process completed tasks
            for future in as_completed(future_to_file):
                md_file = future_to_file[future]
                try:
                    success = future.result()
                    if success:
                        successful += 1
                    else:
                        failed += 1
                except Exception as e:
                    self.logger.error(f"Unexpected error processing {md_file}: {e}")
                    failed += 1

        return {"total": len(md_files), "successful": successful, "failed": failed}

    def save_metadata(self) -> None:
        """Save conversion metadata to files."""
        # Save conversion log
        log_file = METADATA_DIR / "conversion-log.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.conversion_log, f, indent=2, ensure_ascii=False)

        # Save failed conversions
        if self.failed_conversions:
            failed_file = METADATA_DIR / "failed-conversions.json"
            with open(failed_file, "w", encoding="utf-8") as f:
                json.dump(self.failed_conversions, f, indent=2, ensure_ascii=False)

        # Create document index
        index = {
            "conversion_date": datetime.now().isoformat(),
            "total_files": len(self.conversion_log),
            "successful_conversions": len(self.conversion_log),
            "failed_conversions": len(self.failed_conversions),
            "phases": {},
        }

        # Group by phase
        for log_entry in self.conversion_log:
            input_path = Path(log_entry["input"])
            phase = self.get_phase_from_path(input_path)
            if phase:
                if phase not in index["phases"]:
                    index["phases"][phase] = []
                index["phases"][phase].append(
                    {
                        "title": log_entry["metadata"]["title"],
                        "input": log_entry["input"],
                        "output": log_entry["output"],
                    }
                )

        index_file = METADATA_DIR / "document-index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Convert [CLIENT] F&I documentation to PDF"
    )
    parser.add_argument(
        "--custom-css", help="Path to custom CSS file (overrides branding)"
    )
    parser.add_argument("--file", help="Process only specific file")
    parser.add_argument(
        "--phase", help="Process only specific phase (e.g., 5-architecture)"
    )
    parser.add_argument(
        "--parallel", type=int, default=4, help="Number of parallel conversions"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Setup paths
    base_dir = Path.cwd()
    opportunity_dir = base_dir / OPPORTUNITY_DIR
    output_dir = base_dir / OUTPUT_DIR

    # Check if opportunity directory exists
    if not opportunity_dir.exists():
        print(f"Error: {opportunity_dir} directory not found")
        sys.exit(1)

    # Load custom CSS if provided
    custom_css = None
    if args.custom_css:
        css_path = Path(args.custom_css)
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                custom_css = f.read()
        else:
            print(f"Warning: Custom CSS file not found: {css_path}")

    # Create processor with branding
    processor = DocumentProcessor(output_dir, args.verbose, custom_css)

    print("Converting [CLIENT] F&I documentation to PDF with Capgemini branding...")
    print(f"Parallel workers: {args.parallel}")
    if custom_css:
        print(f"Using custom CSS: {args.custom_css}")
    else:
        print("Using integrated Capgemini brand styling")

    # Process specific file, phase, or all
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        print(f"Processing file: {file_path}")
        # Calculate relative path from input directory
        if file_path.is_relative_to(opportunity_dir):
            rel_path = file_path.relative_to(opportunity_dir)
        else:
            rel_path = Path(file_path.name)
        output_path = output_dir / rel_path.with_suffix(".pdf")

        success = processor.convert_file(file_path, output_path)
        results = {
            "total": 1,
            "successful": 1 if success else 0,
            "failed": 0 if success else 1,
        }
    elif args.phase:
        phase_dir = opportunity_dir / args.phase
        if not phase_dir.exists():
            print(f"Error: Phase directory not found: {phase_dir}")
            sys.exit(1)

        print(f"Processing phase: {args.phase}")
        results = processor.process_directory(phase_dir, args.parallel)
    else:
        print("Processing all phases...")
        results = processor.process_directory(opportunity_dir, args.parallel)

    # Save metadata
    processor.save_metadata()

    # Print results
    print("\nConversion Results:")
    print(f"Total files: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

    if results["failed"] > 0:
        print(
            f"\nFailed conversions logged to: {METADATA_DIR / 'failed-conversions.json'}"
        )

    print(f"\nOutput directory: {output_dir}")
    print(f"Metadata saved to: {METADATA_DIR}")


if __name__ == "__main__":
    main()
