from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import io
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/apply-filters', methods=['POST'])
def apply_filters():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        image = Image.open(image_file)
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        filters = {
            "blur": image.filter(ImageFilter.BLUR),
            "sharpen": image.filter(ImageFilter.SHARPEN),
            "contour": image.filter(ImageFilter.CONTOUR),
            "edge_enhance": image.filter(ImageFilter.EDGE_ENHANCE),
            "grayscale": image.convert("L")  # Convert to grayscale
        }

        image_urls = []
        for filter_name, filtered_image in filters.items():
            output = io.BytesIO()
            filtered_image.save(output, format='JPEG')
            output.seek(0)
            
            img_url = f"data:image/jpeg;base64,{base64.b64encode(output.getvalue()).decode()}"
            image_urls.append({filter_name: img_url})
        
        return jsonify({"images": image_urls})
    
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")  # Log the error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
