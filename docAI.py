
from google.cloud import documentai_v1 as documentai

def extract_table_data(image_path):
  # Authenticate with GCP project and service account
  client = documentai.DocumentAIProcessorServiceClient()

  # Read image file
  with open(image_path, "rb") as image_file:
    content = image_file.read()

  # Set document type and processor
  document = documentai.types.RawDocument(
      content=content, mime_type="image/jpeg"  # Adjust for image format
  )
  processors = [documentai.types.Processor(type_=documentai.enums.Processor.Type.FORM_PARSER)]

  # Make request to Document AI
  request = documentai.types.ProcessRequest(
      parent=f"projects/certain-axis-418908/locations/us",
      raw_documents=[document],
      processors=processors,
  )
  response = client.process_request(request=request)

  # Extract table data from response
  tables = []
  for page in response.documents:
    for form_field in page.form_fields:
      if form_field.field_type == documentai.enums.FieldType.TABLE:
        table_data = []
        for row in form_field.table_value.rows:
          row_data = []
          for cell in row.cells:
            row_data.append(cell.text)
          table_data.append(row_data)
        tables.append(table_data)

  # Return extracted tables
  return tables

# Example usage
image_path = "./image/match_1.jpg"
tables = extract_table_data(image_path)

# Process and use the extracted tables (tables is a list of lists)
