To run the script you need to install required packages. So you have to install packages from requirements.txt to your system or into your virtualenv/conda env( which is preferred :) )

I've used **virtualenv** package to create my virtual environment:
```
# create the env
virtualenv PATH_TO_YOUR_ENV -p /usr/local/bin/python3.9

# activate your env
source PATH_TO_YOUR_ENV/bin/activate

# change directory to repository and install packages
pip install -r requirements.txt
```

You can run _prepare_files.py_ to download files provided in task, in that case you don't need to change anything, it just works as it is:

```
python prepare_files.py
python main.py
```

Also you can specify your own DB and currency files in config.ini if you want.

The script should work fine for all RDBMS that use SQL standard, I've converted dummy dump file provided in task to PostgreSQL DB and used for my own tests.
You can download it [here](https://drive.google.com/file/d/1ZCzfpVRQSg8lWLZ8qHoYmTQLOmivooEO/view?usp=sharing)
```
# To restore dump create a new db and instead postgres use any suitable user with permissions
psql -U postgres -c 'create database tech_task;'
gunzip -c tech_task.sql.gz | psql -U postgres tech_task
```

To test the code using PostgreSQL, change **connection_string** in config.ini to your DB. For example(my connection_string):
```
connection_string=postgresql://postgres:secret@localhost/tech_task
```

PostgreSQL connection string format according to [documentation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) is:
```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

#### P.S. Also I've tested all the steps on a fresh Linux VM and hope you don't have any problems :)
