from flask import Flask, render_template, url_for, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path to the folder containing photos
PHOTO_FOLDER = os.path.join('static', 'photos')

# Ensure the photos folder exists
if not os.path.exists(PHOTO_FOLDER):
    os.makedirs(PHOTO_FOLDER)


@app.route('/')
def index():
    # List all photos in the folder
    photos = os.listdir(PHOTO_FOLDER)
    photos = [url_for('static', filename=f'photos/{photo}') for photo in photos]
    return render_template('index.html', photos=photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the 'photo' file is in the request
        if 'photo' not in request.files:
            return "No file part", 400
        
        photo = request.files['photo']

        if photo.filename == '':
            return "No selected file", 400

        # Secure the filename
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(PHOTO_FOLDER, filename))

        # After upload, redirect to home page
        return redirect('/')
    
    # If it's a GET request, render the upload form
    return render_template('upload.html')

# handling deleting request
@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    
        # Construct the path to the image to be deleted
        photo_path = os.path.join(PHOTO_FOLDER, filename)
        
        # Check if the image exists and delete it
        if os.path.exists(photo_path):
            os.remove(photo_path)
        
        # Redirect to the homepage to show the updated list of images
        return redirect(url_for('index'))
    





"""@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'photo' not in request.files:
        return "No file part", 400
    
    photo = request.files['photo']

    if photo.filename == '':
        return "No selected file", 400

    print(f"File selected: {photo.filename}")

     # Secure the filename
    filename = secure_filename(photo.filename)
    # Save the file to the photos folder
    photo.save(os.path.join(PHOTO_FOLDER, filename))

     # Redirect to home page to show the new photo
    return render_template('upload.html')"""

if __name__ == '__main__':
    app.run(debug=True, port=8000)



