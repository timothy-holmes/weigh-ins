from app import app, db
from app.models import User, WeighIn
import csv
from datetime import datetime

application = app

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'WeighIn': WeighIn}

def import_data():
    # read in CSV
    with open('data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            w = WeighIn(user_id=0,weight=row['Weight'],bf=row['BF'],time=datetime.strptime(row['Time'],'%H:%M'),date=datetime.strptime(row['Date'],'%d/%m/%Y'))
            db.session.add(w)
            
if __name__ == "__main__":
    app.run()