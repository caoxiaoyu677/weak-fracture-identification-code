# Batch Slice Processing
import matplotlib.pyplot as plt
from skimage import io
import cv2
import numpy as np
from skimage.morphology import thin
import os

folder_path = 'D:\\sample4chuli\\yuchuli\\Intensities'
new_folder_path = 'D:\\sample4chuli\\yuchuli\\zhongtu2'

for filename in sorted(os.listdir(folder_path)):
    dcm_path = os.path.join(folder_path, filename)
    Image = cv2.imread(dcm_path)

    # Create rectangular kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Perform closing operation
    closed = cv2.morphologyEx(Image, cv2.MORPH_CLOSE, kernel)

    # Threshold to create binary image
    _, binary = cv2.threshold(closed, 127, 255, cv2.THRESH_BINARY)
    gray_image = cv2.cvtColor(binary, cv2.COLOR_BGR2GRAY)

    # Find connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(gray_image, connectivity=8)

    # Create blank image for filtered result
    filtered_image = np.zeros_like(gray_image)

    # Set minimum size threshold for connected components
    min_size = 2500  # Adjust this value as needed

    # Filter components based on size
    for i in range(1, num_labels):  # Start from 1 to skip background
        x, y, w, h, area = stats[i]
        aspect_ratio = w / float(h)
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            filtered_image[labels == i] = 255

    # Create circular mask to remove center hole
    Infor = [512, 512]
    MaskHole = np.ones((Infor[0], Infor[1]))
    for i in range(Infor[0]):
        for j in range(Infor[1]):
            if (i - 249) ** 2 + (j - 252) ** 2 >= 220 ** 2:
                MaskHole[i][j] = 0
    res = np.multiply(filtered_image, MaskHole)

    # Perform additional morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(filtered_image, cv2.MORPH_CLOSE, kernel)
    closed = cv2.medianBlur(closed, 11)

    # Apply thinning algorithm
    thinned = thin(closed // 255)
    thinned = (thinned * 255).astype(np.uint8)

    # Reapply circular mask
    Infor = [512, 512]
    MaskHole = np.ones((Infor[0], Infor[1]))
    for i in range(Infor[0]):
        for j in range(Infor[1]):
            if (i - 249) ** 2 + (j - 252) ** 2 >= 220 ** 2:
                MaskHole[i][j] = 0
    res = np.multiply(closed, MaskHole)

    # Save processed image
    new_image_path = os.path.join(new_folder_path, filename)
    cv2.imwrite(new_image_path, res)

########## Single Slice Processing ############################################################################
#######################################################################################
Image = cv2.imread(r"D:\jpg1\quzao\Intensities\0000000000000001.jpg")

# Create kernel for morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
# Perform closing operation
closed = cv2.morphologyEx(Image, cv2.MORPH_CLOSE, kernel)

# Threshold and convert to grayscale
_, binary = cv2.threshold(closed, 127, 255, cv2.THRESH_BINARY)
gray_image = cv2.cvtColor(binary, cv2.COLOR_BGR2GRAY)

# Additional morphological closing
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
closed = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

# Apply circular mask
Infor = [512, 512]
MaskHole = np.ones((Infor[0], Infor[1]))
for i in range(Infor[0]):
    for j in range(Infor[1]):
        if (i - 252) ** 2 + (j - 252) ** 2 >= 220 ** 2:
            MaskHole[i][j] = 0
res = np.multiply(closed, MaskHole)
plt.imshow(res, cmap='gray')
plt.show()

# Find connected components
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed, connectivity=8)

# Create blank image for filtered result
filtered_image = np.zeros_like(gray_image)

# Set minimum size threshold for connected components
min_size = 1116  # Adjust this value as needed

# Filter components based on size
for i in range(1, num_labels):  # Start from 1 to skip background
    x, y, w, h, area = stats[i]
    aspect_ratio = w / float(h)
    if stats[i, cv2.CC_STAT_AREA] >= min_size:
        filtered_image[labels == i] = 255

plt.imshow(filtered_image, cmap='gray')
plt.axis('off')
plt.show()

# Perform additional morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
closed = cv2.morphologyEx(filtered_image, cv2.MORPH_CLOSE, kernel)

plt.subplot(1, 3, 1)
plt.imshow(closed, cmap='gray')
plt.title('filter')

# Apply median blur
closed = cv2.medianBlur(closed, 11)

plt.subplot(1, 3, 2)
plt.imshow(closed, cmap='gray')
plt.title('filter')

# Apply thinning algorithm
thinned = thin(closed // 255)
thinned = (thinned * 255).astype(np.uint8)

# Reapply circular mask
Infor = [512, 512]
MaskHole = np.ones((Infor[0], Infor[1]))
for i in range(Infor[0]):
    for j in range(Infor[1]):
        if (i - 248) ** 2 + (j - 252) ** 2 >= 200 ** 2:
            MaskHole[i][j] = 0
res = np.multiply(thinned, MaskHole)
target_folder = r'D:\jpg1\zhongtu'

plt.subplot(1, 3, 3)
plt.imshow(res, cmap='gray')
plt.title('filter')
plt.show()

plt.imshow(res, cmap='gray')
plt.axis('off')
plt.show()