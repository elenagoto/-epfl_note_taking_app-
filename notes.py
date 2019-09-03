import flask

app = flask.Flask("notes_app")

# === FUNCTIONS ===

# = Create note =

# = Get notes =

# = Search note =

# = Get HTML page =
def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content

# === ROUTE FUNCTIONS ===

# = Homepage =
@app.route("/")
def homepage():
    return get_html("index")

# = Create note =

# = Search for notes =

# = Show full list =