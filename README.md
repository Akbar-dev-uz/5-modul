# 5-modul

pybabel extract -o translations/messages.pot main.py

pybabel init -i translations/messages.pot -d translations -l en
pybabel init -i translations/messages.pot -d translations -l ru

pybabel compile -d translations
