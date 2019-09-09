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
    # element to compare the date of the note
    today = datetime.datetime.now().strftime("%d/%B/%y")

    # loop the notes content
    for note in notes_array:
        if note.lower().find(text) != -1:
            # adds for every match
            notes_count += 1
            # Makes list with every single note that matched the search to separate date and text
            note_array = note.split("***")

            # DATE. If note created Today, then text is TODAY Adds date as a <span>
            # inside a <p> tag
            if note_array[0] == today:
                note_date = "<p class=\"note__date\">Created: <span>Today<span></p>"
            else:
                note_date = "<p class=\"note__date\">Created: <span>" + \
                    note_array[0] + "<span></p>"

            # CONTENT. Gets the note text and puts it inside a <p> tag
            note_text = note_array[1].replace(
                "\n", "<br>")  # Keeping newlines in notes
            note_text = "<p class=\"note__text\">" + note_text + "</p>"

            # create note <div> with latest note created appearing first in the list
            full_text = "<div class=\"note\">" + note_date + note_text + "</div>" + full_text
    
    # Produces the final text to add to the page with the results
    if full_text != "":
        full_text = "<h3>Notes found: " + str(notes_count) + "</h3 >" + full_text

    # If there are no results adds the <div> and <p> tags with the no matches message
    else:
        full_text = "<h3>Notes found: " + str(notes_count) + \
            "</h3> <div class=\"note\"> <p class=\"note__text\">Sorry! there are no results that match your search.</p> </div>"

    # Returns the full block
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
    # get the .html file with the corresponding page name
    html_file = open(page_name + ".html")
    # get the content
    content = html_file.read()
    # close de file
    html_file.close()
    # return the content
    return content

# === ROUTE FUNCTIONS ===
# = Homepage =
@app.route("/")
def homepage():
    return get_html("index").replace("{$$ SUBMITED $$}", "")

# = Add note page =
@app.route("/addnote", methods=['GET', 'POST'])
def addnote():
    # get the note's text
    note_text = flask.request.form['new_note']
    # Get the page
    html_page = get_html("index")
    
    # variable to store the page's text to return
    page_text = ""

    # This Loop replaces the {$$ SUBMITED $$} in the layout depending 
    # on the content of the textbox. If the textbox is empty go to "else"
    if note_text != "":
        # Gets note without trailing white-spaces
        create_note(note_text.strip())
        # get the page text, replacing the {$$ SUBMITED $$} with message
        page_text = html_page.replace(
            "{$$ SUBMITED $$}", '<p class="form__saved"> Your note has been saved</p>')
    else:
        # replaces the {$$ SUBMITED $$} with empty string
        page_text = html_page.replace("{$$ SUBMITED $$}", "")
    
    # returns the page text
    return page_text

# = Search for notes page =
@app.route("/search")
def search():
    # Get user search element, takes out trailing white-spaces and converts to lowercase
    search_text = flask.request.args.get("q").strip().lower()
    # get html text
    html_page = get_html("search")
    # search using the search function created above
    notes_text = search_note(search_text)

    #return the page's content with the {$$ NOTES $$} replaced by result's list
    return html_page.replace("{$$ NOTES $$}", notes_text)
    
    
# = Show full list =
@app.route("/all_notes")
def all_notes():
    # Get same html as search
    html_page = get_html("search")
    # get all notes using an empty search
    notes_text = search_note("")
    # return the page's content with the {$$ NOTES $$} replaced by the full list
    return html_page.replace("{$$ NOTES $$}", notes_text)
