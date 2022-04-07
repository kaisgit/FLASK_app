from app import app, db
from app.models import User, Post

### Don't forget to (setenv FLASK_APP microblog.py) in the shell

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}
