
## Project Overview
This is  a simple software to Manage cars in a show room. 







# Installation and Setup
```
https://github.com/Ngahu/Car-management-System.git
```


## Create a virtual environment

```
python3 -m venv venv;
source venv/bin/activate
```
If you need to install virtualenv:
```
virtualenv venv
```

## Activate the virtual environment
Before you begin you will need to activate the corresponding environment
```
source venv/bin/activate
```
## Install requirements
```
pip install -r car_management_app/requirements.txt
```


## Running the application
After the configuration, first run load_people script to download the json then  run the app 
```
cd car_management_app

chmod +x load_people.sh
./load_people.sh

python manage.py runserver
```

