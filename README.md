# About 

This project was created by my own as a final project in one of study programs, which name is "Data Science full course".

# Files

The notebook "final" is the whole completed work. Here you can find all steps collected in one big file
File "api.py" contains an api service (as the main executor of a model). Its service realization was made in "service.py" file
In file "instruction.txt" you can find the Russian instruction how to use api service
In 'model' folder you can find .pkl files of the model and its transformers
We also have an additional file with business notes about the model, which was created in Russian

# API instruction

1. /status - status check. If u got 200, everything is up (GET)
2. /metadata - meta-data output (GET)
3. /predict - prediction. 0 - no target action is awaited. 1 - a target action is awaited (POST)
4* /predict_proba - probability output (POST)
