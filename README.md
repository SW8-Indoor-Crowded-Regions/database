# 📂 Indoor Crowded Region Detection Database

This repository provides a **MongoEngine-based database** for managing data related to **indoor crowded region detection**.

---

## 📦 Installation

To install this package in your project, run following cmd:

```python
pip install git+https://github.com/SW8-Indoor-Crowded-Regions/database.git
```
And remember to use pipreqs to save dependencies.

## ⚙️ Setup
- add secrets to .env
- update dependency in case of updates 
- import config when interacting with db


## 🚀 Example of usage
Below is an example with a fictional model of a user.
```python
import config  # REMEMBER TO IMPORT! - Handles DB connection
from models import User  # Models are now easily accessible

# Create a new user
user = User(name="Alice", email="alice@example.com")
user.save() # User is now saved, if all went well!
``` 
