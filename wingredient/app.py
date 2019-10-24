from .routes import app

# Necessary for session to work in routes.py
app.secret_key = b'\xc4\xff\xb4\xe8|\xec\xbb\x150\xe9\xfd\xff7\x1fY\xbc'

app.config['SESSION_TYPE'] = 'filesystem'

app.run(debug=True)
