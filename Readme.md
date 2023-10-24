# Global Gazette Backend

A quick brown fox jumps over the lazy dog multiple times, illustrating the backend setup for the Global Gazette project.

## Prerequisites

- Python 3.10 (or whichever version you're using)
- pip
- virtualenv (optional but recommended)

## Installation

### 1. Clone the Repository  

```bash
git clone https://github.com/FarehaSi/global-gazette-backend.git backend
cd backend/
```

### 2. Set up a Virtual Environment (optional but recommended)
```bash
python3 -m venv venv 
```
#### Activating the Virtual Environment
To activate the virtual environment, follow the instructions below based on your operating system:
. Windows
```bash
venv\Scripts\activate
```
. Mac and Linux
```bash
source venv/bin/activate
```
### 3. Installing Dependencies
To install the dependencies for this project, use pip with the provided requirements.txt file:
```bash
pip install -r requirements.txt
```
This will install all the required dependencies for the project.

### 4. Run Migrations
```bash
python manage.py migrate
```
### 5. Run the Development Server
```bash
python manage.py runserver
```
You should now be able to access the development server at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
