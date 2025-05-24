################################ Single DICOM Data Processing ##################################################
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pydicom
from skimage import exposure
from skimage import io
import pydicom

# CLAHE (Contrast Limited Adaptive Histogram Equalization) function
def apply_clahe(image, clip_limit=3.0, tile_grid_size=(3,3)):
    """
    Apply CLAHE to enhance contrast
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)

# Gamma transformation function
def apply_gamma_transform(image_path, gamma):
    # Read image
    image = image_path

    if image is None:
        print(f"Error: Unable to open image at {image_path}")
        return

    # Normalize to [0, 1] range
    normalized_image = image / 255.0

    # Apply gamma transformation
    gamma_corrected = np.power(normalized_image, gamma)

    # Normalize gamma-corrected image to [0, 255] range and convert to uint8
    gamma_corrected = cv2.normalize(gamma_corrected, None, 0, 255, cv2.NORM_MINMAX)
    gamma_corrected = np.uint8(gamma_corrected)
    return gamma_corrected

# Read DICOM file and convert to grayscale
dcm_file = 'D:\样品1\IM-0017-0043.dcm'
ds = pydicom.dcmread(dcm_file)  # Read DICOM file using pydicom
image = ds.pixel_array
image = np.clip(image, 0, None)  # Clip negative values to 0
image = np.uint16(image)  # Convert to uint16
print(image.dtype)
print(image.shape)

# Display original image
plt.imshow(image)
plt.colorbar()  # Show colorbar
plt.axis('off')  # Hide axes
plt.show()

# Apply histogram equalization to enhance contrast
image2 = apply_clahe(image, clip_limit=2, tile_grid_size=(2,2)) # (15,15) sigma = 0.72

# Sharpen image using custom kernel
kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]])

# Apply custom convolution kernel
sharpened_image_custom = cv2.filter2D(image2, -1, kernel)

# Apply gamma transformation to increase brightness and contrast
gamma = 2 #0.86
image3 = apply_gamma_transform(sharpened_image_custom, gamma)

# Apply bilateral filtering
bilateral_filtered = cv2.bilateralFilter(image3, 2, 100, 100)

# Gabor filter parameters
ksize = 35  # Kernel size
sigma = 0.82 # Standard deviation of Gaussian function - larger values remove more noise
theta = 0.3 # Rotation angle of the filter kernel - detects edges in different orientations
lambda_ = 7 # Wavelength - smaller values capture high-frequency details
gamma = 1.12 # Spatial aspect ratio - smaller values detect narrow edges

# Generate Gabor filter kernel
kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambda_, gamma, 0, ktype=cv2.CV_32F)
# Apply filtering
res = cv2.filter2D(bilateral_filtered, cv2.CV_8UC3, kernel)
plt.show()
plt.title("Gamma Enhanced")
plt.imshow(res, cmap='gray')
plt.axis('off')

# Remove injection holes using Hough Circle Transform
circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, dp=1, minDist=30, param1=50, param2=30, minRadius=30, maxRadius=40)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    scale_factor = 1.3 # Scaling factor
    for (x, y, r) in circles:
         adjusted_r = int(r * scale_factor)
         cv2.circle(res, (x, y), adjusted_r, (255), thickness=-1)

# Save processed image
target_folder = r'D:\jpg1\quzao'
cv2.imwrite(os.path.join(target_folder, '1.jpg'), res)
# res[res < 100] =1
# res1 = cv2.bitwise_not(res)

# Display original and processed images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Sharpened Image (Custom Kernel)')
plt.imshow(res, cmap='gray')
plt.axis('off')
plt.show()

################################# Batch DICOM Data Processing ################################################
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pydicom
from skimage import exposure
from skimage import io

# Apply CLAHE for contrast enhancement
def apply_clahe(image, clip_limit=3.0, tile_grid_size=(3,3)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)

# Apply gamma transformation
def apply_gamma_transform(image, gamma):
    # Normalize to [0, 1] range
    normalized_image = image / 255.0

    # Apply gamma transformation
    gamma_corrected = np.power(normalized_image, gamma)

    # Normalize gamma-corrected image to [0, 255] range and convert to uint8
    gamma_corrected = cv2.normalize(gamma_corrected, None, 0, 255, cv2.NORM_MINMAX)
    gamma_corrected = np.uint8(gamma_corrected)

    return gamma_corrected

# Process all DICOM files in a folder
folder_path = 'D:\\sample4'  # Input DICOM folder
new_folder_path = 'D:\\sample4chuli\\yuchuli'  # Output folder for processed images

# Create output folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

# Process each DICOM file in the folder
for filename in sorted(os.listdir(folder_path)):
    # Only process DICOM files
        dcm_file = os.path.join(folder_path, filename)
        ds = pydicom.dcmread(dcm_file)  # Read DICOM file
        image = ds.pixel_array  # Get pixel data

        # Process image: ensure pixel values are in correct range
        image = np.clip(image, 0, None)
        image = np.uint16(image)

        # Apply CLAHE for contrast enhancement
        image2 = apply_clahe(image, clip_limit=2, tile_grid_size=(2,2))

        # Sharpen image using custom kernel
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpened_image_custom = cv2.filter2D(image2, -1, kernel)

        # Apply gamma transformation
        gamma = 0.98 # Adjust gamma value
        image3 = apply_gamma_transform(sharpened_image_custom, gamma)

        # Apply bilateral filtering
        bilateral_filtered = cv2.bilateralFilter(image3, 2, 100, 100)

        # Gabor filter parameters
        ksize = 35  # Kernel size
        sigma = 0.45
        theta = 0.3
        lambda_ = 7
        gamma_gabor = 1.12

        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambda_, gamma_gabor, 0, ktype=cv2.CV_32F)
        res = cv2.filter2D(bilateral_filtered, cv2.CV_8UC3, kernel)

        # Remove injection holes using Hough Circle Transform
        circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, dp=1, minDist=30, param1=50, param2=30, minRadius=30, maxRadius=40)
        if circles is not None:
               circles = np.round(circles[0, :]).astype("int")
               scale_factor = 1.3 # Scaling factor
               for (x, y, r) in circles:
                 adjusted_r = int(r * scale_factor)
                 cv2.circle(res, (x, y), adjusted_r, (255), thickness=-1)

        # Save processed image
        # res[res < 200] = 1
    #   #res1 = cv2.bitwise_not(res)
    #   #new_image_path = os.path.join(new_folder_path, filename.replace('.dcm', '.jpg'))
        new_image_path = os.path.join(new_folder_path, filename+'.jpg')
        cv2.imwrite(new_image_path, res)
        print(f"Saved processed image to: {new_image_path}")