import os
import random
from datetime import datetime
import utils.arrays
import time
import PySimpleGUI as sg

from googlesearch import search

from utils.startup import setup
from utils.rules import reset_all_last_used_reassembly_rule
from utils.response import prepare_response, generate_response

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = os.path.join(PROJECT_DIR, 'scripts')
GENERAL_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'general.json')
SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'doctor.json')

def main():
    memory_stack = []
    general_script, script, memory_inputs, exit_inputs = setup(GENERAL_SCRIPT_PATH, SCRIPT_PATH)

    sg.theme('LightBlue 1')
    sg.set_options(text_color="Black")
    layout = [[sg.Text('You: '), sg.Text(size=(50,1), key='-mytext-')],
          [sg.Text(''), sg.Text(size=(70,11), key='-CSI-')],
          [sg.Input(key='-myinput-', do_not_clear=False)],
          [sg.Button('Send message'), sg.Button('Bye!')]]

    window = sg.Window('Eliza Application', layout, [100, 50])

    # if true, search the next thing the user responds with
    searchactive = False
    
    # boolean for if the user is currently in the settings control loop
    settingsmode = False

    #Setting that the user can change to enable or disable the search tool and jokes
    searchsetting = "True"
    jokesetting = "True"

    # used for telling if the window is closed to exit the event loops or the bye button is pressed
    done = "False"

    # Randomizing Eliza's greeting
    random.seed(datetime.now().timestamp())
    greetingindex = random.randint(0,len(utils.arrays.greetingarray)-1)

    # Waiting for the user to press a button or close the application
    while True:
        event, values = window.read()
        print('event:', event)
        print('values:', values)
        window['-CSI-'].update(utils.arrays.displayNameSetting + utils.arrays.greetingarray[greetingindex])
        if event == 'Send message':
            break
        if event == sg.WIN_CLOSED or event == 'Bye!':
            window.close()
            in_str_l = "seeya"
            done = "True"
            break

    if done == "False":
        in_str = values['-myinput-']
        in_str_l = in_str.lower()
        print('in_str_l: ' + in_str_l)
        if in_str_l != "":
            window['-mytext-'].update(in_str_l)


    # Main execution loop
    while in_str_l not in exit_inputs:
        # str.lower().islower() is a fast way of checking
        # if a string contains any characters of the alphabet.
        # Source: https://stackoverflow.com/a/59301031

        # Waiting for the user to press a button or close the application
        while True:
            event, values = window.read()
            print('event:', event)
            print('values:', values)
    
            if event == 'Send message':
                break
            if event == sg.WIN_CLOSED or event == 'Bye!':
                window.close()
                done = "True"
                in_str_l = "seeya"
                break
        if done == "False":
            in_str = values['-myinput-']
            in_str_l = in_str.lower()
            print('in_str_l: ' + in_str_l)
            if in_str_l != "":
                window['-mytext-'].update(in_str_l)
            
            # if not in_str_l.islower():
                # response = prepare_response(utils.arrays.displayNameSetting + ': Please, use letters. I am human, after all.')
            
            if in_str_l == 'reset':
                reset_all_last_used_reassembly_rule(script)
                utils.arrays.displayNameSetting = "Eliza"
                searchsetting = "True"
                jokesetting = "True"
                response = prepare_response(utils.arrays.displayNameSetting + ': Reset complete.')

            # keywords to enter the settings control loop
            elif in_str_l == 'settings' or in_str_l == "setting":
                settingsmode = True
                namechange = False
                searchmodechange = False
                jokemodechange = False
                window['-CSI-'].update("\n----------Settings----------\n>Chat Bot Name: " + utils.arrays.displayNameSetting + "\n>Search Tool Active: " + str(searchsetting) + "\n>Jokes Active: " + jokesetting + "\n" + utils.arrays.displayNameSetting + ': Which setting would you like to change? (to exit, type "exit")')
                # print("\n----------Settings----------\n>Chat Bot Name: " + utils.arrays.displayNameSetting + "\n>Search Tool Active: " + str(searchsetting) + "\n>Jokes Active: " + jokesetting + "\n")
                # response = prepare_response(utils.arrays.displayNameSetting + ': Which setting would you like to change? (to exit, type "exit")')
                while settingsmode == True:

                    # Waiting for the user to press a button or close the application
                    while True:
                        event, values = window.read()
                        print('event:', event)
                        print('values:', values)
        
                        if event == 'Send message':
                            break
                        if event == sg.WIN_CLOSED or event == 'Bye!':
                            window.close()
                            done = "True"
                            in_str_l = "seeya"
                            break
            
                    in_str = values['-myinput-']
                    print('in_str_l: ' + in_str_l)
                    if in_str_l != "":
                        window['-mytext-'].update(in_str_l)

                    if namechange == True:
                        utils.arrays.displayNameSetting = in_str
                        namechange = False

                    if searchmodechange == True and in_str in ["True", "False"]:
                        searchsetting = in_str
                        searchmodechange = False

                    if jokemodechange == True and in_str in ["True", "False"]:
                        jokesetting = in_str
                        jokemodechange = False

                    in_str_l = in_str.lower()

                    if in_str_l == 'exit':
                        settingsmode = False

                    elif in_str_l in utils.arrays.namesettingarray:
                        response = prepare_response(utils.arrays.displayNameSetting + ': what would you like to change my name to be?')
                        namechange = True

                    elif in_str_l in utils.arrays.searchtoolsetting:
                        response = prepare_response(utils.arrays.displayNameSetting + ': Enter "True" or "False" to enable or disable the search feature.')
                        searchmodechange = True

                    elif in_str_l in utils.arrays.jokesettingarray:
                        response = prepare_response(utils.arrays.displayNameSetting + ': Enter "True" or "False" to enable or disable the jokes feature.')
                        jokemodechange = True

                    else:
                        # print("\n----------Settings----------\n>Chat Bot Name: " + utils.arrays.displayNameSetting + "\n>Search Tool Active: " + str(searchsetting) + "\n>Jokes Active: " + jokesetting + "\n")
                        response = prepare_response("\n----------Settings----------\n>Chat Bot Name: " + utils.arrays.displayNameSetting + "\n>Search Tool Active: " + str(searchsetting) + "\n>Jokes Active: " + jokesetting + "\n" + utils.arrays.displayNameSetting + ': Which setting would you like to change? (to exit, type "exit")')
                    window['-CSI-'].update(response)
                response = prepare_response(utils.arrays.displayNameSetting + ': Thank you for changing settings. Is there anything else you wanted to talk about?')

            # keywords to enter the google search control loop
            elif "resource" in in_str_l or "info" in in_str_l or "search" in in_str_l and searchsetting == "True":
                resource = True
                response = prepare_response(utils.arrays.displayNameSetting + ': Would you like me to find additional resources to help you?')
                window['-CSI-'].update(response)
                while resource == True:

                    # Waiting for the user to press a button or close the application
                    while True:
                        event, values = window.read()
                        print('event:', event)
                        print('values:', values)
        
                        if event == 'Send message':
                            break
                        if event == sg.WIN_CLOSED or event == 'Bye!':
                            window.close()
                            done = "True"
                            in_str_l = "seeya"
                            break
            
                    in_str_l = values['-myinput-']
                    print('in_str_l: ' + in_str_l)
                    if in_str_l != "":
                        window['-mytext-'].update(in_str_l)
            
                    if searchactive == True:
                        # Eliza searches for whatever is in the input string and resets to a defaut state
                        response = utils.arrays.displayNameSetting + ": Let me take a look.\n"
                        for j in search(in_str_l, num_results=3):
                            response = response + "       " + j + "\n"
                        response = response + utils.arrays.displayNameSetting + ": Are any of these helpful?"
                        searchactive = False
                        resource = False

                    # if the user responds with anything close to "yes", then Eliza asks what they want to search for
                    elif in_str_l in utils.arrays.acceptarray:
                        response = prepare_response(utils.arrays.displayNameSetting + ": What would you like me to search for?")
                        searchactive = True

                    # if the user responds with anything close to "no", Eliza cancels the search
                    elif in_str_l in utils.arrays.declinearray:
                        response = prepare_response(utils.arrays.displayNameSetting + ": Alright, if you want me to search for anything, just ask.")
                        resource = False
                        
                    # if the user responds with something not resembling "yes" or "no", Eliza asks again
                    else:
                        response = prepare_response(utils.arrays.displayNameSetting + ": I'm sorry, I dont seem to understand. Would you like me to find additional resources for you?")
                    window['-CSI-'].update(response)

            # joke control loop
            elif "joke" in in_str_l and jokesetting == "True":
                jokeactive = True
                response = prepare_response(utils.arrays.displayNameSetting + ': Would you like me to tell you a joke?')
                window['-CSI-'].update(response)
                while jokeactive == True:

                    # Waiting for the user to press a button or close the application
                    while True:
                        event, values = window.read()
                        print('event:', event)
                        print('values:', values)
        
                        if event == 'Send message':
                            break
                        if event == sg.WIN_CLOSED or event == 'Bye!':
                            window.close()
                            done = "True"
                            in_str_l = "seeya"
                            break
            
                    in_str_l = values['-myinput-']
                    print('in_str_l: ' + in_str_l)
                    if in_str_l != "":
                        window['-mytext-'].update(in_str_l)

                    # if the user responds in some form of yes, start the joke
                    if in_str_l in utils.arrays.acceptarray:
                        jokeindex = random.randint(0,len(utils.arrays.jokearray)-1)
                        response = prepare_response(utils.arrays.displayNameSetting + utils.arrays.jokearray[jokeindex])
                        punchline = True
                    # if the user says no, leave the control loop
                    elif in_str_l in utils.arrays.declinearray:
                        response = prepare_response(utils.arrays.displayNameSetting + ": Alright, What else would you like to talk about?")
                        jokeactive = False
                    # say the punchline
                    elif punchline == True:
                        response = prepare_response(utils.arrays.displayNameSetting + utils.arrays.punchlinearray[jokeindex])
                        punchline = False
                        jokeactive = False
                    window['-CSI-'].update(response)

            else:
                response = generate_response(in_str_l, script, general_script['substitutions'], memory_stack, memory_inputs)

            window['-CSI-'].update(response)

    # randomizing Eliza's goodbye message
    goodbyeindex = random.randint(0,len(utils.arrays.goodbyearray)-1)
    print(utils.arrays.displayNameSetting + utils.arrays.goodbyearray[goodbyeindex])

if __name__=="__main__":
   main()