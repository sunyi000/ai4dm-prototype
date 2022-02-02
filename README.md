# ai4dm-prototype

Prerequisite
- install GraphDB and create a triple store, for example "ai4dm"
- download AnyBURL, and take note of its binary location


1 . ai4dm-backend is a standard Flask application.
2 . ai4dm-frontend is a Angular10 application.

# Ontology files
- ai4dm-schema.ttl is the main schema for ai4dm kb. It imports the below files
    - data-triples folder contains all instances in the ontology. (aircraft-model.ttl is not used for now)
    - ttl-vocabs contains the controlled vocabulary ontology which are imported by the main ai4dm ontology schema 

# Steps to start the prototype application.

1. start GraphDB, create a triple store "ai4dm"
2. load triples in all ttl files under ai4dm-backend/data (data-triples and ttl-vocabs folders, exclude aircraft-model.ttl)
3. make sure GraphDB is running, and take notes of its url 
4. update the GraphDB endpoint in config.py in ai4dm-backend
5. replace line 350 in app.py with anyBURL binary file location
6. start ai4dm-backend application
7. update endpoint in ai4dm-frontend. This endpoint is the Flask server side URL
8. Install Angular10 and all its dependencies.
9. start the ai4dm-frontend applications
10. make sure CORS is enabled
