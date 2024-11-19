from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageFilter
import io

app = Flask(__name__)
CORS(app)  

@app.route('/')
def index():
    return jsonify(message="Welcome to Flask image filtering app 🚅")

@app.route('/apply-filter', methods=['POST'])
def apply_filter():
    try:
        if 'image' not in request.files:
            return {"error": "No image uploaded"}, 400
    
        image_file = request.files['image']
        image = Image.open(image_file)
        filtered_image = image.filter(ImageFilter.BLUR)
    
        output = io.BytesIO()
        filtered_image.save(output, format='JPEG')
        output.seek(0)

        return send_file(output, mimetype='image/jpeg', as_attachment=False
                         
      except Exception as e:
        return jsonify(error=str(e)), 500
          
if __name__ == "__main__":
    app.run(debug=True)
