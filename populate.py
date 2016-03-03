#!/usr/bin/env python3
""":script:`getpost.database.populate` --- script for populating database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import csv

from sqlalchemy import MetaData

from getpost.models import Student
from getpost.orm import engine, Session


CSV_FILE = 'OCMRs.csv'


def populate_student(csv_dictreader, db_session):
    for row in csv_dictreader:
        student = Student(
            first_name=row['first_name'],
            last_name=row['last_name'],
            # alternative_name='',
            ocmr=row['ocmr'],
            t_number='T01000000',
            email_address=row['email_id']+'@oberlin.edu',
        )
        db_session.add(student)

if __name__ == '__main__':

    metadata = MetaData(bind=engine)

    with open(CSV_FILE) as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=',')

        db_session = Session()
        try:
            populate_student(cf, db_session)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
