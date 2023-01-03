# dwarf-app
"Twitter-like" social media

## Getting started

### Run Locally
 
 - Create a virtual environment(venv) [OPTIONAL]
 
 https://www.youtube.com/watch?v=hA2l0TgaZhM&t=146s (Tutorial PT/BR)
 https://www.youtube.com/watch?v=Wuuiga0wKdQ (Tutorial ENG)
 
 - Install all required packages:
```
pip install -r requirements.txt
```
- Setup database
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Run in your localhost server:
```
python manage.py runserver
```

## What you can do

- Create your account and login
- Email verification and password recovery (temp. disabled)
- Change your profile settings (image,nickname,etc)
- Post (image and text)
- Like and comment
- Follow other users

## To do

-Block user system
- Notifications
- "Retweet"
- Save Posts (Favorite posts)

