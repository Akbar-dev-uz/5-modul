# 5-modul

pybabel extract -o locales/messages.pot .

pybabel init -i locales/messages.pot -d locales -l en
pybabel init -i locales/messages.pot -d locales -l ru
pybabel init -i locales/messages.pot -d locales -l uz


[
pybabel extract -F babel.cfg -o locales/messages.pot .
pybabel update -i locales/messages.pot -d locales
]
    
    👆нужно запускать всякий раз,
    когда ты добавляешь или изменяешь текст,
    обёрнутый в _() или gettext() в своём коде.


pybabel compile -d locales

    👆после перевода