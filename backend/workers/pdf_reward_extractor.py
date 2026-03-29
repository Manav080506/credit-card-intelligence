"""Production-grade PDF reward extraction for credit card benefit documents.

Extracts reward rates, benefits, fees, and milestones from PDF files.
Handles multi-page documents, text normalization, confidence scoring.
"""

from __future__ import annotations

import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

logger = logging.getLogger(__name__)


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PDF_ARCHIVE_DIR = DATA_DIR / "pdf_guides"


class PDFRewardExtractor:
    """Extract reward structures from credit card PDF documents."""
    
    def __init__(self):
        self.extracted_data = {}
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text for consistent parsing."""
        # Remove extra whitespace, normalize line breaks
        text = " ".join(text.split())
        return text.lower()
    
    def extract_reward_rates_from_pdf(self, pdf_text: str) -> Dict[str, float]:
        """Extract reward rates from PDF text."""
        rates = {
            "online_shopping": 0.0,
            "dining": 0.0,
            "travel": 0.0,
            "groceries": 0.0,
            "fuel": 0.0,
            "utilities": 0.0,
            "general": 0.0,
        }
        
        # Pattern matching for common PDF structures
        patterns = {
            "online_shopping": [
                r"online\s+shopping[^.]{0,100}?(?:₹|rs\.?|points?)[^.]{0,50}?(\d+(?:\.\d+)?)\s*(?:%|per 100)",
                r"e[- ]?commerce[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"amazon\s+flipkart[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
            "dining": [
                r"dining\s+restaurants[^.]{0,100}?(?:cashback|points?)\s*(?:.*?)?(\d+(?:\.\d+)?)\s*%",
                r"restaurants\s+cafes[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"food\s+delivery[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
            "travel": [
                r"travel\s+(?:flights?|hotels?)[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"airlines\s+bookings[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
            "groceries": [
                r"grocery\s+supermarket[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"groceries[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
            "fuel": [
                r"fuel\s+(?:surcharge\s+)?(?:pump|station|petrol)[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"petrol\s+diesel[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
            "utilities": [
                r"(?:electricity|water|gas|phone|broadband|utility|billboard)[^.]{0,100}?(\d+(?:\.\d+)?)\s*(?:%|points?)",
                r"utility\s+bills[^.]{0,100}?(\d+(?:\.\d+)?)\s*%",
            ],
        }
        
        pdf_text_norm = self._normalize_text(pdf_text)
        
        for category, pattern_list in patterns.items():
            found_rates = []
            for pattern in pattern_list:
                matches = re.finditer(pattern, pdf_text_norm, re.IGNORECASE)
                for match in matches:
                    try:
                        rate = float(match.group(1)) / 100.0
                        found_rates.append(rate)
                    except (ValueError, IndexError):
                        continue
            
            if found_rates:
                rates[category] = max(found_rates)
        
        return rates
    
    def extract_annual_fee_from_pdf(self, pdf_text: str) -> float:
        """Extract annual fee from PDF."""
        patterns = [
            r"annual\s+fee[^\d₹inr]*?(?:₹|rs\.?|inr)\s*([0-9,]+)",
            r"membership\s+fee[^\d₹inr]*?(?:₹|rs\.?|inr)\s*([0-9,]+)",
            r"renewal\s+fee[^\d₹inr]*?(?:₹|rs\.?|inr)\s*([0-9,]+)",
        ]
        
        pdf_text_norm = self._normalize_text(pdf_text)
        
        for pattern in patterns:
            match = re.search(pattern, pdf_text_norm, re.IGNORECASE)
            if match:
                try:
                    fee_str = match.group(1).replace(",", "")
                    return float(fee_str)
                except ValueError:
                    continue
        
        return 0.0
    
    def extract_milestones_from_pdf(self, pdf_text: str) -> List[Dict]:
        """Extract milestone bonuses from PDF."""
        milestones = []
        
        # Look for milestone patterns
        patterns = [
            r"spend\s+(?:₹|rs\.?|inr)?\s*([0-9,]+)[^.]{0,80}?(?:get|earn|bonus)\s+(?:₹|rs\.?|inr)?\s*([0-9,]+)",
            r"(?:₹|rs\.?|inr)?\s*([0-9,]+)\s+spend[^.]{0,80}?(?:₹|rs\.?|inr)?\s*([0-9,]+)\s+(?:bonus|cashback)",
        ]
        
        pdf_text_norm = self._normalize_text(pdf_text)
        
        for pattern in patterns:
            for match in re.finditer(pattern, pdf_text_norm, re.IGNORECASE):
                try:
                    threshold = float(match.group(1).replace(",", ""))
                    bonus = float(match.group(2).replace(",", ""))
                    milestones.append({
                        "threshold": threshold,
                        "bonus": bonus,
                    })
                except (ValueError, IndexError):
                    continue
        
        return milestones
    
    def extract_benefits_from_pdf(self, pdf_text: str) -> Dict:
        """Extract categorical benefits from PDF."""
        benefits = {
            "lounge_access": False,
            "travel_insurance": False,
            "purchase_protection": False,
            "concierge": False,
            "fuel_surcharge_waiver": False,
        }
        
        pdf_text_lower = pdf_text.lower()
        
        if re.search(r"(?:airline|domestic|lounge)\s+(?:lounge|access)", pdf_text_lower):
            benefits["lounge_access"] = True
        
        if re.search(r"(?:travel\s+)?insurance", pdf_text_lower):
            benefits["travel_insurance"] = True
        
        if re.search(r"purchase\s+protection", pdf_text_lower):
            benefits["purchase_protection"] = True
        
        if re.search(r"concierge\s+service", pdf_text_lower):
            benefits["concierge"] = True
        
        if re.search(r"fuel\s+surcharge\s+waiver", pdf_text_lower):
            benefits["fuel_surcharge_waiver"] = True
        
        return benefits
    
    def extract_from_pdf_file(
        self,
        pdf_path: Path,
        card_name: str,
        bank: str
    ) -> Dict:
        """
        Extract reward data from a PDF file.
        
        Args:
            pdf_path: Path to PDF file
            card_name: Name of credit card
            bank: Issuing bank
        
        Returns:
            Structured reward data
        """
        if not HAS_PYPDF:
            return {
                "error": "PyPDF2 not installed",
                "card_name": card_name,
                "bank": bank,
            }
        
        try:
            with open(pdf_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                pdf_text = ""
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    pdf_text += f"\n--- Page {page_num + 1} ---\n{text}"
        except Exception as e:
            return {
                "error": f"PDF read error: {str(e)}",
                "card_name": card_name,
                "bank": bank,
            }
        
        # Extract structured data
        return {
            "card_name": card_name,
            "bank": bank,
            "source_pdf": str(pdf_path),
            "extracted_at": datetime.utcnow().isoformat(),
            "reward_rates": self.extract_reward_rates_from_pdf(pdf_text),
            "annual_fee": self.extract_annual_fee_from_pdf(pdf_text),
            "milestones": self.extract_milestones_from_pdf(pdf_text),
            "benefits": self.extract_benefits_from_pdf(pdf_text),
            "data_confidence": 0.75,  # PDFs are less precise than structured pages
            "extraction_method": "pdf_parsing",
        }


def extract_pdfs_from_directory(directory: Path) -> List[Dict]:
    """Extract reward data from all PDFs in a directory."""
    extractor = PDFRewardExtractor()
    results = []
    
    if not directory.exists():
        return results
    
    for pdf_file in directory.glob("**/*.pdf"):
        # Extract card name and bank from filename
        # Expected format: {bank}_{card_name}.pdf
        parts = pdf_file.stem.split("_", 1)
        if len(parts) != 2:
            continue
        
        bank, card_name = parts
        bank = bank.replace("-", " ").title()
        card_name = card_name.replace("-", " ").title()
        
        print(f"Extracting: {pdf_file}")
        result = extractor.extract_from_pdf_file(pdf_file, card_name, bank)
        results.append(result)
    
    return results


def run_pdf_extraction() -> Dict:
    """Main entry point for PDF extraction worker."""
    PDF_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    results = extract_pdfs_from_directory(PDF_ARCHIVE_DIR)
    
    # Save results
    output_file = DATA_DIR / "cards" / "extracted_from_pdfs.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    return {
        "status": "completed",
        "worker": "pdf_extractor",
        "pdfs_processed": len(results),
        "output_file": str(output_file),
    }


if __name__ == "__main__":
    result = run_pdf_extraction()
    print(json.dumps(result, indent=2))
