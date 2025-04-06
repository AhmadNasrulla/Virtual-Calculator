###🖐️ Virtual Calculator - Hand Gesture Controlled
This is a Virtual Calculator built using OpenCV, cvzone, and Mediapipe, controlled by hand gestures using your webcam.

📌 Features:

Hover effect when index finger is over a button

"Pinch" gesture (index + middle finger) to click

Virtual calculator layout rendered via OpenCV

Clear (CC) and Erase (C) buttons

Real-time input using hand gestures

📦 Requirements
Python version: 3.7 – 3.10 recommended

🔧 Installation Steps
Clone the repository

bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/virtual-calculator.git
cd virtual-calculator
Create a virtual environment

bash
Copy
Edit
python -m venv venv
Activate the virtual environment

On Windows:

bash
Copy
Edit
venv\Scripts\activate
On Mac/Linux:

bash
Copy
Edit
source venv/bin/activate
Install required libraries

bash
Copy
Edit
pip install -r requirements.txt
If you don’t have a requirements.txt, create one using:

bash
Copy
Edit
pip install opencv-python cvzone mediapipe numpy
pip freeze > requirements.txt
▶️ How to Run
After activating your virtual environment and installing the dependencies:

bash
Copy
Edit
python chatgpt.py
A window will open using your webcam. Show your hand, hover over calculator buttons with your index finger, and "pinch" with your middle finger to press.

📸 Controls
Gesture	Action
Pinch (Index + Middle finger)	Click button
Hover (Index finger)	Highlights button
CC	Clears the equation
C  	Removes last character
=	  Evaluates the result
q   (keyboard)	Quits the app

🛠 Tech Stack
  Python
  OpenCV
  cvzone
  MediaPipe

🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request.

📜 License
This project is licensed under the MIT License.

Let me know if you'd like me to:
Add demo GIF/screenshots
Update with your GitHub repo link
Help deploy it or convert to a .exe

Happy coding! 🚀
