from flask import Flask, request, jsonify, send_file, abort
from docx import Document
import os

app = Flask(__name__)

# file we always write to
FILE_NAME = "Summary of Sale of Goodwill Act,1930.docx"

@app.route("/write_word", methods=["POST"])
def write_word():
    data = request.get_json(force=True)
    content = data.get("content", "")

    if os.path.exists(FILE_NAME):
        doc = Document(FILE_NAME)
    else:
        doc = Document()

    for line in content.split("\n"):
        line = line.strip()
        if line:
            doc.add_paragraph(line)

    doc.save(FILE_NAME)
    return jsonify({
        "message": f"Written to {FILE_NAME}",
        "content_lines": len(content.splitlines())
    })

@app.route("/download_word", methods=["GET"])
def download_word():
    if os.path.exists(FILE_NAME):
        return send_file(FILE_NAME, as_attachment=True, download_name=FILE_NAME)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
