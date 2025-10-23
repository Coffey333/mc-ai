"""
MC AI - ECG Image Preprocessor
Cleans and prepares ECG images for digitization
"""

import cv2
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ECGImagePreprocessor:
    """
    Handles image preprocessing for ECG digitization
    MC AI's first step: Clean the image! 💜
    """
    
    def __init__(self, target_dpi=300):
        self.target_dpi = target_dpi
        logger.info("MC AI ECG Preprocessor initialized! 💜")
    
    def load_image(self, image_path):
        """Load image from file or PIL Image"""
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
        else:
            image = np.array(image_path)
        
        # Convert to RGB if needed
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        
        return image
    
    def denoise(self, image):
        """Remove noise while preserving ECG signal"""
        logger.info("MC AI: Removing noise from ECG image...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply bilateral filter (preserves edges)
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        return denoised
    
    def enhance_contrast(self, image):
        """Enhance contrast to make waveform stand out"""
        logger.info("MC AI: Enhancing contrast...")
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(image)
        
        return enhanced
    
    def binarize(self, image, method='adaptive'):
        """Convert to binary (black/white) image"""
        logger.info(f"MC AI: Binarizing image using {method} method...")
        
        if method == 'otsu':
            _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif method == 'adaptive':
            binary = cv2.adaptiveThreshold(
                image, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
        else:
            _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        
        return binary
    
    def remove_grid(self, image):
        """
        Remove background grid while preserving ECG waveform
        MC AI's cymatic pattern detection helps here!
        """
        logger.info("MC AI: Detecting and removing grid pattern...")
        
        # Detect lines using Hough Transform
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180,
            threshold=100,
            minLineLength=50,
            maxLineGap=10
        )
        
        # Create mask of grid lines
        grid_mask = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Only mark perfectly horizontal/vertical lines as grid
                if abs(x1 - x2) < 5 or abs(y1 - y2) < 5:
                    cv2.line(grid_mask, (x1, y1), (x2, y2), (255,), 2)
        
        # Remove grid from image
        no_grid = cv2.bitwise_and(image, cv2.bitwise_not(grid_mask))
        
        return no_grid
    
    def preprocess_pipeline(self, image_path, remove_grid=True):
        """
        Full preprocessing pipeline
        Returns clean image ready for digitization
        """
        logger.info("MC AI: Starting full preprocessing pipeline! 🎨")
        
        # Step 1: Load
        image = self.load_image(image_path)
        
        # Step 2: Denoise
        denoised = self.denoise(image)
        
        # Step 3: Enhance
        enhanced = self.enhance_contrast(denoised)
        
        # Step 4: Binarize
        binary = self.binarize(enhanced, method='adaptive')
        
        # Step 5: Remove grid (optional)
        if remove_grid:
            clean = self.remove_grid(binary)
        else:
            clean = binary
        
        logger.info("MC AI: Preprocessing complete! ✨")
        return clean, binary, enhanced, denoised


# Example usage
if __name__ == "__main__":
    preprocessor = ECGImagePreprocessor()
    
    # Process an ECG image
    # clean_image, binary, enhanced, denoised = preprocessor.preprocess_pipeline(
    #     "ecg_sample.jpg",
    #     remove_grid=True
    # )
    
    print("MC AI: ECG Image Preprocessor ready for competition! 💜")
