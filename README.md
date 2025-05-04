 ## Overview
This is a university AWS project incorporating ubuntu EC2 instance and postgresql RDS served by static file in S3. the project includes two files zhamshid_index.html that has markup styling and js script, and python app.py file running on flask. server runs at port 5000.
## Endpoints
 4 endpoints are available on server: /schema, /preview, /add, /delete<id>.
## How to Run
to start the project connection to EC2 instance is required. once inside instance venv needs to be activated with source venv/bin/activate. there is a dir called webapp_zhamshid inside that dir the app.py file started by python3 app.py command. once the server is up and running (watch logs in terminal) app can be accessed through static file from bucket. note that the EC2 instance is attached to elastic ip address to avoid manual adjustment on every instance re-run

## Screenshots
![image](https://github.com/user-attachments/assets/8bd9a796-4673-45a6-a90d-138d066b69e0)
![image](https://github.com/user-attachments/assets/9fc699a1-ba5f-4585-b7b2-8eb4674eeb82)
![image](https://github.com/user-attachments/assets/67e8b1d6-7841-4998-8446-ce8d0ab6ff35)
![image](https://github.com/user-attachments/assets/e3a8a70a-0483-4d8d-b664-ee8873723fde)

## links: 
s3 http://zhamshidt1.s3-website.ap-northeast-2.amazonaws.com
rds endpoint db-zhamshid.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com
ec2 instance ssh -i "zhamshid_key.pem" ubuntu@ec2-3-36-4-76.ap-northeast-2.compute.amazonaws.com, elastic ip address 3.36.4.76
