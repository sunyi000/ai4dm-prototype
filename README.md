# ai4dm-prototype

Prerequisite
- install GraphDB and create a triple store, for example "ai4dm"


1 . ai4dm-backend is a standard Flask application.

2 . ai4dm-frontend is a Angular10 application.


Steps to start the prototype application.

1. start GraphDB, create a triple store "ai4dm"
2. load triples in all ttl files under ai4dm-backend/data (data-triples and ttl-vocabs folders, exclude aircraft-model.ttl)
3. make sure GraphDB is running, and take notes of its url 
4. update the GraphDB endpoint in config.py in ai4dm-backend
5. start ai4dm-backend application
6. update endpoint in ai4dm-frontend. This endpoint is the Flask server side URL
7. Install Angular10 and all its dependencies.
8. start the ai4dm-frontend applications
9. make sure CORS is enabled
