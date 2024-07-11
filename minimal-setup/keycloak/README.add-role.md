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
![alt text](image-17.png)
4. add password
![alt text](image-4.png)
![alt text](image-7.png)
![alt text](image-8.png)
![alt text](image-9.png)
5. add [permissions](./permissions.jsonc) 
![alt text](image-16.png)
6. connect as admin and add a study with the `research` flag and press enter
![alt text](image-14.png)
![alt text](image-15.png)
7. restart: `ctrl+c` in terminal -> `docker compose up` -> http://localhost/ -> connect to the new user (username: researcher / pwd: change-me)
8. you should see the study with researcher (with the research tag) but not see it with the external account
