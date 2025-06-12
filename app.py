# I tried using sqlAlchemy to work with my database but I never used it so I used ChatGPT's help for that
# I also used ChatGPT's help to work with the nexar API and also for some tweaks in the code
import os
import requests

from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Component, db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'components.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
NEXAR_CLIENT_ID = 'seu_client_id'
NEXAR_CLIENT_SECRET = 'seu_client_secret'

# API function for search components if it's not inside the db
def get_nexar_token():
    url = 'https://identity.nexar.com/connect/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': '4013dc26-ec85-4255-b815-fcc3fe418abc',
        'client_secret': 'BLYzdJQ_qjr299SMdIGQE53PBkkzLNmczz7v',
        'scope': 'supply.domain'
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')

def search_nexar_component(query, token):
    url = 'https://api.nexar.com/graphql'
    headers = {'Authorization': f'Bearer {token}'}
    graphql_query = {
        "query": """
        query SearchParts($q: String!) {
            supSearch(q: $q, limit: 1) {
            results {
              part {
                mpn
                manufacturer {
                  name
                }
                specs {
                  attribute {
                    name
                  }
                  displayValue
                }
              }
            }
          }
        }
        """,
        "variables": {"q": query}
    }
    response = requests.post(url, json=graphql_query, headers=headers)
    return response.json()

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/search', methods=["GET", "POST"]) 
# for this route I use ChatGPT for help, mainly because of the use of Nexar API, and some other points just for questions
def search():
    query = request.form.get("query", "").strip() or request.args.get("query", "").strip()
    category = request.form.get("category")
    voltage_min = request.form.get("voltage_min", type=float)
    voltage_max = request.form.get("voltage_max", type=float)
    current_min = request.form.get("current_min", type=float)
    current_max = request.form.get("current_max", type=float)

    filters = []

    if query:
        filters.append(Component.name.ilike(f"%{query}%"))
    if category:
        filters.append(Component.category == category)
    if voltage_min is not None:
        filters.append(Component.voltage_max >= voltage_min)
    if voltage_max is not None:
        filters.append(Component.voltage_min <= voltage_max)
    if current_min is not None:
        filters.append(Component.current_max >= current_min)
    if current_max is not None:
        filters.append(Component.current_min <= current_max)

    results = Component.query.filter(*filters).all()
    error_message = None

    if not results and query:
        # Fallback: Nexar API
        token = get_nexar_token()
        nexar_data = search_nexar_component(query, token)

        if 'errors' in nexar_data:
            error_message = nexar_data['errors'][0].get('message', 'Unknown error from Nexar')
            return render_template("search.html", query=query, results=[], external=True, error=error_message)

        #print("Nexar answer:", nexar_data)  # DEBUG
        part_info = nexar_data.get('data', {}).get('supSearch', {}).get('results', [])

        if part_info:
            part = part_info[0]['part']

            specs = {spec['attribute']['name']: spec['displayValue'] for spec in part.get('specs', [])}
            voltage_min = voltage_max = current_min = current_max = None

            for key, value in specs.items():
                try:
                    if "Voltage" in key and "Min" in key:
                        voltage_min = float(value.split()[0])
                    elif "Voltage" in key and "Max" in key:
                        voltage_max = float(value.split()[0])
                    elif "Current" in key and "Min" in key:
                        current_min = float(value.split()[0])
                    elif "Current" in key and "Max" in key:
                        current_max = float(value.split()[0])
                except:
                    pass

            datasheets = part.get('datasheets')
            datasheet_link = datasheets[0]['url'] if datasheets else 'N/A'

            new_component = Component(
                name=part.get('mpn'),
                category=part.get('manufacturer', {}).get('name'),
                voltage_min=voltage_min,
                voltage_max=voltage_max,
                current_min=current_min,
                current_max=current_max,
                datasheet_link=datasheet_link,
                notes="Import via Nexar"
            )

            db.session.add(new_component)
            db.session.commit()

            results = [new_component]
            return render_template("search.html", query=query, results=results, external=True, error=error_message)

    return render_template("search.html", query=query, results=results, external=False, error=error_message)


# with DRY to minimize the number of routes
# I've never used this before, but I love this variable page concept.
@app.route('/category/<cat>')
def category(cat):
    components = Component.query.filter_by(category=cat).all()
    #print("category of url:", cat)
    #print("components:", components)
    return render_template("category.html", components=components, category=cat)


@app.route("/debug")
def debug():
    components = Component.query.all()
    return "<br>".join([f"{c.id}: {c.name}" for c in components])

#print(os.path.abspath("components.db"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)