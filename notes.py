# To run it: FLASK_APP=notes.py flask run

import flask
import datetime

app = flask.Flask("notesapp")

# === FUNCTIONS ===


def create_note(note):
    # Open note
    notes = open("notesapp.txt", "a")
    # Get date
    date = datetime.datetime.now().strftime("%d/%B/%y")
    # write date + separator
    notes.write(date + "***")
    # write note + newline
    notes.write(note + "\n")
    # write separator
    notes.write("---")
    # close note
    notes.close()

# Function to use inside the search_note function below
def parse_note(notes_array, text):
    # variables to get the text
    full_text = ""
    notes_count = 0

    # loop the notes content
    for note in notes_array:
        if note.lower().find(text) != -1:
            notes_count += 1
            # Make list with single note to separate date and text
            note_array = note.split("***")

            # get date. If note created Today, then text is TODAY
            today = datetime.datetime.now().strftime("%d/%B/%y")
            if note_array[0] == today:
                note_date = "<p class=\"note__date\">Created: <span>Today<span></p>"
            else:
                note_date = "<p class=\"note__date\">Created: <span>" + \
                    note_array[0] + "<span></p>"

            # get text
            note_text = note_array[1].replace(
                "\n", "<br>")  # Keeping newlines in notes
            note_text = "<p class=\"note__text\">" + note_text + "</p>"

            # create note div with latest note created appearing first in the list
            full_text = "<div class=\"note\">" + note_date + note_text + "</div>" + full_text
    
    # Produces the final text to add to the page with the results
    if full_text != "":
        full_text = "<h3>Notes found: " + \
            str(notes_count) + "</h3 >" + full_text

    # If there are no results
    else:
        full_text = "<h3>Notes found: " + str(notes_count) + \
            "</h3> <div class=\"note\"> <p class=\"note__text\">Sorry! there are no results that match your search.</p> </div>"

    return full_text


def search_note(text):
    # open file
    document = open("notesapp.txt")
    # get content
    content = document.read()
    # close file
    document.close()
    # split content using separator
    notes = content.split("\n---")
    # erase the last element that is always empty
    notes.pop(len(notes) - 1)

    # get note with the function created above
    note = parse_note(notes, text)
    return note


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
@app.route("/addnote", methods=['GET', 'POST'])
def addnote():
    note_text = flask.request.form['new_note']
    html_page = get_html("index")
    if note_text != "":
        create_note(note_text.strip())
        return html_page.replace("{$$ SUBMITED $$}", '<p class="form__saved"> Your note has been saved</p>')
    else:
        return html_page.replace("{$$ SUBMITED $$}", "")
        

# = Search for notes =
@app.route("/search")
def search():
    search_text = flask.request.args.get("q").strip().lower()
    html_page = get_html("search")
    notes_text = search_note(search_text)
    return html_page.replace("{$$ NOTES $$}", notes_text)
    
    
# = Show full list =
@app.route("/all_notes")
def all_notes():
    html_page = get_html("search")
    notes_text = search_note("")
    return html_page.replace("{$$ NOTES $$}", notes_text)
