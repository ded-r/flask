from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import io
import logging

# Enable Flask logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/apply-filter', methods=['POST'])
def apply_filter():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        image = Image.open(image_file)
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        filtered_image = image.filter(ImageFilter.BLUR)
        
        output = io.BytesIO()
        filtered_image.save(output, format='JPEG')
        output.seek(0)
        
        return send_file(output, mimetype='image/jpeg', as_attachment=False)
    
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")  # Log the error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
