import pandas as pd

# Load the CSV file to examine its content
file_path = 'C:/Users/Usuario/OneDrive/Desktop/asistente-de-compras/dataset/VerdurasporSupermercado.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Define a function to normalize product names
def normalize_product_name(product_name):
    # Split the name by the first space and take the first part
    return product_name.split(' ')[0]

# Apply the normalization function to the 'Producto' column
data['Producto'] = data['Producto'].apply(normalize_product_name)

# Display the updated dataframe
data.head()

# Save the updated dataframe to a new CSV file
normalized_file_path = 'C:/Users/Usuario/OneDrive/Desktop/asistente-de-compras/dataset/VerdurasNormalizadas.csv'
data.to_csv(normalized_file_path, index=False)

normalized_file_path
