# SOFT DESK REST API 

## **Description**

This API is used for an application that tracks issues on web site and
 android/IOS apps. 
 The API endpoints will served tha data.


## **Clone the repository**

Download the repository from this link to the local folder you want: https://github.com/MargueriteT/SoftDesk.git

## **Installation**

First, make sure you already have python3 install on your computer. If not, please go to this link: https://www.python.org/downloads/ and follow the instructions. Open your Cmd and proceed as indicated:

    Navigate to your repository folder: cd path/to/your/folder
    Create a virtual environment: python -m venv env (windows) python3 -m venv env (macos ou Linux)
    Activate this virtual environment: env\Scripts\activate (windows) ou source env/bin/activate (macos ou linux)
    Install project dependencies: pip install -r requirements.txt
    Navigate to the SoftDesk folder : cd SoftDesk
    Run the program: python manage.py runserver

In the SoftDesk application, create a configuration.py file from which the
 SECRET_KEY will be imported.

## **SoftDesk API**

### Signup

POST/signup/

API endpoint to register a new user Five keys must be provided in the body : 
- username, 
- email, 
- first_name, 
- last_name, 
- password.

   
       successful request : http status 201 
       missing key or already exists : http status 400 

### Login

POST/login/

API endpoint to log in. Two key must be passed in the body : 
- username, 
- password.

   
      successful request : http status 200 
      account doesn't exist or password error : http status 401
      missing field : http status 400

### Projects list

GET/projects/

API endpoint to access the user's projects. The user can access only projects if he is author or contributor. 
Token must be provided to access this page.

 
     successful request : http status 200 
     no token : http status 401

### Create a new project

POST/projects/

API endpoint to create a new project. Token must be provided. 
The user must provided :
 - the title,
 - the description,
 - the type.


    successful request : http status 201 
    no token : http status 401
    missing field : http status 400

### Details of a project

POST/projects/{project_id}/

API endpoint to access details on a project. The user can access only projects if he is author or contributor. 
Token must be provided to access this page.

  
    successful request : http status 200 
    no token : http status 401
    non-existent project : http status 404


### Update a project

PUT/projects/{project_id}/

API endpoint to update details on a project. The user can only update a project if he is the author. 
Token must be provided to access this page. The user must provide :
- title,
- description,
- type.


    succesful request : http status 200 
    no token : http status 401
    non-existent project : http status 404


### Delete a project

DELETE/projects/{project_id}/

API endpoint to delete a project. The user can only delete a project if he is the author. 
Token must be provided to access this page.

    sucessful request : http status 204
    no token : http status 401
    non-existent project : http status 404


### Access list of users for a specific project

GET/projects/{project_id}/users/

API endpoint to access the list of contributor for the selected project. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401

### Add an user

POST/projects/{project_id}/users/

API endpoint to add an user to the project's contributors.
Token must be provided to access this page. The user must provide the
 following keys :
 - permission,
 - role,
 - project,
 - user_id.


    sucessful request : http status 201
    no token : http status 401
    missing field : http status 400
    

### Details of an user

GET/projects/{project_id}/users/{user_id}/

API endpoint to access the details on a specific contributor. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401
    non-existent user : http status 404

### Update an user

PUT/projects/{project_id}/users/{user_id}/

API endpoint to update data of a specific contributor. 
Token must be provided to access this page.
The user must provide the following keys :
 - permission,
 - role,
 - project,
 - user_id.
 

    sucessful request : http status 200
    no token : http status 401
    non-existent user : http status 404
    missing field : http status 400
    
### Delete an user

DELETE/projects/{project_id}/users/{user_id}/

API endpoint to delete a specific contributor. 
Token must be provided to access this page.

    sucessful request : http status 204
    no token : http status 401
    non-existent user : http status 404
    
### List of issues for a specific project

GET/projects/{project_id}/issues/

API endpoint to access the list of issues for the selected project. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401
    
### Create a new issue

POST/projects/{project_id}/issues/

API endpoint to a new issue for the selected project. 
Token must be provided to access this page. 
The user must provide the following keys :
- title,
- description,
- tag,
- priority,
- project_id,
- status.
Author_user is set to the logged in user. Assigned_user is the author of the
 project.
 

    sucessful request : http status 200
    no token : http status 401
    missing field : http status 400
    
### Details of an issue

GET/projects/{project_id}/issues/{issue_id}/

API endpoint to access the details of a specific issue. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401
    non-existent issue : http status 404
    
### Update an issue

PUT/projects/{project_id}/issues/{issue_id}/

API endpoint to update data of a specific issue. 
Token must be provided to access this page.
The user must provide the following keys :
- title,
- description,
- tag,
- priority,
- project_id,
- status.


    sucessful request : http status 200
    no token : http status 401
    non-existent user : http status 404
    missing field : http status 400
    
### Delete an issue

DELETE/projects/{project_id}/issues/{issue_id}/

API endpoint to delete a specific issue. 
Token must be provided to access this page.

    sucessful request : http status 204
    no token : http status 401
    non-existent issue : http status 404
    
### List of comments for a specific issues

GET/projects/{project_id}/issues/{issue_id}/comments/

API endpoint to access the list of comments for the selected issue. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401


### Add a comment

POST/projects/{project_id}/issues/{issue_id}/comments/

API endpoint to create a new comment for the selected issue. 
Token must be provided to access this page.
The user must provide the following keys :
- description


    sucessful request : http status 200
    no token : http status 401
    missing field : http status 400
    
### Details on a comment

GET/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/

API endpoint to access the details of a specific comment. 
Token must be provided to access this page.

    sucessful request : http status 200
    no token : http status 401
    non-existent issue : http status 404
    
### Update a comment

PUT/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/

API endpoint to update the details of a specific comment. The user can
 update a comment only if is his author.
Token must be provided to access this page.
The user must provide the following keys :
- description


    sucessful request : http status 200
    no token : http status 401
    non-existent comment : http status 404
    
### Delete a comment

DELETE/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/

API endpoint to delete a specific comment. The user can delete a comment
 only if is his author.
Token must be provided to access this page.

    sucessful request : http status 204
    no token : http status 401
    non-existent comment : http status 404