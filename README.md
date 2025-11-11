# Create branch
git status
--make sure you are on main branch
git checkout -b <branch_name>
-- creates a new branch


# Create your environment
## Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Windows
python -m venv venv
venv\Scripts\activate

# Update environment if you added any libraries
pip freeze > requirements.txt


# Run the app
python main.py
