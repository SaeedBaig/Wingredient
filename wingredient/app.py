from .routes import app

# Necessary for session to work in routes.py
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.run(debug=True, port=8001)
