# 💡Lightbulb

A simple social networking web application built using Django, Bootstrap, and Font Awesome. Users can sign up, log in, create posts, like posts, follow other users, and search for profiles.

## Table of Contents

- [Features](#features)
- [Technologies Used](#Technologies)
- [Installation](#Installation)

## Features

🔐 User Authentication: Register, log in, and securely log out.

🖼️ Post Creation: Upload images with captions and view them on your feed.

❤️ Like Functionality: Like other users’ posts and view like counts.

👥 Follow System: Follow or unfollow users to see their posts.

🔍 Search Function: Search for user profiles by username.

📄 User Profiles: View and edit personal profiles with a profile picture, bio, and location.

🖥️ Responsive Interface: Clean, modern UI with Bootstrap styling.

## Technologies

- Python 3
- Django
- SQLite 
- Bootstrap 5
- Font Awesome
- HTML5 & CSS3
- JavaScript 

## Installation
Clone my repository:

```bash
git clone https://github.com/darragh50/Lightbulb.git
```
Change directory
```bash
cd Lightbulb
```
Create a virtual environment:
```bash
python -m venv myenv
```

Activate the virtual environment
```bash
myenv\Scripts\activate
```

Install dependencies:

```bash
pip install django, pillow
```
Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Run the development server:
```bash
python manage.py runserver
```

Open in your browser:

```bash
http://127.0.0.1:8000/
```

