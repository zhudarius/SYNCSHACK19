from serve import *
@app.route('/compatible_unit/<unit>', methods=['GET', 'POST'])
def compatible_unit(unit):
    data_in = request.get_json()
    categories = calculate_categories(data_in['units_taken'])
    if unit in categories['can_take']:
        return str(True), 200
    else:
        return str(False), 200