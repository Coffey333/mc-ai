"""
MC AI - ECG Axis Calibrator with OCR
Detects axes and reads scale labels from ECG images
Critical for accurate digitization! 📏
"""

import cv2
import numpy as np
import pytesseract
import re
import logging

logger = logging.getLogger(__name__)

class ECGAxisCalibrator:
    """
    Calibrate ECG image axes using OCR
    MC AI reads the labels to understand the scale! 📏💜
    """
    
    def __init__(self):
        logger.info("MC AI: Axis Calibrator initialized! 📏")
        
        # Standard ECG paper parameters
        self.standard_time_scale = 0.04  # seconds per large box (25 mm/s)
        self.standard_voltage_scale = 0.5  # mV per large box (10 mm/mV)
        self.standard_paper_speed = 25  # mm/s
    
    def detect_axes(self, image):
        """
        Detect X (time) and Y (voltage) axes using edge detection
        """
        logger.info("MC AI: Detecting ECG axes...")
        
        # Find edges
        edges = cv2.Canny(image, 50, 150)
        
        # Detect horizontal and vertical lines
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        h_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, h_kernel)
        v_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, v_kernel)
        
        # Find axis positions
        h_positions = np.where(h_lines > 0)
        v_positions = np.where(v_lines > 0)
        
        if len(h_positions[0]) == 0 or len(v_positions[1]) == 0:
            logger.warning("MC AI: Could not detect axes, using image bounds")
            return {
                'x_axis': image.shape[0] - 50,
                'y_axis': 50,
                'detected': False
            }
        
        # X-axis is typically at the bottom
        x_axis_y = int(np.median(h_positions[0]))
        
        # Y-axis is typically on the left
        y_axis_x = int(np.median(v_positions[1]))
        
        logger.info(f"MC AI: Axes detected at x={x_axis_y}, y={y_axis_x}")
        
        return {
            'x_axis': x_axis_y,
            'y_axis': y_axis_x,
            'detected': True
        }
    
    def extract_text_regions(self, image, axes):
        """
        Extract regions where scale labels are likely to be
        """
        height, width = image.shape[:2]
        
        # X-axis labels (bottom region)
        x_label_region = image[
            max(0, axes['x_axis'] - 50):min(height, axes['x_axis'] + 50),
            :
        ]
        
        # Y-axis labels (left region)
        y_label_region = image[
            :,
            max(0, axes['y_axis'] - 50):min(width, axes['y_axis'] + 50)
        ]
        
        return {
            'x_labels': x_label_region,
            'y_labels': y_label_region
        }
    
    def read_scale_with_ocr(self, image):
        """
        Use OCR to read scale labels from ECG image
        MC AI's reading skills! 👓
        """
        logger.info("MC AI: Reading scale labels with OCR... 👓")
        
        try:
            # Run OCR
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            # Look for common ECG scale patterns
            # Examples: "25 mm/s", "10 mm/mV", "1 mV/cm", "0.5 s/cm"
            
            # Time scale patterns
            time_patterns = [
                r'(\d+\.?\d*)\s*mm/s',
                r'(\d+\.?\d*)\s*s/cm',
                r'(\d+\.?\d*)\s*cm/s',
            ]
            
            # Voltage scale patterns
            voltage_patterns = [
                r'(\d+\.?\d*)\s*mm/mV',
                r'(\d+\.?\d*)\s*mV/cm',
                r'(\d+\.?\d*)\s*mV/mm',
            ]
            
            time_scale = None
            voltage_scale = None
            
            # Extract time scale
            for pattern in time_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    if 'mm/s' in pattern:
                        time_scale = value  # mm/s paper speed
                    elif 's/cm' in pattern:
                        time_scale = 10.0 / value  # convert to mm/s
                    break
            
            # Extract voltage scale
            for pattern in voltage_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    if 'mm/mV' in pattern:
                        voltage_scale = value  # mm/mV
                    elif 'mV/cm' in pattern:
                        voltage_scale = 10.0 / value  # convert to mm/mV
                    elif 'mV/mm' in pattern:
                        voltage_scale = 1.0 / value  # convert to mm/mV
                    break
            
            logger.info(f"MC AI: OCR found - Time: {time_scale} mm/s, Voltage: {voltage_scale} mm/mV")
            
            return {
                'time_scale_mm_per_s': time_scale,
                'voltage_scale_mm_per_mV': voltage_scale,
                'raw_text': text
            }
        
        except Exception as e:
            logger.warning(f"MC AI: OCR failed: {e}")
            return None
    
    def calibrate_from_grid(self, binary_image):
        """
        Calibrate scale by detecting grid pattern
        MC AI counts the boxes! 📐
        FIXED: Separate horizontal and vertical grid spacing
        """
        logger.info("MC AI: Calibrating from grid pattern... 📐")
        
        # Detect grid lines
        edges = cv2.Canny(binary_image, 50, 150)
        
        # Find both horizontal and vertical lines
        h_lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180,
            threshold=100,
            minLineLength=100,
            maxLineGap=5
        )
        
        if h_lines is None or len(h_lines) < 2:
            logger.warning("MC AI: Not enough grid lines detected")
            return None
        
        # Separate horizontal and vertical lines
        h_y_coords = []
        v_x_coords = []
        
        for line in h_lines:
            x1, y1, x2, y2 = line[0]
            
            # Horizontal line (time axis)
            if abs(y2 - y1) < 5 and abs(x2 - x1) > 100:
                h_y_coords.append((y1 + y2) / 2)
            
            # Vertical line (voltage axis)
            elif abs(x2 - x1) < 5 and abs(y2 - y1) > 100:
                v_x_coords.append((x1 + x2) / 2)
        
        h_y_coords = sorted(h_y_coords)
        v_x_coords = sorted(v_x_coords)
        
        if len(h_y_coords) < 2 or len(v_x_coords) < 2:
            logger.warning("MC AI: Not enough grid lines in both directions")
            return None
        
        # Calculate spacing in both directions
        h_spacings = np.diff(h_y_coords)
        v_spacings = np.diff(v_x_coords)
        
        # CRITICAL: Detect whether we have small-box (1mm) or large-box (5mm) spacing
        # If Hough detects ALL grid lines, spacings will be ~1mm
        # If it detects only major lines, spacings will be ~5mm
        
        # Check for multiple spacing clusters (1mm and 5mm)
        v_median = np.median(v_spacings)
        h_median = np.median(h_spacings)
        
        # If we have small spacings, look for the 5× larger ones (large boxes)
        # Count how many spacings are ~5× the median (within 20% tolerance)
        large_v_spacings = v_spacings[np.abs(v_spacings - 5*v_median) < v_median]
        large_h_spacings = h_spacings[np.abs(h_spacings - 5*h_median) < h_median]
        
        # Use large-box spacing if detected, otherwise assume current spacing is large boxes
        if len(large_v_spacings) >= 3:
            vertical_spacing_pixels = np.median(large_v_spacings)
            box_size_v = 5.0  # Large box
        else:
            vertical_spacing_pixels = v_median
            # Check if this looks like small-box spacing (assume ~1-2mm per pixel)
            if vertical_spacing_pixels < 20:
                box_size_v = 1.0  # Small box
            else:
                box_size_v = 5.0  # Large box
        
        if len(large_h_spacings) >= 3:
            horizontal_spacing_pixels = np.median(large_h_spacings)
            box_size_h = 5.0
        else:
            horizontal_spacing_pixels = h_median
            if horizontal_spacing_pixels < 20:
                box_size_h = 1.0
            else:
                box_size_h = 5.0
        
        # Pixels per mm in each direction
        pixels_per_mm_vertical = vertical_spacing_pixels / box_size_v
        pixels_per_mm_horizontal = horizontal_spacing_pixels / box_size_h
        
        # Pixels per physical unit
        pixels_per_mV = pixels_per_mm_vertical * 10  # 10 mm/mV standard
        pixels_per_s = pixels_per_mm_horizontal * 25  # 25 mm/s standard
        
        logger.info(f"MC AI: Detected {box_size_v}mm vertical, {box_size_h}mm horizontal boxes")

        
        logger.info(f"MC AI: Vertical spacing = {vertical_spacing_pixels:.1f} pixels")
        logger.info(f"MC AI: Horizontal spacing = {horizontal_spacing_pixels:.1f} pixels")
        logger.info(f"MC AI: Calibration = {pixels_per_mV:.1f} pixels/mV, {pixels_per_s:.1f} pixels/s")
        
        return {
            'pixels_per_mm_vertical': pixels_per_mm_vertical,
            'pixels_per_mm_horizontal': pixels_per_mm_horizontal,
            'pixels_per_mV': pixels_per_mV,
            'pixels_per_s': pixels_per_s,
            'vertical_grid_spacing': vertical_spacing_pixels,
            'horizontal_grid_spacing': horizontal_spacing_pixels
        }
    
    def full_calibration(self, image, binary_image):
        """
        Complete calibration using both OCR and grid detection
        MC AI's comprehensive approach! 💜
        """
        logger.info("MC AI: Starting full axis calibration! 💜📏")
        
        calibration = {}
        
        # Step 1: Detect axes
        axes = self.detect_axes(binary_image)
        calibration['axes'] = axes
        
        # Step 2: Try OCR
        ocr_result = self.read_scale_with_ocr(image)
        if ocr_result:
            calibration['ocr'] = ocr_result
        
        # Step 3: Grid-based calibration
        grid_cal = self.calibrate_from_grid(binary_image)
        if grid_cal:
            calibration['grid'] = grid_cal
        
        # Step 4: Determine final calibration
        # PRAGMATIC APPROACH: Use OCR if available, validate grid, then fallback
        
        height, width = binary_image.shape[:2]
        
        # Start with OCR if available
        if ocr_result and ocr_result['time_scale_mm_per_s']:
            paper_speed = ocr_result['time_scale_mm_per_s']
            voltage_scale = ocr_result.get('voltage_scale_mm_per_mV', 10)
            logger.info("MC AI: Using OCR calibration")
        else:
            # Standard ECG defaults
            paper_speed = 25  # 25 mm/s
            voltage_scale = 10  # 10 mm/mV
            logger.info("MC AI: Using standard ECG calibration")
        
        # Use grid calibration if it passes sanity checks
        if grid_cal:
            grid_pixels_per_s = grid_cal['pixels_per_s']
            grid_pixels_per_mV = grid_cal['pixels_per_mV']
            
            # Sanity check: Reasonable pixels/second ratio
            expected_pixels_per_s = width / 10  # Assume ~10 seconds
            ratio = grid_pixels_per_s / expected_pixels_per_s
            
            # Accept grid if ratio is reasonable (0.5 - 2.0)
            if 0.5 <= ratio <= 2.0:
                pixels_per_s = grid_pixels_per_s
                pixels_per_mV = grid_pixels_per_mV
                logger.info("MC AI: Grid calibration passed sanity check!")
            else:
                # Grid failed sanity check, use image-based estimation
                pixels_per_s = width / 10  # Assume 10 seconds
                pixels_per_mV = height / 10  # Assume 10 mV range  
                logger.warning(f"MC AI: Grid calibration suspicious (ratio={ratio:.2f}), using fallback")
        else:
            # No grid detected, use image-based estimation
            pixels_per_s = width / 10  # Assume 10 seconds
            pixels_per_mV = height / 10  # Assume 10 mV range
            logger.info("MC AI: Using image-based calibration fallback")
        
        calibration['final'] = {
            'pixels_per_second': pixels_per_s,
            'pixels_per_mV': pixels_per_mV,
            'paper_speed_mm_s': paper_speed,
            'voltage_scale_mm_mV': voltage_scale,
            'x_axis_y': axes.get('x_axis', binary_image.shape[0] // 2),
            'y_axis_x': axes.get('y_axis', 0),
            'image_height': binary_image.shape[0],
            'image_width': binary_image.shape[1]
        }
        
        logger.info("MC AI: Calibration complete! ✨")
        logger.info(f"   {pixels_per_s:.1f} pixels/second")
        logger.info(f"   {pixels_per_mV:.1f} pixels/mV")
        
        return calibration


# Example usage
if __name__ == "__main__":
    calibrator = ECGAxisCalibrator()
    print("MC AI: Axis Calibrator ready! 📏💜")
