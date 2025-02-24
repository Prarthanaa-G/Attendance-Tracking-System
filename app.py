import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import sqlite3
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)

# Load the saved model in TensorFlow format
model = tf.keras.models.load_model('trained_model11.h5')

# Database setup
DB_NAME = 'attendance.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     name TEXT,
    #                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    #                 )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
                )''')

    conn.commit()
    conn.close()
    
    
def convert_to_ist(utc_time):
    utc_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
    ist_zone = pytz.timezone('Asia/Kolkata')
    ist_dt = utc_time.replace(tzinfo=pytz.utc).astimezone(ist_zone)
    return ist_dt.strftime('%Y-%m-%d %H:%M:%S')


       
    
def alter_speed(frames, factor):
    """Alter the speed of video frames."""
    if factor > 1:  # Speed up
        return frames[::int(factor)]
    elif factor < 1:  # Slow down
        return [frame for frame in frames for _ in range(int(1 / factor))]
    return frames

def extract_keypoints_from_video(video_path):
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    keypoints_sequence = []

    cap = cv2.VideoCapture(video_path)
    frame_sequence = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_sequence.append(frame_rgb)

    cap.release()

    # Apply speed alteration (factor = 1.5 for consistency with preprocessing)
    altered_frames = alter_speed(frame_sequence, factor=1.5)

    # Augment frames: original + flip
    augmented_frames = []
    for frame in altered_frames:
        augmented_frames.append(frame)  # Original
        augmented_frames.append(cv2.flip(frame, 1))  # Flip

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in augmented_frames:
            result = pose.process(frame)
            if result.pose_landmarks:
                keypoints = [
                    [lm.x, lm.y, lm.z]
                    for lm in result.pose_landmarks.landmark
                ]
                keypoints_sequence.append(np.array(keypoints).flatten())
            else:
                keypoints_sequence.append(np.zeros(99))

    # Pad or truncate the sequence to fit the model's input shape
    max_sequence_length = 350
    keypoints_sequence = np.array(keypoints_sequence)

    if keypoints_sequence.shape[0] < max_sequence_length:
        padding = np.zeros((max_sequence_length - keypoints_sequence.shape[0], 99))
        keypoints_sequence = np.vstack([keypoints_sequence, padding])
    else:
        keypoints_sequence = keypoints_sequence[:max_sequence_length, :]

    return np.expand_dims(keypoints_sequence, axis=0)  # Shape: (1, 350, 99)

 

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file uploaded.'}), 400

        video = request.files['video']
        os.makedirs('uploads', exist_ok=True)
        video_path = os.path.join('uploads', video.filename)
        video.save(video_path)

        # Extract keypoints
        keypoints = extract_keypoints_from_video(video_path)

        print("Keypoints shape before prediction:", keypoints.shape)  # Debugging
        print("Sample keypoints:", keypoints[0][:5])  # Inspect data consistency

        # Normalize keypoints as done during training
        keypoints = keypoints / np.max(keypoints)

        # Predict
        prediction = model.predict(keypoints)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence = float(np.max(prediction))

        # Map prediction to name
        class_mapping = {0: 'Prarthana', 1: 'Preksha', 2: 'Rashmi', 3: 'Shilpa'}
        threshold = 0.98  # Set a confidence threshold
        name = class_mapping.get(predicted_class, 'Unknown') if confidence >= threshold else 'Unknown'
        print(f"Prediction array: {prediction}")  # Debugging predictions
        print(f"Predicted class index: {predicted_class}, Name: {name}, Confidence: {confidence}")


        # Save to database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO attendance (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()

        return jsonify({'name': name, 'confidence': confidence})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500




@app.route('/view_attendance')
def view_attendance_page():
    return render_template('attendance.html')





# @app.route('/attendance', methods=['GET'])
# def view_attendance():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, name, timestamp FROM attendance ORDER BY timestamp DESC')
#     records = cursor.fetchall()
#     conn.close()

#     # Convert records to a list of dictionaries
#     attendance_list = [{'id': r[0], 'name': r[1], 'timestamp': r[2]} for r in records]
#     return jsonify(attendance_list)




@app.route('/attendance', methods=['GET'])
def view_attendance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, timestamp FROM attendance ORDER BY timestamp DESC')
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries with IST timestamp
    attendance_list = [{'id': r[0], 'name': r[1], 'timestamp': convert_to_ist(r[2])} for r in records]
    return jsonify(attendance_list)




if __name__ == '__main__':
    init_db()
    app.run(debug=True)
