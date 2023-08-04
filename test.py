# import json
#
# with open('f1_2023.json', 'r') as f:
#     current_results = json.load(f)
#
# print(current_results)
# print('Bahrain' in current_results)
#
import ergast_py

e = ergast_py.Ergast()
race_results = e.season().get_races()
dict_of_round_name = {str(i.round_no): ' '.join(i.race_name.split(" ")[:-2]) for i in race_results}
res = e.season().round(13).get_results()
results = ""
# print(res)
for i in res:
    for y in i.results:
        results += (f"{y.position}, #{y.number}, {y.driver.given_name + ' ' + y.driver.family_name}, "
                    f"{y.constructor.name}, {y.laps}, {y.time.strftime('%I:%M:%S') if y.time else None}, {y.points}\n")

# print(str(results))
def get_gp_results(number_of_gp):
    e = ergast_py.Ergast()
    res = e.season().round(number_of_gp).get_results()
    if not res:
        date = e.season().round(number_of_gp).get_race().date
        return f"No results yet. This Grand Prix will start {date}"
    results = ""
    for i in res:
        for y in i.results:
            results += (f"{y.position}, #{y.number}, {y.driver.given_name + ' ' + y.driver.family_name}, "
                    f"{y.constructor.name}, {y.laps}, {y.time.strftime('%I:%M:%S') if y.time else None}, {y.points}\n")

    return results

# print(get_gp_results(13))
