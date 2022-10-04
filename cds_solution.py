from sqlite3 import connect
import pandas as pd

# Create a connection to the provided DB file
conn = connect(r'exercise01.sqlite')

# Store the desired query in a variable for later use
query = '''SELECT r.id, r.age, w.name workclass, e.name education_level, 
r.education_num, ms.name marital_status, o.name occupation, rel.name relationship, 
ra.name race, s.name sex, r.capital_gain, r.capital_loss, r.hours_week, 
c.name country, r.over_50k
FROM records r 
JOIN countries c ON r.country_id = c.id
JOIN education_levels e ON e.id = r.education_level_id
JOIN marital_statuses ms ON r.marital_status_id = ms.id
JOIN occupations o ON r.occupation_id = o.id
JOIN races ra ON r.race_id = ra.id
JOIN relationships rel ON r.relationship_id = rel.id
JOIN sexes s ON r.sex_id = s.id
JOIN workclasses w ON r.workclass_id = w.id;'''

# Execute the provided query against the connection and store the result in a dataframe
results = pd.read_sql(query, conn)

# Save the dataframe to a csv for later use
results.to_csv('consolidated_records.csv', mode = 'w', index = False)