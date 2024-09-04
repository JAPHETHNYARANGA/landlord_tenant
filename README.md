# City Reality Backend
## Overview
This is the backend api for City Reality App,  a house management App.

## Technologies Used

1. [Python-Django](https://www.djangoproject.com/start/) 
2. [PostgreSQL](https://www.postgresql.org/docs/): An open-source relational database system.

## Prerequisites

1. Python Development Kit (Python 3.12.3) installed on your machine.
2. 
## Setup Instructions

1. Clone the Repository ` git clone https://github.com/JAPHETHNYARANGA/landlord_tenant.git`
   
      1. Cd into the landlord_tenant directory and cd into `City  project so as to activate project virtual enviroment by running  ` source enviroment/bin/activate` and after it    run `pip install requirements.txt` to install python dependancies being used in the project from your  terminal
         2.  Nagivating into the python-Django app 
        2. To Nagivate into the Django app created -  `cd into reality ` and check .env file where you will see database configuration variable and edit your DB_NAME,DB_USER,DB_PASSWORD according to your preference examples e.g 
            DB_NAME=city
            DB_USER=realityuser
            DB_PASSWORD=password
         # 3. Creating database
         # first install components from unbuntu  Repositories by typing `sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`
Create database by typing `sudo -u postgres psql` to open postgres console from your terminal in ubuntu  then run `CREATE DATABASE city`; to create a  database.

 Next, you will create a database user which you will use to connect to and interact with the database. Set the password to something strong and secure by typing ` CREATE USER realityuser WITH PASSWORD 'password';` from your postgres console on your terminal.

 Afterwards, you will modify a few of the connection parameters for the user you just created. This will speed up database operations so that the correct values do not have to be queried and set each time a connection is established by typing ` ALTER ROLE realityuser SET client_encoding TO 'utf8';ALTER ROLE realityuser SET default_transaction_isolation TO 'read committed';ALTER ROLE realityuser SET timezone TO 'UTC'; `
 You are setting the default encoding to UTF-8, which Django expects. You are also setting the default transaction isolation scheme to “read committed”, which blocks reads from uncommitted transactions. Lastly, you are setting the timezone. By default, your Django projects will be set to use UTC. These are all recommendations from the Django project itself


 Lastly , all you need to do is give your database user access rights to the database you created by typing  `GRANT ALL PRIVILEGES ON DATABASE city TO realityuser;` and lastly run `GRANT ALL PRIVILEGES ON SCHEMA public TO your_database_user` to avoid getting  migrations error .


4. Migrations: to apply migrations you need to run ` python3 manage.py makemigrations ` m which is responsible for creating new migrations based on the changes you have made to your models. then run  `python3 manage.py migrate ` which is responsible for applying and unapplying migrations.



 5. Create a Superuser so as to access the admin side  of the project by running  `python manage.py createsuperuser` , it will prompt you to enter `username,email and password`   after creating from your terminal in project run `python3 manage.py runserver `   then open the link from your browser and run `http://127.0.0.1:8000/admin`  fill in your username password  to  access the page.


 6 Running the django app  cd city and run python3 manage.py runserver

#  Contributing
1. Clone repository
    ```bash
    git clone https://github.com/JAPHETHNYARANGA/landlord_tenant.git
    ```
2. Change to the `development` branch
    ```bash
    cd /cd C
    ```
3. Create a new feature branch off this branch
    ```bash
    git checkout -b feature-example
    ```
4. Make your changes and commit them.
5. Pull the latest changes from the `development` branch and merge them into your working branch.
    ```bash
    git checkout development
    git pull origin development
    git checkout feature-example
    git merge development
    ```
6. Resolve any merge conflicts that you may have, then push your feature branch
    ```bash
    git push origin feature-example
    ```
7. Create a pull request against the base branch (`development`).
8. Give a summary of what changes your working branch introduces. 

See [example pull request](https://github.com/JAPHETHNYARANGA/landlord_tenant.git).




 lasty cd into reality and you will see all the app files e.g serializer.py ,models.py etc

 # Dtabase structure

 `https://lucid.app/lucidchart/a51c8867-26f8-4184-a3f7-d134b5fb8652/edit?viewport_loc=1219%2C597%2C2125%2C1104%2C0_0&invitationId=inv_c3817d27-33dd-467f-85c0-ad76448cd2f9`

 ## Applications structure 

Users:

    Admin
    Landlord
    Tenant
Properties:

    Property
    Property Search
Bookings:

    Booking
Payments:

    Rent Payment
    Virtual Wallet
    Transaction
Maintenance:

    Maintenance Ticket
Emergency Contacts:

    Emergency Contact
Chat:

    Chatbox



 