import os
import shutil

# Define the path to the directory containing the images
directory_path = 'C:/Users/Usuario/OneDrive/Desktop/asistente-de-compras/dataset/Carrefour'
# Define the path to the new directory for normalized images
normalized_directory_path = os.path.join(directory_path, 'normalized_images')

# Create the new directory if it doesn't exist
os.makedirs(normalized_directory_path, exist_ok=True)

# Function to normalize the product name from the image filename
def normalize_image_name(filename):
    # Split the filename by spaces and take the first part
    base_name = filename.split(' ')[0]
    # Add the file extension back
    extension = os.path.splitext(filename)[1]
    return base_name + extension

# Iterate over all files in the directory
for filename in os.listdir(directory_path):
    # Check if the file is an image
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        # Get the new normalized filename
        new_filename = normalize_image_name(filename)
        # Define the full old and new file paths
        old_file_path = os.path.join(directory_path, filename)
        new_file_path = os.path.join(normalized_directory_path, new_filename)
        # Copy the file to the new directory with the new name
        shutil.copyfile(old_file_path, new_file_path)

print("All image files have been renamed and copied to the new directory.")
