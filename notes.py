import flask
import datetime

app = flask.Flask("notes_app")

# === FUNCTIONS ===

# = Create note =
def create_note(note):
    notes = open("notesapp.txt", "a")
    # Get date
    date = date = datetime.datetime.now().strftime("%y/%B/%d")
    notes.write(date + "***")
    notes.write(note)
    notes.write("---")
    notes.close()

# = Get notes =
# def get_notes():
#     document = open("notesapp.txt")
#     content = document.read()
#     document.close()
#     notes = content.split("\n---")

#     # variables to get the text
#     full_text = ""

#     # loop the notes content
#     for note in notes:
#         if note != "":
#             note_array = note.split("***")
#             # get date
#             note_date = "<p class=\"note__date\">" + note_array[0] + "</p>"
#             # get text
#             note_text = "<p class=\"note__text\">" + note_array[1] + "</p>"
#             # create note div
#             full_text += "<div class=\"note\">" + note_date + note_text + "</div>"
    
#     return full_text

# = Search note =
def search_note(text):
    document = open("notesapp.txt")
    content = document.read()
    document.close()
    notes = content.split("---")

    # variables to get the text
    full_text = ""

    # loop the notes content
    for note in notes:
        if note.lower().find(text) != -1:
            note_array = note.split("***")
            if len(note_array) > 1:
                # get date
                note_date = "<p class=\"note__date\">" + note_array[0] + "</p>"
                # get text
                note_text = "<p class=\"note__text\">" + note_array[1] + "</p>"
                # create note div
                full_text += "<div class=\"note\">" + note_date + note_text + "</div>"
        
    if full_text == "":
        full_text = "<div class=\"note\"> <p class=\"note__text\">Sorry! there are no results that match your search.</p> </div>"
    print(full_text)
    return full_text

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
    return get_html("index").replace("{$$ SUBMITED $$}", "")

# = Create note =
@app.route("/submit", methods=['GET', 'POST'])
def addnote():
    note_text = flask.request.form['new_note']
    create_note(note_text)
    return get_html("index").replace("{$$ SUBMITED $$}", "<p> Your note has been saved</p>")

# = Search for notes =
@app.route("/search")
def searchnote():
    search_text = flask.request.args.get("q").strip().lower()
    html_page = get_html("search")
    notes_text = search_note(search_text)
    return html_page.replace("{$$ NOTES $$}", notes_text)
    
    
# = Show full list =
@app.route("/notes")
def shownotes():
    html_page = get_html("search")
    notes_text = search_note("")
    return html_page.replace("{$$ NOTES $$}", notes_text)
