
# To run local 
after cloning the repo
```
  docker build -t {your_tag} 
  docker run -p 5000:5000 -d {your_tag}
```
or 
```
  pip install -r requirements.txt
  python manage.py run 
```
You should be able to access api on http://localhost:5000/ 

# obtain token
1. Go to

## Notes 

### For db init and migrations 
python manage.py db init
python manage.py db migrate --message 'initial database migration'
python manage.py db upgrade
