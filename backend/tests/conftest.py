import os
import sys

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))