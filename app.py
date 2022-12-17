import json
from flask import Flask, jsonify, session, sessions, g, request, render_template, redirect, flash
from random import randint

from stories import Story
from surveys import Survey
from surveys import satisfaction_survey
from surveys import Question
from boggle import Boggle

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "ratatouille"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False #for the redirect() old home page.

# debug = DebugToolbarExtension(app)

# since this app'name is NOT 'app.py' we need to define en environment variable when launching flask server run:
#  FLASK_APP=myapp.py flask run

# Running the app in debug mode will show an interactive traceback and console in the browser when there is an error. As of Flask 2.2, to run in debug mode, pass the --app and --debug options to the flask command.

# $ flask --app example --debug run
# Prior to Flask 2.2, this was controlled by the FLASK_ENV=development environment variable instead. You can still use FLASK_APP and FLASK_DEBUG=1 instead of the options above.

# For Linux, Mac, Linux Subsystem for Windows, Git Bash on Windows, etc.:

# $ export FLASK_APP=example
# $ export FLASK_DEBUG=1 //// THIS CAN BE SET INSIDE .profile (linux) or .bash_profile (MAC OS)
# $ flask run

# For Windows CMD, use set instead of export:

# set FLASK_DEBUG=1
# For PowerShell, use $env:

# $env:FLASK_DEBUG = "1"

# print("-------------HELLO!----------------")

# creating a route

@app.route("/")  # these routes listen to GET requests only
def home_page():
    return render_template("home.html")

@app.route("/hello")  # we add a decorator called "hello"
def hello():
    return render_template("/hello.html")

@app.route("/lucky")
def lucky_number():
    num=randint(1, 5)
    msg="IS THIS YOUR LUCKY NUMBER?" #can pass msg with flash()
    flash(msg)
    return render_template("lucky.html", lucky_num=num, msg=msg) #can pass msg as third rendered argument

@app.route("/goodbye")
def say_goodbye():
    return """
<h1 style="color:red;">GOOD BYE!</h1>
"""

@app.route("/search")
def search():
    term = request.args["term"]
    sort = request.args["sort"]
    # use term to find db data that matches term
    return f"<h1>Search results for: {term}</h1> <p>Sorting by {sort}</p>"

@app.route("/spell/<word>")
def spell(word):
    return render_template("spell.html", word=word.upper())

@app.route("/spellfromform", methods=["POST"])
def spell_from_form():
    word = request.form["wordfromform"]
    return render_template("spell.html", word=word.upper())

@app.route("/add-comment")
def add_comment_form():
    return """
    <form method="POST">
        <h1>Add Comment</h1>
            <input type="text" placeholder="comment" name="comment"/>
            <input type="text" placeholder="username" name="username"/>
        <button>Submit</button>
    </form>
    """

@app.route("/add-comment", methods=["POST"])
def save_comment():
    print(request.form)
    comment = request.form["comment"]
    username = request.form["username"]
    return f"""
    <h1>Comment submited and saved!</h1>
    <p>{username}'s last comment: <b><i>"{comment}"</i></b></p>
    """

# PATH VARIABLE
@app.route("/r/<subreddit>")
def show_subreddit(subreddit):    
    #here we would write some logic to find the 'subreddit' value in a db    
    return f"this is a subreddit for <b>{subreddit}</b>"

@app.route("/r/<subreddit>/comments/<post_id>")
def show_comments(subreddit, post_id):
    return f"<h1>Viewing comments for for post with id: {post_id} from the {subreddit} Subreddit</h1>"

#let's create a data structure 
POST = {
    1:"I like chocolate", 
    2:"I like flask, it's cool",
    3:"Hey dude!",
    4:"My daughters are awesome!"
}

@app.route("/posts/<int:id>") 
#beware of data type 'int' here! in path variable default are STRINGS!
def find_post(id):
    post = POST[id] 
    return f"""
    <p>{post}</p>
    """
        

@app.route("/storyform")
def form():
    return render_template("storyform.html")

@app.route("/story")
def set_story():
    # place = request.args["Place"]
    # noun = request.args["Noun"]
    # verb = request.args["Verb"]
    # adjective = request.args["Adjective"]
    # plural_noun = request.args["Plural-noun"]
    
    # arguments = {
    #     "Place":place, 
    #     "Noun":noun, 
    #     "Verb":verb, 
    #     "Adjective":adjective, 
    #     "Plural-noun":plural_noun
    #     }
       
    
    text = Story.create(request.args) #dict like object already...
    
    print(f"text = {text}")
    
    return render_template("story.html", text=text)
    
@app.route("/old-home-page")
def redirect_old_home():
    """Redirect to new home page"""
    return redirect("/")
    
MOVIES = {
    "Amadeus",
    "Armageddon", 
    "Dances with wolves"
} # converted to a set with {} instead of [] allows to easily enforce unique titles

@app.route("/movies")
def shwo_movies():
    """Show list of all movies in fake DB"""
    return render_template("movies.html", movies=MOVIES)

@app.route("/movies/new", methods=["POST"])
def add_movie():
    title = request.form['title']
    
    if title in MOVIES:
        flash(f"{title} already exists!", "error") # we can pass a category to style the message
        # SEE: https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/
    else:
        flash("MOVIE ENTRY CREATED!", "success")
    
    #add to pretend db
    # MOVIES.append(title) # can't use append since now it's a set()
    MOVIES.add(title)       
    
    # return render_template("movies.html", movies=MOVIES) THIS IS BAD because would re-add 
    # the same entry upon every page refresh!     
    
    # THAT'S WHY WE USE REDIRECT:
    return redirect("/movies")


# RESPONDING WITH JSON #
@app.route("/movies/json")
def get_movies_json():
    return jsonify(list(MOVIES))


############################## SURVEY ##################################
responses = []
username = ""

@app.route("/survey")
def home():   
    responses.clear()
    print(f"responses cleared!{responses}")
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    if not session.get("username"):
        return render_template("user_form.html")
    else:
        username = session.get("username", "")
        session["responses"] = {username:[]}
        return render_template("home_survey.html", title=title, instructions=instructions, username=username)

@app.route("/handle_user_form")
def handle():
    print(f"********** USER NAME IS: {request.args['username']}")
    session["username"] = request.args["username"]
    return redirect("/survey")

@app.route("/restart")
def restart():
    session.clear()  
    return redirect("/survey")
    
@app.route("/questions/0")  # starting point
def zero():
    params = parseQuestions(0)
    session["lastquestion"] = 0
    

    nextq = f"/questions/1"
    return render_template("/questions.html", question=params[0], choices=params[1], comment=params[2], nextq=nextq)


@app.route("/questions/<int:q>")
def quest(q):

    last_quest = session["lastquestion"]

    if not session.get("same_page_reload", False):
        expect_nextq = last_quest + 1
        wrong = q != expect_nextq
        print(f"last_quest ===========> {last_quest}")
        print(f"this question ==========> {q}")
        print(f"------------- wrong? ====> {wrong}")

        if wrong:
            print(
                f"---------wrong consecutive question, {q} instead of {expect_nextq} redirecting to /questions/{expect_nextq}")
            return redirect(f"/questions/{expect_nextq}")

    arr_len = len(satisfaction_survey.questions)

    arguments = request.args
    print(f"-----------arguments= {arguments}")
    print(f"+++++++++++ {session.get('same_page_reload')}")
    if not arguments:
        print(f"*****************************NO ARGS")
        
        
        empty_resp = session.get("emptyresponse", 0)
        
        if empty_resp > 5:            
            flash(f"You must select a response for every question", "error")
            flash(f"number of empy responses: {empty_resp}", "error")
            return redirect(f"/questions/{q-1}?null")        
        else:
            session["emptyresponse"] = empty_resp + 1
            flash("Select a response...", "error")
            flash(f"number of empy responses: {empty_resp}", "error")
            return redirect(f"/questions/{q-1}?null")
        
    session["lastquestion"] = q

    response = list(arguments)[0]
    print(f"-----------response= {response}")
    
    append_response(response)

    print(f" q = {q} | arr_len = {arr_len}")
    if (q == arr_len):
        
        responses = get_responses(session.get("username", ""))
        print(f"responses= {responses}")
        return render_template("thanks.html", responses=responses, questions=satisfaction_survey.questions)

    nextq = f"/questions/{q+1}"
    params = parseQuestions(q)
    return render_template("/questions.html", question=params[0], choices=params[1], comment=params[2], nextq=nextq)


def parseQuestions(q):
    instance = satisfaction_survey.questions[q]
    question = instance.question
    choices = instance.choices
    comment = instance.allow_text
    return [question, choices, comment]

def append_response(response):
    username = session.get("username", "")
    print(f"/***************************************\ username = {username}")
    responses = get_responses(username)
    print(f"/***************************************\ responses = {responses}")
    responses.append(response) # append the list
    
    session["responses"] = {username:responses} # recreate the dict and store it
    
def get_responses(username):
    r = session["responses"] # {username:[]}
    print(f"/***************************************\ r = {r}")
    responses = r[username] # []
    return responses


############################## BOGGLE ##################################

boggle_game = Boggle()

hits = 0
score = 0



@app.route("/boggle")
def boggle_home():
    """Home page: 
    - shows a button to clear all game data
    - generates a new game board
    - sets the game number
    - updates the stats (score and hits) for future reference at the end of the game
    """
    clear_session()
    board = get_new_board()
    setStats()
    return render_template("index_boggle.html")    


@app.route("/game_page")
def new_game(): 
    """Method that displays the game's page and board
    
    """
          
    return render_template("boggle.html", board=session["board"])

@app.route("/check-word")
def get_word():
    """Handles user's input"""
    
    print(f"request.args : {request.args}")
    
    word = request.args['word'] 
    
    print("***********************************")
    print(f"checking this word: {word}")
    print("***********************************")
    
    
    board = session["board"]
    resp = boggle_game.check_valid_word(board, word)
    print(f"wordstatus ? ===> {resp}")
    return jsonify({"result":resp})
    
@app.route("/newboard")  
def new():
    """method that allows users to start a new game without having to go back to the home page"""    
    get_new_board()  
    setStats()      
    return redirect("/game_page")

@app.route("/clear/<ingame>")
def cl(ingame):
    """Method by which users can call clear_session()"""   
    
    if ingame == "true":
        board_bkup = session["board"] # save a copy of the board (this is an "in game" call)
        clear_session()
        session["board"] = board_bkup # restore backup
        return redirect("/game_page") # basically stay on the same page
    else:
        clear_session()
        get_new_board() # must not leave board value empty
        return redirect("/boggle")

@app.route("/endgame", methods=["POST"])
def end():
    """End of game handler:
    - retrieves game number
    - retrieves number of hits
    - retrieves the final score
    - parse those 3 values into a dictionary {"game_number":{"hits":hits, "score":score}}
    """
    game_numb = session["game_numb"]
    hits = request.json["hits"]
    score = request.json["score"]
    
    stats = session["stats"]
    stats[f"{game_numb}"] = {"hits":hits, "score":score}
    
    session["stats"] = stats
    
    print("********************************")
    print(f"stats => {stats}")
    print("********************************")
    
    return jsonify(stats)    
    

def get_new_board():
    """Function that generates the board by calling the boggle_game class's instance"""
    b = boggle_game.make_board()
    session["board"] = b
    return b    

def setStats():
    game_number = session.get("game_numb", 0) 
    
    if game_number == 0:
        session["game_numb"] = 1
        game_number = 1
    else:
        session["game_numb"] = game_number + 1
        game_number = game_number + 1
    
    print("**************************************")
    print(f"This is game number: {game_number}")
    print("**************************************")
       
    print("**************************************")
    print(f"session.get('stats'): {session.get('stats')}")
    print("**************************************")
    
    stats = session.get("stats")    
    if stats == None:
        stats = {"1":{"hits": 0, "score": 0}}
        
    print("**************************************")
    print(f"stats ============> {stats}")
    print("**************************************")
        
    stats[f"{game_number}"] = {"hits":hits, "score":score}
    session["stats"] = stats
    print(f"ADDING NEW GAME-------------------- {stats}") 
    
def clear_session():
    """Function by which the player will reset the game history and all its data"""
    session.clear()
    
##################################### FOREX CONVERTER #######################################

from currencies import Converter, codes, checkString, all_rates
import re # regex

@app.route("/forex", methods=["POST", "GET"])  
def forex_home_page():
    """Route that renders a forex converter form """
    currencies = codes() #get the list of currencies from currencies.py to build the drop down menus
    rates = all_rates()
    
    return render_template("forex_home.html", currencies=currencies, rates=rates)

@app.route("/convert", methods=["POST"])
def conv():
    
    """Route that 
    1. requests POST data from the form
    2. returns the conversion result
    """
    currencies = codes() #get the list of currencies from currencies.py to preserve the drop down menus
    rates = all_rates()
    
    FROM = request.form.get("FROM")
    TO = request.form.get("TO") 
    amount = request.form.get("amount")
    
    # we must check if entry is a number. Pb: it's always a string to begin with. 
    # So we use a dedicated function with a regex test
                           
    if not checkString(amount):
        flash("ENTER A VALID NUMBER!", "error")
        return render_template("forex_home.html", currencies=currencies, result="invalid entry", rates=rates)
        
    print("*******************************************")
    print(f"     FROM = {FROM}"                        )
    print(f"     TO = {TO}"                            )
    print(f"     amount = {amount}"                    )
    print("*******************************************")
    
    result = Converter(FROM, TO, amount).convert()
    
    return render_template("forex_home.html", currencies=currencies, result=result, rates=rates)
    
