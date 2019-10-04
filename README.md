# persona_movieChar
Analyze movie character base on their speech


## Content
- main.py : python file to analyze dataset
- requirements.txt : python depencency packages 
- Top1_movie_actor.csv : dataset

## Preparation
1. create virtual enviroment & activate it
```bash
virtualenv venv -p python3
source venv/bin/activate
```
2. install python packages
```bash
pip install -r requirements.txt
```
3. Put dataset on same folder with main.py
4. open main.py on text editor, change setting *personality_insights* (API Key and URL) and *filename* with IBM watson setting and dataset filename


## Running
1. activate virtual env
```bash
source venv/bin/activate
```
2. running the python file
```bash
python main.py
```
3. after python file finish running, output files will be in output directory
