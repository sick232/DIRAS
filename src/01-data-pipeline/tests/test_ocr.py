"""Tests for OCR pipeline"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from ..ocr import OCRPipeline


class TestOCRPipeline:
    """Tests for OCRPipeline class"""

    def test_initialization(self):
        """Test OCR pipeline initialization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            assert pipeline.languages == ['en', 'hi']
            assert pipeline.reader is not None
            assert Path(tmpdir).exists()

    def test_metrics_initialization(self):
        """Test that metrics are initialized correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            assert 'total_documents' in pipeline.metrics
            assert pipeline.metrics['total_documents'] == 0
            assert pipeline.metrics['successful_ocr'] == 0
            assert pipeline.metrics['failed_ocr'] == 0

    def test_accuracy_measurement_perfect_match(self):
        """Test accuracy measurement with perfect match"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            text = "This is test text"
            accuracy = pipeline.measure_accuracy(text, text)
            
            assert accuracy['char_accuracy'] == 100.0
            assert accuracy['word_accuracy'] == 100.0

    def test_accuracy_measurement_partial_match(self):
        """Test accuracy measurement with partial match"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            ground_truth = "This is test text"
            ocr_text = "This is best text"  # One character different
            
            accuracy = pipeline.measure_accuracy(ground_truth, ocr_text)
            
            assert accuracy['char_accuracy'] < 100.0
            assert accuracy['char_accuracy'] > 0.0

    def test_metrics_saving(self):
        """Test saving metrics to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            pipeline.metrics['successful_ocr'] = 5
            pipeline.metrics['failed_ocr'] = 1
            
            pipeline.save_metrics('test_metrics.json')
            
            output_file = Path(tmpdir) / 'test_metrics.json'
            assert output_file.exists()
            
            # Verify content
            with open(output_file) as f:
                metrics = json.load(f)
                assert metrics['successful_ocr'] == 5
                assert metrics['failed_ocr'] == 1

    def test_results_saving(self):
        """Test saving OCR results to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            results = [
                {'success': True, 'text': 'Document 1', 'page': 1},
                {'success': True, 'text': 'Document 2', 'page': 2},
            ]
            
            pipeline.save_results(results, 'test_results.json')
            
            output_file = Path(tmpdir) / 'test_results.json'
            assert output_file.exists()
            
            # Verify content
            with open(output_file) as f:
                saved_results = json.load(f)
                assert len(saved_results) == 2

    def test_metrics_summary(self):
        """Test getting metrics summary"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            pipeline.metrics['successful_ocr'] = 10
            pipeline.metrics['failed_ocr'] = 2
            pipeline.metrics['total_pages'] = 50
            
            summary = pipeline.get_metrics_summary()
            
            assert summary['documents_processed'] == 10
            assert summary['documents_failed'] == 2
            assert summary['total_pages'] == 50

    @patch('easyocr.Reader')
    def test_process_pdf_file_not_found(self, mock_reader):
        """Test processing non-existent PDF file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            result = pipeline.process_pdf('non_existent.pdf')
            
            assert result['success'] == False
            assert result['error'] == 'File not found'
            assert pipeline.metrics['failed_ocr'] == 1

    def test_create_dummy_image(self):
        """Test creating a dummy image for testing"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='white')
        
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = Path(tmpdir) / 'test.jpg'
            img.save(img_path)
            
            assert img_path.exists()

    def test_extract_images_from_pdf_file_not_found(self):
        """Test extracting images from non-existent PDF"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            images = pipeline.extract_images_from_pdf('non_existent.pdf')
            
            assert images == []


class TestOCRAccuracy:
    """Tests for OCR accuracy measurement"""

    def test_character_accuracy_calculation(self):
        """Test character-level accuracy calculation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            # 9 out of 10 characters match
            ground_truth = "0123456789"
            ocr_text =      "0123456X89"  # X instead of 7
            
            accuracy = pipeline.measure_accuracy(ground_truth, ocr_text)
            
            assert accuracy['char_accuracy'] == 90.0

    def test_word_accuracy_calculation(self):
        """Test word-level accuracy calculation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            ground_truth = "the quick brown fox"
            ocr_text =      "the quick brown dog"  # dog instead of fox
            
            accuracy = pipeline.measure_accuracy(ground_truth, ocr_text)
            
            assert accuracy['word_accuracy'] == 75.0  # 3 out of 4 words match

    def test_empty_text_accuracy(self):
        """Test accuracy with empty text"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = OCRPipeline(output_dir=tmpdir)
            
            accuracy = pipeline.measure_accuracy("", "")
            
            assert accuracy['char_accuracy'] == 100.0  # Empty matches empty


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
