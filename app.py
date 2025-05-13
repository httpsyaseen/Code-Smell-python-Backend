from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import zipfile
import logging
from smell_detector import traverse_zip

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_project():
    logger.debug("Received upload request")
    
    if "file" not in request.files:
        logger.error("No file uploaded in request")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".zip"):
        logger.error("Uploaded file is not a ZIP file: %s", file.filename)
        return jsonify({"error": "File must be a ZIP file"}), 400

    try:
        # Read ZIP file in memory
        logger.debug("Reading ZIP file: %s", file.filename)
        zip_data = io.BytesIO(file.read())
        
        # Verify ZIP file integrity
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            zip_ref.testzip()  # Check for corrupted ZIP
            logger.debug("ZIP file is valid, starting smell detection")
        
        # Analyze smells in the ZIP file
        detected_smells = traverse_zip(zip_data)
        
        # Format results to match requested structure
        results = []
        for filepath, smells in detected_smells.items():
            filename = filepath.split("/")[-1]
            for smell in smells:
                results.append({
                    "fileName": filename,
                    "filePath": filepath,
                    "startLine": smell["startline"],
                    "endLine": smell["endline"],
                    "smellType": smell["codeSmellType"],
                    "code": smell["code"],
                    "category": smell["category"].capitalize(),
                    "weight": smell["weight"]
                })
        
        logger.debug("Smell detection completed, returning %d smells", len(results))
        return jsonify({"total_smells":len(results),"codeSmells": results})
    
    except zipfile.BadZipFile as e:
        logger.error("Invalid ZIP file: %s", str(e))
        return jsonify({"error": "Invalid or corrupted ZIP file"}), 400
    except Exception as e:
        logger.error("Error during smell detection: %s", str(e), exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)