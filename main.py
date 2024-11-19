from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter
import io
import logging

# Enable Flask logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/apply-filter', methods=['POST'])
def apply_filter():
    try:
        # Ensure an image was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Apply a filter (for example, a blur filter)
        filtered_image = image.filter(ImageFilter.BLUR)
        
        # Save the filtered image to a BytesIO object to return it as a response
        output = io.BytesIO()
        filtered_image.save(output, format='JPEG')
        output.seek(0)
        
        return send_file(output, mimetype='image/jpeg', as_attachment=False)
    
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")  # Log the error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
