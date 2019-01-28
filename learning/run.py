# Setup django app
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning.settings")
django.setup()
from quiz.models import pumpModel
from quiz.man import predict

def pump_into_model(pump_row):
    reuslt = pumpModel()
    reuslt.needHelp = pump_row
    reuslt.save()

if __name__ == "__main__":
    let = predict()
    #print(let)

    test = []

    for i in range(len(let)):
        test.append(let[i])
        pump_into_model(let[i])
                    
    #print(len(test))
