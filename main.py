from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "ccrop":
            height, width = img.shape[:2]
            cropped_image = img[(int)(height/2)-150:(int)(height/2)+150, (int)(width/2)-150:(int)(width/2)+150]
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, cropped_image)
            return newFilename
        case "cresize1":
            imgResized = cv2.resize(img, (350, 350))
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgResized)
            return newFilename
        case "cresize2":
            imgResized = cv2.resize(img, (1000, 1000))
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgResized)
            return newFilename
        case "crotate1":
            imgRotated1 = cv2.flip(img, 0)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgRotated1)
            return newFilename
        case "crotate2":
            imgRotated2 = cv2.flip(img, 1)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgRotated2)
            return newFilename
        case "cgblur":
            gaussian = cv2.GaussianBlur(img, (7, 7), 0)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, gaussian)
            return newFilename
        case "cmblur":
            median = cv2.medianBlur(img, 5)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, median)
            return newFilename
        case "cbblur":
            bilateral = cv2.bilateralFilter(img, 9, 75, 75)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, bilateral)
            return newFilename
        case "cborder":
            border = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = 0)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, border)
            return newFilename
    pass
        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation") 
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"<strong>Success! </strong>Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
        else:
            flash("Allowed image types are png, jpg, jpeg, gif")
            return render_template("index.html")

    return render_template("index.html")


app.run(debug = True, port = 5001)