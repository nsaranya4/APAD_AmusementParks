# Amusement Parks
## Project Overview 
The project includes building a web-based crowd-sourcing application where users can upload pictures, pin geotags and share their experience of different amusement parks. The application features include creating parks/posts/users, searching posts by tags, subscribing/unsubscribing to amusement parks and viewing the user's history of uploads.

## Team Members
- Bhargav Naik
- Gowtami Khambhampati
- Haoyang Li
- Saranya Nagarajan

## Components

### Backend
This service hosts the backend which is a REST service which performs read write to mongo DB and serves JSON response. This will be a common service which will be used by frontend and mobile application for performing CRUD operations.

#### Project Layout

#####  - Resources
Package Contains all python Flask-Restful http resources which is used for implementing the CRUD API. All the Authentication and JSON validation can be done in this layer.

##### - Services
Package contains the business logic to handle the requests for the resources. Authorization checks and other business logic can be put in this layer.

##### - Repositories
Package contains the repository per entity which creates an abstraction layer between the data access layer and the business logic layer.

##### - Models
Package contains the database collections, fields and field constraints

##### - Representations
Package contains all the Request, Response objects used to interact with backend microservice. We have used the marshmallow python package to eliminate boilerplate code required for serializing, deserializing json objects. These models are separated from the DB models and help us maintain a contract with the clients in case the DB the models changes in the future. We can version the models and take advantage of the API versioning that we have in place (/funtech/<version>/<resource>)

##### - [Requirements.txt]( https://github.com/APAD-Summer2020/Team4/blob/master/backend/app/requirements.txt ) 

---

### UI
This service hosts the frontend and communicates with the backend REST service using http client to perform CRUD operations.

#### Project Layout
##### - Routes
All the app routes for user, park, post are wired in this package using blueprints

##### - Clients
Package contains all the http clients (Park, Post, User, Firebase) to make calls to the backend. We have used a Firebase client to upload/download images from the firebase cloud storage.

##### - Representations
Package contains all the Request, Response objects used to interact with backend microservice. We have used the marshmallow python package to eliminate boilerplate code required for serializing, deserializing json objects.

##### - Static
Contains the *.css, *.js  files required for the website

##### - Templates
Contains the html file for the website. We have used Jinja templating for dynamic python pages.

##### - [Requirements.txt](https://github.com/APAD-Summer2020/Team4/blob/master/ui/app/requirements.txt) 

---

### Android
Android app to view the Amusement parks and rides shared by user. 
- It connects to the backend service to get the json data.
- It connects to the firebase for user login
- It connects to the firebase storage for uploading and downloading images

#### Libraries
- [Firebase Google SignIn](https://firebase.google.com/docs/auth/android/google-signin): for implementing Single Sign In functionality
- [Firebase Cloud Storage](https://firebase.google.com/docs/storage/android/start): for implementing upload/download image functionality
- [Retrofit](https://square.github.io/retrofit/) library drastically reduces the boilerplate code and make integration with backend(REST) service seamless.
- [Picasso](https://square.github.io/picasso/)  provides seamless support for displaying images.
- [ImagePicker](https://github.com/esafirm/android-image-picker): library for integrating with camera and gallery to add pictures to post


 
