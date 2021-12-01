import pyjokes
import dateparser
from datetime import datetime
from Skills.todo import Todo, Item
from Skills.weather import Weather
from AI.Orchestration_engine.ai import AI

Helix = AI()
todo = Todo()


def joke():
    funny = pyjokes.get_joke()
    print(funny)
    Helix.say(funny)


def add_todo() -> bool:
    item = Item()
    Helix.say("Tell me what to add to the list")
    try:
        item.title = Helix.listen()
        todo.new_item(item)
        message = "Added " + item.title
        Helix.say(message)
        return True
    except:
        print("oops there was an error")
        return False


def list_todos():
    if len(todo) > 0:
        Helix.say("Here are your to do's")
        for item in todo:
            Helix.say(item.title)
    else:
        Helix.say("The to do list is empty!")


def remove_todo() -> bool:
    Helix.say("Tell me which item to remove")
    try:
        item_title = Helix.listen()
        todo.remove_item(title=item_title)
        message = "Removed " + item_title
        Helix.say(message)
        return True
    except:
        print("opps there was an error")
        return False


def weather():
    myweather = Weather()
    forecast = myweather.forecast
    # print(forecast)
    Helix.say(forecast)


def goodbye():
    Helix.say("goodbye, I am going to standby")


command = ""

while True and command != "goodbye":
    command = Helix.listen()
    print("command was:", command)

    try:
        command = Helix.listen()
        command = command.lower()
    except:
        print("oops there was an error")
        command = ""
    print("command was:", command)

    if command == "tell me a joke":
        joke()
        command = ""
    if command in ["add to-do", "add to do", "add item"]:
        add_todo()
        command = ""
    if command in ["list todos", "list todo", "list to do", "list to-do", "list to do's", 'list items']:
        list_todos()
        command = ""
    if command in ["remove todo", "remove item", "mark done", "remove todos", "remove to-do", "remove to do's"]:
        remove_todo()
    if command in ['what is the weather like', 'give me the forecast', "what's the weather"]:
        weather()

    if command in ['good morning', 'good evening', 'good night', 'good afternoon']:
        now = datetime.now()
        hr = now.hour
        if hr <= 0 <= 12:
            message = "Morning"
        if hr >= 12 <= 17:
            message = "Afternoon"
        if hr >= 17 <= 21:
            message = "Evening"
        if hr > 21: message = "Night"

        message = "Good " + message + " Kevin"
        Helix.say(message)
        weather()
        list_todos()
        joke()

    if command in ['goodbye', 'shut up', 'stop']:
        goodbye()
