@echo off

cd ..
echo Installing virtual environment...
python -m venv .venv
call .venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Ready to use!
