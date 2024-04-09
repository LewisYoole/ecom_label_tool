import base64
import requests
import requests
from PIL import Image
from io import BytesIO
import ast

def resize_image_at_url(image_url, output_filename):
    # Download the image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    # Resize the image
    new_size = (266, 354)
    resized_image = image.resize(new_size)
    
    # Saving the resized image at 72 DPI
    # PIL saves images at 72 DPI by default, so we don't need to explicitly set it here
    resized_image.save(output_filename)

def extract_choices(json_data):
    # Define the key where the target data is located
    target_key = 'choices'
    
    # Initialize an empty list to store the cleaned data
    cleaned_data = []
    
    # Check if the target key exists in the JSON data
    if target_key in json_data:
        # Extract the content from each choice's message
        for choice in json_data[target_key]:
            content = choice['message']['content']
            # Strip the markdown code block syntax and evaluate the string as a Python object
            try:
                content_cleaned = content.strip('```python\n').rstrip('\n```')
                python_dict = ast.literal_eval(content_cleaned)
                cleaned_data.extend(python_dict)
            except ValueError as e:
                # Handle possible evaluation errors
                print(f"Error evaluating content: {e}")
    
    # Return the cleaned and extracted data as a list of dictionaries
    return cleaned_data

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def open_api_image_reader(img):
  # OpenAI API Key
  with open('openai_api_key.txt', 'r') as file:
      # Read the contents of the file
      file_contents = file.read()

  api_key = file_contents


  #image to download, later replace with DB Query
  image_url = img
  output_filename = "current_image/img.jpg"

  #resize to keep tokens cost low, adjust sizing if labels come back aids
  resize_image_at_url(image_url, output_filename)


  image_path = "current_image/img.jpg"

  # Getting the base64 string
  base64_image = encode_image(image_path)

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Given the following product image, analyze its attributes with a fashion-centric perspective. Identify and return a Python list of 25 dictionary that describe key characteristics of the product, such as the gender of the model (if applicable), type of garment, color, and any other relevant features. Focus on extracting detailed attributes to provide a comprehensive understanding of the product's appearance and style. Ensure the response is direct and consists only of the Python list, omitting any introductory or conversational elements."

          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 1000
  }


  #return json data
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


  #clean json data and only returns labels removing open ai noise 

  #print(response.json())
  product_labels = extract_choices(response.json())

  return product_labels