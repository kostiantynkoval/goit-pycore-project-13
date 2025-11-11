# Create branch

```
git status
```
make sure you are on `main` branch
```
git checkout -b <branch_name>
```
creates a new branch


# Create your environment
## Linux

```
python3 -m venv venv
source venv/bin/activate
```

## Windows

```
python -m venv venv
venv\Scripts\activate
```

# Install dependencies from requirements.txt

```
pip install -r requirements.txt
```

# Update environment (in case you added any libraries)

```
pip freeze > requirements.txt
```


# Run the app

```
python main.py
```
