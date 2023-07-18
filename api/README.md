# SocialNet Backend

There are some endpoints for mini socialnet 

With this API you can:
- Register as User
- Login with User
- See all posts
- Create/Delete/Edit your Post 
- React with other's posts

## Technologies used:
- FastAPI as backend framework
- SQLAlchemy as ORM
- Redis as im-memory db for cache
- PostgreSQL as db

## Features
- Backend use OAuth2.0 for authorization and authentication
- Using EmailHunter API to verify is email exisists

## Usage instractions

### For Local usage:
```zsh
git clone https://github.com/algakz06/test_task.git 

cd test_task/api 

docker compose up -d (For MacOS)
docker-compose up -d (For Linux)
```
SwaggerUI will be in http://localhost:3333/docs

### For Non-Local Usage

API was deployed to server

You can see SwaggerUI in http://176.57.213.66:3333/docs
