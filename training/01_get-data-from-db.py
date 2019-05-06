import sys
import pandas as pd
from db import conn

if __name__ == "__main__":
    if len(sys.argv) > 1:
        location_name = sys.argv[1]
        print("Now get {0} data from db".format(location_name))

        data = pd.DataFrame(columns=['date', 'price'])

        # fetch from db
        with conn.cursor() as cursor:
            sql = 'select * from egg_price where location_name="{0}";'.format(
                location_name)
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                newrow = pd.DataFrame(
                    {'date': row[1], 'price': row[3]}, index=[1])
                data = data.append(newrow, ignore_index=True)
            conn.commit()

        data.to_csv("data.csv", index=0)
        print("Save {0} data to data.csv".format(location_name))
    else:
        print("No location name assigned.")
