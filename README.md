# PixPlore

## Prerequisites
## Step 1: Clone the Repository

Open your terminal or command prompt and run the following command to clone the PixPlore repository:

```bash
git clone https://github.com/Yoelaugustan/PixPlore.git
```

Navigate to the project directory:
```bash
cd PixPlore
```

## Step 2: Create a Virtual Environment

Creating a virtual environment is recommended to avoid conflicts with other Python projects.

### For Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### For macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

## Step 3: Install Dependencies

With your virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

Once all dependencies are installed, you can run the Streamlit application:

```bash
streamlit run HomePage.py
```

## Step 5: Access the Application

After running the command, Streamlit will automatically open your default web browser and navigate to the application. If it doesn't open automatically, you can access it at:

```
http://localhost:8501
```
