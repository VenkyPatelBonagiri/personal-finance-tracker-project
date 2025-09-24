Software Requirements
Operating System:
The Personal Finance Tracker is a desktop GUI application and works on any OS with a graphical interface. Tested and compatible with:
Windows: Windows 10 / 11
macOS: macOS 10.15 (Catalina) or newer
Linux: Modern distributions with a desktop environment (e.g., Ubuntu 20.04+, Fedora 36+, Mint 21+)

Python:
Version: Python 3.8 or newer is required.

Git (Optional):
Only needed if you want to clone the project directly from GitHub.

Hardware Requirements
This project is very lightweight and runs smoothly on most modern computers:
RAM: Minimum 2 GB
Disk Space: At least 50 MB of free space
Internet Connection: Required only for two cases:
Installing libraries during the initial setup.
Converting currencies (uses Frankfurter API).

Python Library Dependencies
All dependencies can be installed using pip.
Required Libraries:
requests → For fetching real-time exchange rates from the Frankfurter API
matplotlib → For generating the pie chart (spending analytics)
tkinter → Built-in with Python (for GUI)
json & os → Built-in modules (for data storage and file handling)
Install All at Once
Navigate to the project folder and run:
pip install -r requirements.txt
Or Install Manually
pip install requests matplotlib

API Requirement
This project uses the Frankfurter API for live currency conversion.
Service: Frankfurter Exchange Rates API
API Key: Not required — it’s a free, no-authentication API.


How to Run the Application

Follow these steps to set up and run the Personal Finance Tracker on your computer:

1. Clone the Repository (or Download ZIP)
If you have Git installed, run:
git clone https://github.com/your-username/personal-finance-tracker.git
Or download the project as a ZIP file from GitHub and extract it.

2. Navigate to the Project Folder
Open a terminal (or VS Code terminal) and go into the project directory:
cd personal-finance-tracker

3. (Optional) Create a Virtual Environment
This keeps your dependencies isolated:
python -m venv venv

Activate it:

Windows (PowerShell):
.\venv\Scripts\Activate

macOS/Linux:
source venv/bin/activate

4. Install Dependencies
Install all required libraries:
pip install -r requirements.txt

5. Run the Application
Start the GUI by running:
python gui.py
