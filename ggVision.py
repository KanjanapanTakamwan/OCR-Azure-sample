from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Initialize the client
client = vision_v1.ImageAnnotatorClient()

# Load the image from the local file system
file_name = './image/match_1.jpg'
with open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Perform text detection
response = client.document_text_detection(image=image)
document = response.full_text_annotation
print(document)
# Extract tables
tables = []
for page in document.pages:
    for block in page.blocks:
        if block.block_type == types.Block.BlockType.TABLE:
            table_data = []
            for row in block.rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(' '.join([symbol.text for symbol in cell.symbols]))
                table_data.append(row_data)
            tables.append(table_data)

# Process tables (e.g., convert to CSV, DataFrame)
for i, table in enumerate(tables):
    # You can process each table here (e.g., convert to CSV, DataFrame)
    print(f"Table {i+1}:")
    for row in table:
        print(row)
