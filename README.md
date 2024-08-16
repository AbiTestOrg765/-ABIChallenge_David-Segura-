# -ABIChallenge_David-Segura-
## Proposed architecture
![ABIChalenge](https://github.com/user-attachments/assets/464fb019-0c09-44ad-95c5-3b8f4628340b)

## Colaboration
Required workflow image, obtained via the GitGraph extension from VS Code. Hopefully, this will suffice.
![image](https://github.com/user-attachments/assets/67280a0d-5fb4-4eca-a8c7-9b4e838fde81)

## Sonar CLound
As you can see in the PRs and I hope in the sonar cloud too I have been running checks during the developing process. I have found this solution quite usefull and hopefully I'll keep using it in the future.
![image](https://github.com/user-attachments/assets/7dc2bde3-7eb9-4987-8c5b-0ff52be1cd62)

## ML Model Deployment
This project contains the docker files required to run individually each part of this project (Database and Flask app) you can activate them individually (thought this would probably generate connectivity issues) or run this project with the docker- compose file.

      docker-compose up -d
### Flask app
In order to create the required endpoints I'm using FLask as this is a very simple framework that does not require any configuration files to run.
Most of the code is containd within the Flask/ folder
### Database
I decided to go for postgres Db as I have already worked with it and appreciate that is open source. The DB is made of two tables the `Logs` table and `User`  table, the first one is used to save a register of all the requests that the api proceses and the User table stores users information, as this is a code challenge I decided to focus more on the implementation than in the security part so the passwords are visible.
### Ml model
In this case I decided to select one of the [Titanic competition](https://www.kaggle.com/competitions/titanic) solutions, I picked [this model](https://www.kaggle.com/code/murtadhanajim/80-in-titanic-dataset-using-random-forests) from Murtadha Najim that uses random forests. I had to make som modifications as this model was built in a notebook that handles function deffinition different. 

### End Points

*Predict group survival*

```
curl --location --request GET 'localhost:5000/predict_group_survival' \
--header 'Content-Type: application/json' \
--data '{
"userName":"david" ,
"password": "just_password",
"passengers": [{"Pclass": "3", "Name": "Willer, Mr. Aaron (Abi Weller\")\"", "Sex": "male", "Age": "", "SibSp": "0", "Parch": "0", "Ticket": "3410", "Fare": "8.7125", "Cabin": "", "Embarked": "S"}, {"Pclass": "3", "Name": "Willer, Mr. Aaron (Abi Weller\")\"", "Sex": "male", "Age": "", "SibSp": "0", "Parch": "0", "Ticket": "3410", "Fare": "8.7125", "Cabin": "", "Embarked": "S"}]
}'
```

*Predict individual survival*

```
curl --location --request GET 'localhost:5000/predict_individual_survival' \
--header 'Content-Type: application/json' \
--data '{
"userName":"david" ,
"password": "just_password",
"passenger": {"Pclass": "3", "Name": "Willer, Mr. Aaron (Abi Weller\")\"", "Sex": "male", "Age": "", "SibSp": "0", "Parch": "0", "Ticket": "3410", "Fare": "8.7125", "Cabin": "", "Embarked": "S"}
}'
```

*Create new user*

```
curl --location --request POST 'localhost:5000/newuser' \
--header 'Content-Type: application/json' \
--data '{
"userName":"david" ,
"password": "just_password",
"newUserName":"david" ,
"newPassword": "just_password"
}'
```
