import pydicom
import cv2
import numpy as np
from sklearn.cluster import KMeans

# Read crack extraction image
crack_image = cv2.imread('D:\\jpg1\\zhongtu2\\IM-0017-0041.jpg')  # Replace with your image path

# Read corresponding DICOM image
dcm_path = 'D:\\样品1\\IM-0017-0041.dcm'  # Replace with your DICOM file path
dicom_data = pydicom.dcmread(dcm_path)
dcm_array = dicom_data.pixel_array.astype(np.float32)

# Handle Rescale Slope and Intercept in DICOM
if 'RescaleSlope' in dicom_data and 'RescaleIntercept' in dicom_data:
    slope = dicom_data.RescaleSlope
    intercept = dicom_data.RescaleIntercept
    dcm_array = dcm_array * slope + intercept  # Convert to HU (CT values)

# Ensure dimensions match
assert crack_image.shape[:2] == dcm_array.shape, "Crack extraction image and DICOM shape mismatch"

# Extract strong and weak crack points (coordinates, CT values)
strong_cracks = []  # Store (y, x, CT value)
weak_cracks = []

# ---------- KMeans clustering to separate strong/weak cracks ----------
gray_crack = cv2.cvtColor(crack_image, cv2.COLOR_BGR2GRAY)
crack_mask = gray_crack > 0

coords = np.column_stack(np.where(crack_mask))  # (y, x)
ct_values = np.array([dcm_array[y, x] for y, x in coords]).reshape(-1, 1)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=2, random_state=0)
labels = kmeans.fit_predict(ct_values)
centers = kmeans.cluster_centers_.flatten()

low_ct_label = np.argmin(centers)
high_ct_label = np.argmax(centers)

# Divide cracks into strong/weak based on clustering results
for (y, x), label, ct in zip(coords, labels, ct_values.flatten()):
    if label == low_ct_label:
        strong_cracks.append((y, x, ct))
    else:
        weak_cracks.append((y, x, ct))

# ---------- Mark strong crack pixels as red ----------
for y, x, _ in strong_cracks:
    crack_image[y, x] = (0, 0, 255)  # BGR red

# Optional: Save result image
cv2.imwrite('D:\\jpg1\\zhongtu2\\IM-0017-0041_strong_crack_marked.jpg', crack_image)

# ---------- Output results ----------
print("Strong Crack Points (y, x, CT Value):")
for point in strong_cracks:
    print(point)

print("\nWeak Crack Points (y, x, CT Value):")
for point in weak_cracks:
    print(point)

# Convert to NumPy array, extracting only CT values for statistics
strong_cracks_ct = np.array([item[2] for item in strong_cracks])
weak_cracks_ct = np.array([item[2] for item in weak_cracks])

# Calculate statistical features
print(f"\nStrong Crack - Mean CT: {np.mean(strong_cracks_ct):.2f}, Std: {np.std(strong_cracks_ct):.2f}")
print(f"Weak Crack - Mean CT: {np.mean(weak_cracks_ct):.2f}, Std: {np.std(weak_cracks_ct):.2f}")