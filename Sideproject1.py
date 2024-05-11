import sqlite3
import requests
import json

#კოდს მოაქვს რენდომ ხუმრობა ჩაკ ნორისის შესახებ API-დან, რესფონსის JSON ვერსიას ინახავს ფაილში, თავად ხუმრობას კი ბაზაში.
#API საჯაროა და Key-ს არ საჭიროებს.

category = "science"
url = f"https://api.chucknorris.io/jokes/random?category={category}"
path = "info.json"
path2 = "Sideproject.sqlite"


def get_info(url):

    response = requests.get(url)
    statuscode = response.status_code
    header = response.headers
    info = response.json()

    print(f'სტატუსის კოდი : {statuscode} ')
    print(f"თარიღი - {header['Date']}\n"
          f"კონტენტისა და სიმბოლოების ტიპი - {header['Content-Type']}")
    print(f"ხუმრობა - {info['value']}")

    return

def save_into_file(path, url):
    data = requests.get(url).json()

    with open(path, "w") as file:
        json.dump(data, file, indent=4)

def save_info_database(path2, url):
    data = requests.get(url).json()

    conn = sqlite3.connect(path2)
    curr = conn.cursor()
    curr.execute('''CREATE TABLE if not exists Chuknorris (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           joke TEXT
       )''')

    info = data["value"]
    curr.execute("INSERT INTO Chuknorris (joke) VALUES (?)", (info,))

    conn.commit()
    conn.close()
    return

def main():
    get_info(url)
    save_into_file(path, url)
    save_info_database(path2, url)


if __name__ == "__main__":
    main()
