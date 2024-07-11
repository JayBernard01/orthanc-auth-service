0. `docker compose up` -> connect to the admin console as admin http://localhost/keycloak (username: admin / pwd: change-me) and change to Orthanc Realm
![alt text](image-11.png)
![alt text](image-12.png)
![alt text](image-13.png)
1. add a Realm Role 
![alt text](image.png)
![alt text](image-1.png)
2. add User
![alt text](image-2.png)
![alt text](image-3.png)
3. assign Role
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-4.png)
4. add password
![alt text](image-7.png)
![alt text](image-8.png)
![alt text](image-9.png)
5. add [permissions](./permissions.jsonc) 
![alt text](image-10.png)
6. restart: `ctrl+c` in terminal -> `docker compose up` -> connect to the new user (username: researcher / pwd: change-me)

