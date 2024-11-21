from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image, ImageFilter

app = Flask(__name__)
CORS(app, origins=["https://image-filter-inf440.netlify.app"])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")  
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.route('/apply-filters', methods=['POST'])
def apply_filters():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']

        if not allowed_file(image_file.filename):
            return jsonify({"error": "Invalid file type. Only PNG and JPEG are allowed."}), 400

        image = Image.open(image_file)

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        filters = {
            "blur": image.filter(ImageFilter.BLUR),
            "sharpen": image.filter(ImageFilter.SHARPEN),
            "contour": image.filter(ImageFilter.CONTOUR),
            "edge_enhance": image.filter(ImageFilter.EDGE_ENHANCE),
            "emboss": image.filter(ImageFilter.EMBOSS),
            "detail": image.filter(ImageFilter.DETAIL)
        }

        image_base64 = {}
        for filter_name, filtered_image in filters.items():
            # Convert the filtered image to base64
            image_base64[filter_name] = encode_image_to_base64(filtered_image)

        return jsonify({"images": image_base64})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
