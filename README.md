# Flask Backend 

This project implements a RESTful Flask API for Access Camp.  
It provides backend functionality for managing:

- Campers
- Activities
- Signups linking campers to activities at specific hours

This assessment focuses on backend development only.  
No frontend is required or included.

---

## Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Pytest

---

## Installation and Setup

Clone the repository and set up the environment:

```bash
git clone <repository-link>
cd <repository-name>

python3 -m venv env
source env/bin/activate        # Mac/Linux
# or
.\env\Scripts\activate         # Windows

pip install -r requirements.txt
````

---

## Database Setup

Run the following commands inside the project:

```bash
cd server
flask db init
flask db migrate -m "initial model"
flask db upgrade
```

Optional: seed the database

```bash
python -m server.seed
```

---

## Running the API

From the project root:

```bash
python server/app.py
```

The API will run on:

```
http://localhost:5555
```

---

## API Endpoints

### Campers

| Method | Route         | Description                      |
| ------ | ------------- | -------------------------------- |
| GET    | /campers      | List all campers                 |
| GET    | /campers/<id> | Camper details including signups |
| POST   | /campers      | Create a new camper              |
| PATCH  | /campers/<id> | Update camper information        |

### Activities

| Method | Route            | Description                            |
| ------ | ---------------- | -------------------------------------- |
| GET    | /activities      | List all activities                    |
| POST   | /activities      | Create a new activity                  |
| DELETE | /activities/<id> | Delete activity and associated signups |

### Signups

| Method | Route    | Description     |
| ------ | -------- | --------------- |
| POST   | /signups | Create a signup |

---

## Validation Rules

### Camper

* Name is required
* Age must be an integer between 8 and 18 (inclusive)

### Signup

* Time must be an integer between 0 and 23

---

## Error Responses

Invalid input returns:

```json
{"errors": ["validation errors"]}
```

Not found responses return:

```json
{"error": "Camper not found"}
```

or

```json
{"error": "Activity not found"}
```

---

## Running Tests

```bash
pytest -x
```

All tests should pass.

---

## Assessment Requirements Met

This project includes:

* Flask API only
* MVC structure
* SQLAlchemy ORM models
* Relationships:

  * Camper has many Activities through Signups
  * Activity has many Campers through Signups
  * Signup belongs to both
* Cascade delete behavior
* Migrations with Flask-Migrate
* Input validations
* Standardized JSON responses
* Automated testing with pytest

---

## License

For educational use.