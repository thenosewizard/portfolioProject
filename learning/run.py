# Setup django app
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning.settings")
django.setup()
from quiz.models import pumpModel
from quiz.man import predict

if __name__ == "__main__":
    predict()

                    
