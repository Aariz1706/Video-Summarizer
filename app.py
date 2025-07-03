from flask_cors import CORS
from flask import Flask, request, jsonify #Imports fask and other necessities flask- create webservers, request- helps in file uploads and jsaonify- return to frontend in json format
from transcriber import transcribe_audio #This imports transcribe_audio() from transcription and converts audio/video into text
from summarizer import summarize_text #This imports summarize_text() from summarizer and summarizes the text
import os #Used for handling file paths and creating folders.

app = Flask(__name__) #Creates a new flask application and sets up the web server so u can define URL's
CORS(app)
UPLOAD_FOLDER = "uploads" #Sets a folder name (uploads/) where uploaded videos will be saved.
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER #Adds this folder to the flask configuration settings
os.makedirs(UPLOAD_FOLDER , exist_ok = True) #if created does not give error

@app.route('/upload', methods = ["POST"])
def upload_video():
    if "file" not in request.files: #Checks if uploaded request contains a file if it does not it sends a 400 Bad message
        return jsonify({"error": "No file uploaded"}) , 400

    file = request.files["file"] #Retrieves the uploaded file from the request.
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename) #Creates the full path where the folder will be saved 
    file.save(filepath) #Saves the uploaded file in the uploads folder
    try:
        transcription = transcribe_audio(filepath)
        print("Transcription:", transcription[:500])  # log first 500 characters
        if not transcription.strip():
            return jsonify({"error": "Transcription is empty"}), 500

        summary = summarize_text(transcription)
        print("Summary:", summary)

        return jsonify({
            "transcription": transcription,
            "summary": summary
        })

    except Exception as e:
        print(" Backend Error:", e)
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug = True) #Runs the python file when you type in python app.py

