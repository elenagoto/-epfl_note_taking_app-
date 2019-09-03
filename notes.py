import flask
import datetime

app = flask.Flask("notes_app")

# === FUNCTIONS ===

# = Create note =
def create_note(note):
    notes = open("notesapp.txt", "a")
    # Get date
    date = date = datetime.datetime.now().strftime("%d/%B/%y")
    notes.write(date + "***")
    notes.write(note + "\n")
    notes.write("---")
    notes.close()


# = Search & get notes =
def search_note(text):
    document = open("notesapp.txt")
    content = document.read()
    document.close()
    notes = content.split("\n---")
    notes.pop(len(notes) - 1)

    # variables to get the text
    full_text = ""

    # loop the notes content
    for note in notes:
        if note.lower().find(text) != -1:
            # Make list with single note to separate date and text
            note_array = note.split("***")

            # get date. If note created Today, then text is TODAY
            today = datetime.datetime.now().strftime("%d/%B/%y")
            if note_array[0] == today:
                note_date = "<p class=\"note__date\">Created: <span>Today<span></p>"
            else:
                note_date = "<p class=\"note__date\">Created: <span>" + note_array[0] + "<span></p>"
            
            # get text
            note_text = note_array[1].replace("\n", "<br>")#Keeping newlines in notes
            note_text = "<p class=\"note__text\">" + note_text + "</p>"
            
            # create note div with latest note created appearing first in the list
            full_text = "<div class=\"note\">" + note_date + note_text + "</div>" + full_text
        
    if full_text == "":
        full_text = "<div class=\"note\"> <p class=\"note__text\">Sorry! there are no results that match your search.</p> </div>"
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
    return get_html("index").replace("{$$ SUBMITED $$}", "").replace("{$$ WELCOME $$}", '<h2 id="welcomeMessage">Welcome <span id="userName"></span></h2>')

# = Create note =
@app.route("/submit", methods=['GET', 'POST'])
def addnote():
    note_text = flask.request.form['new_note']
    html_page = get_html("index").replace("{$$ WELCOME $$}", '')
    if note_text != "":
        create_note(note_text.strip())
        return html_page.replace("{$$ SUBMITED $$}", "<p> Your note has been saved</p>")
    else:
        return html_page.replace("{$$ SUBMITED $$}", "")
        

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
