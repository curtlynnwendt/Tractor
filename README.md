# Tractor Advisor

Simple Flask app to help a farmer choose a tractor class and suggest sample models based on acreage, terrain, tasks, and budget.

Run locally:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

Open http://localhost:5000 in your browser.
# Tractor