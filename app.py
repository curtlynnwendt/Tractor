from flask import Flask, render_template, request

app = Flask(__name__)

SAMPLE_MODELS = {
    'compact': [
        {
            'name': 'Compact 25HP',
            'brand': 'Brand A',
            'hp': 25,
            'pto': 18,
            'weight_lbs': 2200,
            'price_usd': 18000,
            'image': 'compact_25.svg',
            'description': 'Small, nimble tractor suitable for small acreage and light loader work.'
        },
        {
            'name': 'Compact 35HP',
            'brand': 'Brand B',
            'hp': 35,
            'pto': 30,
            'weight_lbs': 2800,
            'price_usd': 24000,
            'image': 'compact_35.svg',
            'description': 'Higher-power compact for heavier attachments and more demanding chores.'
        },
    ],
    'utility': [
        {
            'name': 'Utility 50HP',
            'brand': 'Brand A',
            'hp': 50,
            'pto': 45,
            'weight_lbs': 4200,
            'price_usd': 35000,
            'image': 'utility_50.svg',
            'description': 'Versatile mid-range tractor for haying, tillage, and loader work.'
        },
        {
            'name': 'Utility 75HP',
            'brand': 'Brand C',
            'hp': 75,
            'pto': 65,
            'weight_lbs': 6500,
            'price_usd': 62000,
            'image': 'utility_75.svg',
            'description': 'Stronger utility tractor for larger implements and heavier loads.'
        },
    ],
    'rowcrop': [
        {
            'name': 'Row-Crop 120HP',
            'brand': 'Brand D',
            'hp': 120,
            'pto': 100,
            'weight_lbs': 11000,
            'price_usd': 95000,
            'image': 'rowcrop_120.svg',
            'description': 'High-horsepower row-crop tractor for large-acreage farming.'
        },
        {
            'name': 'Row-Crop 150HP',
            'brand': 'Brand E',
            'hp': 150,
            'pto': 130,
            'weight_lbs': 13500,
            'price_usd': 130000,
            'image': 'rowcrop_150.svg',
            'description': 'Very powerful row-crop machine for heavy tillage and large implements.'
        },
    ]
}


def recommend_tractor(data):
    try:
        acres = float(data.get('acres', 0))
    except ValueError:
        acres = 0
    terrain = data.get('terrain', 'flat')
    budget = data.get('budget', 'medium')
    tasks = data.getlist('tasks') if hasattr(data, 'getlist') else data.get('tasks', [])
    # Determine class by acreage and tasks
    if acres <= 50:
        tractor_class = 'compact'
        hp_range = (20, 40)
    elif acres <= 500:
        tractor_class = 'utility'
        hp_range = (40, 100)
    else:
        tractor_class = 'rowcrop'
        hp_range = (100, 250)

    # Adjust for heavy tasks
    if 'harvesting' in tasks or 'plowing' in tasks:
        if tractor_class == 'compact':
            tractor_class = 'utility'
            hp_range = (45, 90)

    # Terrain adjustments
    drive = '2WD'
    if terrain in ('hilly', 'mixed'):
        drive = '4WD'
    if terrain == 'wet':
        drive = '4WD or tracks'

    # Budget influences brand/sample selection
    models = SAMPLE_MODELS.get(tractor_class, [])
    if budget == 'low':
        suggested = models[:1]
    elif budget == 'high':
        suggested = models[-1:]
    else:
        suggested = models

    return {
        'class': tractor_class,
        'hp_range': hp_range,
        'drive': drive,
        'suggested_models': suggested,
        'notes': f"Based on {acres} acres, tasks: {tasks or 'general'}, budget: {budget}."
    }


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.form
    rec = recommend_tractor(data)
    return render_template('result.html', rec=rec, form=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
