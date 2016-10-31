
## Libraries used

  * django 1.10.2
  * xlsxwriter 0.9.3
  * pillow 3.4.2
  * reportlab 3.3.0


## Prerequisite

  * python3
  * virtualenv
  * pip

This demo is developed on Linux but should run without problem on any platform able to run python. Your mileage may vary.


## Install and  run

  1. git clone https://github.com/roppert/django-export-excel-and-pdf.git
  1. virtualenv --python=python3 venv
  1. source venv/bin/activate
  1. pip install -r requirements.txt
  1. cd project
  1. ./manage.py migrate
  1. ./manage.py loaddata data
  1. ./manage.py runserver
