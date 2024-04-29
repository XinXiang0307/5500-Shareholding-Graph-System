import csv
import pandas as pd
from faker import Faker
from random import randint

PERSON_COUNT = 8
CORP_COUNT = 6
PERSON_SHAREHOLD_COUNT = 15
CORP_REL_COUNT = 10
CORP_SHAREHOLD_COUNT = 10
PERSON_REL_COUNT = 4
#PERSON_ROLE_COUNT = 50

WRITE_BATCH = 10

faker = Faker()
Faker.seed(1234)  # Correct way to seed

def csv_writer(file_path, row_count, row_generator):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        csv_buffer = []
        for row in range(row_count):
            csv_buffer.append(row_generator())
            if len(csv_buffer) >= WRITE_BATCH:
                writer.writerows(csv_buffer)
                csv_buffer = []
        if csv_buffer:
            writer.writerows(csv_buffer)

# Generate Persons and Corporations using Faker
def generate_person_data():
    data = {'person_id': ['p_' + str(i) for i in range(PERSON_COUNT)], 'person_name': [faker.name() for _ in range(PERSON_COUNT)]}
    return pd.DataFrame(data)

def generate_corp_data():
    data = {'corp_id': ['c_' + str(i) for i in range(CORP_COUNT)], 'corp_name': [faker.company() for _ in range(CORP_COUNT)]}
    return pd.DataFrame(data)


# Save persons and corporations to CSV
generate_person_data().to_csv('data/person.csv', index=False)
generate_corp_data().to_csv('data/corp.csv', index=False)

# Relationship generators
def person_share_generator():
    return ('p_' + str(randint(0, PERSON_COUNT - 1)), 'c_' + str(randint(0, CORP_COUNT - 1)), randint(0, 100))

def person_rel_generator():
    return ('p_' + str(randint(0, PERSON_COUNT - 1)), 'p_' + str(randint(0, PERSON_COUNT - 1)), randint(1, 3))

def corp_rel_generator():
    return ('c_' + str(randint(0, CORP_COUNT - 1)), 'c_' + str(randint(0, CORP_COUNT - 1)))

def corp_share_generator():
    return ('c_' + str(randint(0, CORP_COUNT - 1)), 'c_' + str(randint(0, CORP_COUNT - 1)), randint(0, 100))
'''
def person_corp_role_generator():
    job_title = faker.job().replace(',', '')
    return ('p_' + str(randint(0, PERSON_COUNT - 1)), 'c_' + str(randint(0, CORP_COUNT - 1)), job_title)
'''
# Writing the relationships to CSV
csv_writer('data/person_corp_share.csv', PERSON_SHAREHOLD_COUNT, person_share_generator)
csv_writer('data/person_rel.csv', PERSON_REL_COUNT, person_rel_generator)
csv_writer('data/corp_rel.csv', CORP_REL_COUNT, corp_rel_generator)
csv_writer('data/corp_share.csv', CORP_SHAREHOLD_COUNT, corp_share_generator)
#csv_writer('data/person_corp_role.csv', PERSON_ROLE_COUNT, person_corp_role_generator)
