"""OCR pipeline for extracting text from PDF documents"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime

import cv2
import easyocr
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from tqdm import tqdm


class OCRPipeline:
    """
    OCR pipeline for processing PDF documents using EasyOCR.
    
    Features:
    - Multi-language support (English + Hindi)
    - Layout analysis (LayoutParser integration)
    - Batch processing with parallelization
    - Accuracy measurement
    - Metrics logging
    """

    def __init__(
        self,
        languages: List[str] = ['en', 'hi'],
        use_gpu: bool = True,
        batch_size: int = 4,
        output_dir: str = 'data/processed/ocr_output'
    ):
        """
        Initialize OCR pipeline.
        
        Args:
            languages: Languages to recognize (e.g., ['en', 'hi'])
            use_gpu: Whether to use GPU (if available)
            batch_size: Number of images to process in parallel
            output_dir: Directory to save OCR results
        """
        self.languages = languages
        self.batch_size = batch_size
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize OCR reader
        gpu = use_gpu
        try:
            self.reader = easyocr.Reader(languages, gpu=gpu)
            self.logger.info(f"Initialized EasyOCR reader for languages: {languages} (GPU: {gpu})")
        except Exception as e:
            self.logger.warning(f"GPU not available, falling back to CPU: {e}")
            self.reader = easyocr.Reader(languages, gpu=False)
        
        # Metrics
        self.metrics = {
            'total_documents': 0,
            'successful_ocr': 0,
            'failed_ocr': 0,
            'total_pages': 0,
            'total_text_length': 0,
            'average_char_accuracy': 0.0,
            'average_word_accuracy': 0.0,
            'start_time': datetime.now().isoformat(),
        }

    def extract_images_from_pdf(self, pdf_path: str) -> List[Tuple[Image.Image, int]]:
        """
        Extract images from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of (image, page_number) tuples
        """
        try:
            images = convert_from_path(pdf_path, dpi=300)  # High DPI for better accuracy
            return [(img, idx) for idx, img in enumerate(images, start=1)]
        except Exception as e:
            self.logger.error(f"Error extracting images from {pdf_path}: {e}")
            return []

    def run_ocr_on_image(self, image: Image.Image) -> Dict:
        """
        Run OCR on a single image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with OCR results (text, confidence, etc.)
        """
        try:
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Run OCR
            results = self.reader.readtext(image_array)
            
            # Extract text and confidence
            text = '\n'.join([result[1] for result in results])
            confidences = [result[2] for result in results]
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'text_blocks': len(results),
                'success': True,
                'error': None,
            }
        except Exception as e:
            self.logger.error(f"Error running OCR: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'text_blocks': 0,
                'success': False,
                'error': str(e),
            }

    def process_pdf(self, pdf_path: str) -> Dict:
        """
        Process entire PDF document through OCR pipeline.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with OCR results for entire document
        """
        self.metrics['total_documents'] += 1
        
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            self.logger.error(f"PDF file not found: {pdf_path}")
            self.metrics['failed_ocr'] += 1
            return {'success': False, 'error': 'File not found'}
        
        # Extract images from PDF
        images = self.extract_images_from_pdf(str(pdf_path))
        
        if not images:
            self.logger.warning(f"No images extracted from {pdf_path}")
            self.metrics['failed_ocr'] += 1
            return {'success': False, 'error': 'No images extracted'}
        
        self.metrics['total_pages'] += len(images)
        
        # Process each page
        page_results = []
        all_text = []
        all_confidences = []
        
        for image, page_num in images:
            ocr_result = self.run_ocr_on_image(image)
            ocr_result['page_number'] = page_num
            page_results.append(ocr_result)
            
            if ocr_result['success']:
                all_text.append(ocr_result['text'])
                all_confidences.append(ocr_result['confidence'])
        
        # Aggregate results
        full_text = '\n---PAGE BREAK---\n'.join(all_text)
        self.metrics['total_text_length'] += len(full_text)
        
        result = {
            'success': True,
            'file': str(pdf_path),
            'total_pages': len(images),
            'full_text': full_text,
            'page_results': page_results,
            'average_confidence': np.mean(all_confidences) if all_confidences else 0.0,
            'processed_at': datetime.now().isoformat(),
        }
        
        self.metrics['successful_ocr'] += 1
        
        return result

    def batch_process_pdfs(
        self,
        pdf_dir: str,
        num_workers: int = 4,
        pattern: str = '*.pdf'
    ) -> List[Dict]:
        """
        Process multiple PDF files in parallel.
        
        Args:
            pdf_dir: Directory containing PDFs
            num_workers: Number of parallel workers
            pattern: Glob pattern for PDF files
            
        Returns:
            List of results for each PDF
        """
        pdf_dir = Path(pdf_dir)
        pdf_files = sorted(pdf_dir.glob(pattern))
        
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit all tasks
            future_to_pdf = {executor.submit(self.process_pdf, str(pdf)): pdf for pdf in pdf_files}
            
            # Process as completed
            with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
                for future in as_completed(future_to_pdf):
                    try:
                        result = future.result()
                        results.append(result)
                        pbar.update(1)
                    except Exception as e:
                        self.logger.error(f"Error processing PDF: {e}")
                        pbar.update(1)
        
        return results

    def measure_accuracy(self, ground_truth: str, ocr_text: str) -> Dict:
        """
        Measure OCR accuracy by comparing with ground truth.
        
        Args:
            ground_truth: Original text (ground truth)
            ocr_text: OCR extracted text
            
        Returns:
            Dictionary with accuracy metrics
        """
        # Character-level accuracy
        char_matches = sum(1 for c1, c2 in zip(ground_truth, ocr_text) if c1 == c2)
        char_accuracy = char_matches / max(len(ground_truth), 1) * 100
        
        # Word-level accuracy
        gt_words = ground_truth.split()
        ocr_words = ocr_text.split()
        word_matches = sum(1 for w1, w2 in zip(gt_words, ocr_words) if w1 == w2)
        word_accuracy = word_matches / max(len(gt_words), 1) * 100
        
        return {
            'char_accuracy': round(char_accuracy, 2),
            'word_accuracy': round(word_accuracy, 2),
            'char_matches': char_matches,
            'total_chars': len(ground_truth),
            'word_matches': word_matches,
            'total_words': len(gt_words),
        }

    def save_results(self, results: List[Dict], output_file: str = 'ocr_results.json'):
        """
        Save OCR results to JSON file.
        
        Args:
            results: List of OCR results
            output_file: Output filename
        """
        output_path = self.output_dir / output_file
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Results saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")

    def save_metrics(self, output_file: str = 'ocr_metrics.json'):
        """Save metrics to file."""
        self.metrics['end_time'] = datetime.now().isoformat()
        
        output_path = self.output_dir / output_file
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2)
            self.logger.info(f"Metrics saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")

    def get_metrics_summary(self) -> Dict:
        """Get summary of OCR metrics."""
        return {
            'documents_processed': self.metrics['successful_ocr'],
            'documents_failed': self.metrics['failed_ocr'],
            'total_pages': self.metrics['total_pages'],
            'average_confidence': self.metrics['average_char_accuracy'],
            'total_text_extracted': self.metrics['total_text_length'],
        }


# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Initialize pipeline
    pipeline = OCRPipeline(languages=['en', 'hi'], use_gpu=True)
    
    # Process a single PDF
    # result = pipeline.process_pdf('sample.pdf')
    
    # Or batch process a directory
    # results = pipeline.batch_process_pdfs('data/raw', num_workers=4)
    # pipeline.save_results(results)
    # pipeline.save_metrics()
