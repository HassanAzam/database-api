# Database as a Service implementation using Python, Flask, MongoDB and Docker

## Description
- User can sign up for using API by sending json object of username and password at /register
```
{
    "username": "user",
    "password": "pass"
}
```
- User will be given 10 Tokens initially for storing data
- User can add sentence to database by sending post request at /store. This action deducts one token
```
{
    "username": "user",
    "password": "pass",
    "sentence": "hello my first sentence"
}
```
- User can get his/her sentence by hitting /get for 1 token
```
{
    "username": "user"
    "password": "pass"
}
```
- status 301 means out of tokens
- status 302 means invalid username or password

## How to run
* Clone the repo
* $ cd database-api
* $ docker-compose build
* $ docker-compose up
* Open new terminal/cmd
* Find you docker machine IP by typing
* $ docker-machine ip
* Open your browser and type : http://your-docker-machine-ip:5000/
* if helloworld appears then its working fine
* Test API using POSTMAN