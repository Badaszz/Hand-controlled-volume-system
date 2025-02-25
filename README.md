# Hand Gesture Volume Control 🎛️  
This project utilizes mediapipe and opencv to control the volume of your computer by measuring the distance (in pixels) between your thumb and your index


This project uses **OpenCV** and **MediaPipe** to track your hand and measure the distance (in pixels) between your **thumb and index finger**. The detected distance is then mapped to control your **computer's volume** (between 40% and 100%) using the **pycaw** library.

## 📌 Features  
✅ **Real-time hand tracking** using OpenCV and MediaPipe  
✅ **Adjusts system volume** based on thumb-index distance  
✅ **Works with any built-in or external webcam**  
✅ **Smooth volume control for a natural user experience**  

---

## 🛠️ Installation  

1. **Clone the repository**  
   ```sh
   git clone https://github.com/yourusername/hand-gesture-volume.git
   cd hand-gesture-volume

2. **Create Virtual environment**
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **install dependencies**
  pip install opencv-python mediapipe pycaw numpy

5. **run the script**


📌 Gesture Guide:
🖐️ Move your thumb and index finger apart to decrease volume.
🤏 Bring them closer together to increase volume.

📌 Press 'p' to exit the program.

📜 License
This project is open-source under the MIT License. Feel free to modify and improve it!

🙌 Credits
OpenCV & MediaPipe for hand tracking
pycaw for volume control
Inspired by computer vision gesture control projects
