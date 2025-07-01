@echo off

cd ..
mkdir data
echo Installing virtual environment...
python -m venv .venv
call .venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Ready to use!
