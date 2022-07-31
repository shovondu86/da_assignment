# da_assignment
## Assignment for a Software Engineer position July 2022
This repository holds source code for the above mentioned assignment. This application uses Flask and SQLite to import user defined ```csv``` file to generate customized data analysis report in ```json``` format. 

#### Requirements:

* Install Ubuntu 20.04 or higher (tested on Ubuntu 22.04)
* Install Python 3.x or higher [(steps are here)](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-22-04/)  
* Git
* cURL

### Installation:
* Clone the repo to your pc <br />
```
git clone https://github.com/shovondu86/da_assignment
```
* Change directory path using and create a Python virtual environment
```
cd da_assignment/ && python3 -m venv my_env
```
* Activate the newly created virtual environment and install the required libraries 
```
source my_env/bin/activate
pip install -r requirments.txt
```
* Run the application in the CLI environment
```
python run.py
```


### Data processing:
Open the another terminal 
#### Disease list processing:
```
curl -L -F "file=@[input_disease_CSV_file]" http://localhost:8000/diseaselistload > [output_name].json
```
example
```
curl -L -F "file=@disease_list.csv" http://localhost:8000/diseaselistload 
```

#### Data case processing and analysis:
### Total number of reported cases and total number of deaths reported at each location
```
curl -L -F "file=@[input_data_cases_CSV_file]" http://localhost:8000/datacasesload > [output_name].json
```
example
```
curl -L -F "file=@data_cases_2.csv" http://localhost:8000/datacasesload > indicators.json
```
To get the output only once uploaded
```
curl http://localhost:8000/getIndicatorInfos > indicators.json
```
View the result
```
curl http://localhost:8000/getIndicatorInfos
```
To handle corrupt data use the exsiting method
```
curl -L -F "file=@[input_corrupt_data_cases_CSV_file]" http://localhost:8000/datacasesload > [output_name].json
```

### To use the advanced indicators
Average number of sick for cat (defualt) from villages and total number of deaths from each disease 
```
curl  http://localhost:8000/getAdvIndicatorInfos?species=cat > indicators_advanced.json
```
For pig
```
curl  http://localhost:8000/getAdvIndicatorInfos?species=pig
```
Others species are same way like
buffalo,
chicken,
dog,
sheep


