from flask import Flask, request, jsonify
from flasgger import Swagger
import shutil
import os

from CW_05_DSA import podpisz_plik, zweryfikuj_plik

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def root():
    """
    Root endpoint
    ---
    responses:
      200:
        description: Returns a greeting message
        examples:
          application/json: {"message": "Hello World"}
    """
    return jsonify({"message": "Hello World"})
  
@app.route("/verifyfile/", methods=["POST"])
def verify_file():
    """
    Verify a file
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to verify
      - name: key_number
        in: formData
        type: string
        required: true
        description: The key number to use for verification
      - name: signature_number_1
        in: formData
        type: string
        required: true
        description: The signature number to use for verification
      - name: signature_number_2
        in: formData
        type: string
        required: true
        description: The signature number to use for verification
      - name: p
        in: formData
        type: string
        required: true
        description: p
      - name: q
        in: formData
        type: string
        required: true
        description: q
      - name: g
        in: formData
        type: string
        required: true
        description: g
    responses:
      200:
        description: File uploaded and processed successfully
        schema:
          type: object
          properties:
            filename:
              type: string
            location:
              type: string
            key_number:
              type: string
            signature_number:
              type: string
            signature:
              type: string
            is_valid:
              type: boolean
            L:
              type: integer
            p:
              type: string
            q:
              type: string
            g:
              type: string
            y:
              type: string
            file_path:
              type: string
      400:
        description: Invalid request
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    if 'key_number' not in request.form or 'signature_number_1' not in request.form or 'signature_number_2' not in request.form:
        return jsonify({"error": "Key number and signature number are required"}), 400
    
    key_number = str(request.form['key_number'])
    signature_number1 = str(request.form['signature_number_1'])
    signature_number2 = str(request.form['signature_number_2'])
    
    p = str(request.form['p'])
    q = str(request.form['q'])
    g = str(request.form['g'])
    
    signature_number = [int(signature_number1), int(signature_number2)]
    
    file_location = os.path.join("./uploaded_files", file.filename)
    
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.stream, buffer)
    
    L, p, q, g, y, file_path, signature, is_valid = zweryfikuj_plik(file_location, int(key_number), signature_number, int(p), int(q), int(g))
    
    return jsonify({
        "filename": file.filename,
        "location": file_location,
        "key_number": key_number,
        "signature_number": signature_number,
        "signature": str(signature),
        "is_valid": is_valid,
        "L": L,
        "p": str(p),
        "q": str(q),
        "g": str(g),
        "y": str(y),
        "file_path": file_path
    })

@app.route("/signfile/", methods=["POST"])
def create_upload_file():
    """
    Upload a file
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to upload
    responses:
      200:
        description: File uploaded and processed successfully
        schema:
          type: object
          properties:
            filename:
              type: string
            location:
              type: string
            signature:
              type: string
            is_valid:
              type: boolean
            L:
              type: integer
            p:
              type: string
            q:
              type: string
            g:
              type: string
            x:
              type: string
            y:
              type: string
            file_path:
              type: string
      400:
        description: Invalid request
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    file_location = os.path.join("./uploaded_files", file.filename)
    
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.stream, buffer)
    
    L, p, q, g, x, y, file_path, signature, is_valid = podpisz_plik(file_location)
    
    return {
        "filename": file.filename,
        "location": file_location,
        "signature": str(signature),
        "is_valid": is_valid,
        "L": str(L),
        "p": str(p),
        "q": str(q),
        "g": str(g),
        "x": str(x),
        "y": str(y),
        "file_path": file_path
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

'''
{
  "L": "1024",
  "file_path": "./uploaded_files\\example.txt",
  "filename": "example.txt",
  "g": "135442647135396322370475004948448112008352759874771699774571454371889949477061649842587488416417921718998348679401104830209281154775661910978223454745541723366772030806128784809691775141741203428878905581826159289075694777819928878447219904625025143405286924385045815773939584481998679191028792101544930583359",
  "is_valid": true,
  "location": "./uploaded_files\\example.txt",
  "p": "160496708107486818681246241008756879202064762296238160223373976135023973743481982260582587454432822754548999427424426725001652935319645043941082122455750221781939544176771281701957022237198219781317746058175658859829681842209789260691446904940928777714998071394485448529131884711005868030984985886624230081109",
  "q": "1405862954209133182068420846754960454055113581751",
  "signature": "(865616887865175328342287077260453179800314138548, 722385111173094230587353461418265230167712111225)",
  "x": "690485773421644452434358104699816928684381795372",
  "y": "20451733680646072379164328622406886520121261505179596958799593209168984111508264658433964892857716614152181870316511185783853545334955178694307579404654283823261001627470110899358295072700945410030405220657963528834862966934034849234280731212262608091322692603053667424108280510293461831094224895066922874270"
}
'''