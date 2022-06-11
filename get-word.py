from wiktionaryparser import WiktionaryParser
import sys

text_to_find = ''
if len(sys.argv) > 1:
    text_to_find = str(sys.argv[1])

HTML1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + text_to_find + """</title>
    <style>
        p {
            padding: 10px;
            box-sizing: border-box;
        }
        textarea{
            width: 1496px;
            height: 88px;
            min-height: 100px;
            box-sizing: border-box;
            padding: 5px;
            margin: 0px;
            border-radius: 10px;
            border: 1px solid gray;
            resize: vertical;
            padding-left: 60px;
        }
        
        input {
            width: 100%;
            height: auto;
            min-height: 50px
            box-sizing: border-box;
            padding: 5px;
            margin: 0px;
            border-radius: 10px;
            border: 1px solid gray;
            padding-left: 60px;
        }

        .position-relative {
            position: relative;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        button {
            position: absolute;
            top: 22px;
            left: 3px;
            height: 21px;
            width: 50px;
            border-radius: 10px;
            border: 0px solid gray;
            font-size: 10px;
            cursor: pointer;
            background-color: rgb(200, 230, 255);
            transition: 0.5s;
        }

        button:hover {
            background-color: rgb(150, 200, 255);
        }
    </style>
    <script>
        function copy(id) {
            document.getElementById(id).select();
            document.execCommand('copy');
        }
    </script>
</head>
<body>
<p>
"""

HTML2 = """
</p>
</body>
</html>
"""

HTML3_1 = """
<div class="position-relative">
    <button onclick="copy('%id%')">Copy</button>
    <span class="label">%label%</span>
    <br>
    <input type='text' value='%value%' id="%id%"/>
</div>
"""

HTML3_2 = """
<div class="position-relative">
    <button onclick="copy('%id%')">Copy</button>
    <span class="label">%label%</span>
    <br>
    <textarea id="%id%">%value%</textarea>
</div>
"""

parser = WiktionaryParser()
word = parser.fetch(text_to_find, 'english')
parser.set_default_language('english')
'''parser.exclude_part_of_speech('noun')
parser.include_relation('alternative forms')'''

if len(word) > 0:
    details = word[0]

    etymology = details["etymology"]
    pronunciation_text = details["pronunciations"]["text"]
    for item in pronunciation_text:
        if ("(Received Pronunciation) IPA: " in item):
            pronunciation_text = str(item).replace("(Received Pronunciation) IPA: ", "").split(",")[0]
    # print(word)
    verb_or_noun = details["definitions"][0]["partOfSpeech"]
    definition = ""
    counter = 0
    for item in details["definitions"][0]["text"]:
        counter += 1
        definition += str(counter) + ". " + str(item) + "\n"

    '''print(text_to_find)
    print(verb_or_noun)
    print(pronunciation_text)
    print(definition)
    print(etymology)'''

    with open("./index.html", "w+", encoding="utf-8") as f:
        f.write(HTML1)

        f.write(HTML3_1.replace("%value%", str(text_to_find)).replace("%id%", "word").replace("%label%", "Word"))
        f.write(HTML3_1.replace("%value%", str(verb_or_noun)).replace("%id%", "verb_nourn_etc").replace("%label%",
                                                                                                      "Verb, noun, ..."))
        f.write(HTML3_1.replace("%value%", str(pronunciation_text)).replace("%id%", "pronunciation").replace("%label%",
                                                                                                             "Pronunciation"))
        f.write(
            HTML3_2.replace("%value%", str(definition)).replace("%id%", "definition").replace("%label%", "Definition"))
        f.write(HTML3_2.replace("%value%", str(etymology)).replace("%id%", "etymology").replace("%label%", "Etymology"))

        f.write(HTML2)

    print("\"" + text_to_find + "\" found and saved.")
else:
    print("Nessun risultato per questa parola (\"" + text_to_find + "\").")
