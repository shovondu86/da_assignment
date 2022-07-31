# da_assignment
Assignment for data analysis with python flask

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-22-04
git clone https://github.com/shovondu86/da_assignment
cd /da_assignment
python3 -m venv my_env
source my_env/bin/activate
pip istall -r requirments.txt
pip istall -r requirments.txt

Open another terminal 

## Data load and analysis
#DiseaseList upload 
a.curl -L -F "file=@disease_list.csv" http://localhost:8000/diseaselistload > diseaselistjson.json
b.curl  http://localhost:8000/diseaseListInfos 

#Cases upload analysis for data_cases_2.csv and data_cases_corrupted.csv
a.curl -L -F "file=@data_cases_2.csv" http://localhost:8000/datacasesload > indicators.json
b.curl  http://localhost:8000/getIndicatorInfos > indicators.json
c.curl  http://localhost:8000/getAdvIndicatorInfos > indicators_advanced.json
