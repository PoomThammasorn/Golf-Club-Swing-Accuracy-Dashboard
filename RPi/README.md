# ML Service

## Prerequisites

- Python 3.9.6 or higher
- pip

## Setup

1. **Clone the repository** (if applicable):

   ```bash
   git clone https://github.com/PoomThammasorn/Golf-Club-Swing-Accuracy-Dashboard.git

   cd Golf-Club-Swing-Accuracy-Dashboard/IoT
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**:

   - Windows:
     ```cmd
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

# Run

- For Sensor Publisher that recieve data from sensor and publish to MQTT Broker

  ```bash
  python sensors_publisher.py
  ```

- For Run Camera Publisher that recieve data from [IP Camera Lite](https://apps.apple.com/th/app/ip-camera-lite/id1013455241?l=th) and publish to MQTT Broker

  ```bash
  python camera_publisher.py
  ```

## After install additonal packages

```bash
pip freeze > requirements.txt
```
