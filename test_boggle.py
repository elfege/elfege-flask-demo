from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        """ test that the home page is loading properly
            and that the board is of the right size

        """
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()

            res = client.get("/boggle")
            # html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(session["board"]), 5)

    def test_newBoggle(self):
        """
                ** the new game page is loaded
                ** the game number is incremented 1000 times
        """
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()
            
            # home must be called so as to define the board which is then called
            # and loaded by /game_page
            client.get("/boggle")

            with client.session_transaction() as change_session:
                change_session["game_numb"] = 999  # test 1000 games!
                print("------------------------------------------------------------------------------------------------")
                print(f"change_session['game_numb'] ==========> {change_session['game_numb']}")
                print("------------------------------------------------------------------------------------------------")


            res = client.get("/newboard")
            self.assertEqual(res.status_code, 302)

            # test 1000 games!
            self.assertEqual(session["game_numb"], 1000)

    def test_check_guess(self):
        """test for a valid, invalid and inexistent word"""
        with app.test_client() as client:

            with client.session_transaction() as sess:
                sess["board"] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
                print("")
                print("----------------*****----------------------")
                print(f"             board => {sess['board']}")
                print("----------------*****----------------------")
                print("")

            # import pdb
            # pdb.set_trace()

            # test a valid word
            response = client.get("/check-word?word=cat")
            print("*************************************")
            print(f"         response from '/check-word?word=cat': {response}")
            print("*************************************")
            self.assertEqual(response.json['result'], 'ok')
            
            
            # test an invalid word (not-on-board)
            response = client.get("/check-word?word=tart")
            print("*************************************")
            print(f"         response: {response}")
            print("*************************************")
            self.assertEqual(response.json['result'], 'not-on-board')
            
            
             # test an inexistent word (not-word)
            response = client.get("/check-word?word=tata")
            print("*************************************")
            print(f"         response: {response}")
            print("*************************************")
            self.assertEqual(response.json['result'], 'not-word')
            

