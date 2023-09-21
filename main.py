from flask import Flask, send_file
from faker import Faker
from setings import seting_customers, seting_tracks
import csv
import requests


app = Flask(__name__)


@app.route('/')
def main_page():
    return (
        "<p>Главная:\n"
        "<p>Для файла requrements.txt /requrements/"
        "<p>Для генерации, напишите вашу цифру /users/generate/"
        "<p>Средний рост, вес из файла hw.csw /mean/"
        "<p>Чтоб увидеть космонавтов /space/"
    )


@app.route('/requrements/', methods=['GET'])
def requrements():
    return send_file('tables_and_txt/requrements.txt', as_attachment=False)


@app.route('/users/generate/<int:generate>', methods=['GET'])
def user_generation(generate: int):
    fake = Faker()
    user_digit = generate

    default_quantity = [[fake.name(), fake.company_email()] for _ in range(100)]
    user_quantity = [[fake.name(), fake.company_email()] for _ in range(user_digit)]

    if user_digit > 0:
        return user_quantity

    return default_quantity


@app.route('/mean/', methods=['GET'])
def mean():
    get_file = 'tables_and_txt/hw.csv'
    heights = []
    weights = []

    with open(get_file, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            try:
                heights.append(float(row[1]))
                weights.append(float(row[2]))

            except (ValueError, IndexError):
                continue

    mean_height = sum(heights) / len(heights) * 2.54
    mean_weight = sum(weights) / len(weights) * 0.453592

    return (f"<p>Средний рост: {mean_height} см"
            f"<p>Средний вес: {mean_weight} кг")


@app.route('/space/', methods=['GET'])
def cosmonaut_count():
    get_response = requests.get('http://api.open-notify.org/astros.json')
    response_in_json = get_response.json()
    numbers_cosmonaut = response_in_json.get('number')

    names = []
    for person in response_in_json.get('people'):
        names.append(person['name'])

    return f"Кол-во космонавтов {numbers_cosmonaut}, вол-во после {len(names)}"


@app.errorhandler(404)
def error_404(error):
    return '<h1 style="text-align:center; font-size:24px;">Ошибка((</h1>'


if __name__ == "__main__":
    seting_customers()
    seting_tracks()
    app.run(debug=True)