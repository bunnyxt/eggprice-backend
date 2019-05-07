import sys
import time
from db import conn


def get_timestamp_s():
    return int(time.time())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        location_name = sys.argv[1]
        print("Now store {0} forecast result to db".format(location_name))

        with open('result.txt', 'r') as f:
            lines = f.readlines()
            RMSE = float(lines[0])
            MAPE = float(lines[1])
            pre_date_str = lines[2][:-1] # delete \n
            pre_result = float(lines[3])
            results = []
            for i in range(4, len(lines)):
                result = lines[i].split()
                date = result[0]
                true_price = float(result[1])
                forecast_price = float(result[2])
                results.append([date, true_price, forecast_price])

        # store result
        with conn.cursor() as cursor:
            # get last_task_id
            sql = 'select * from forecast_task order by id desc limit 1;'
            cursor.execute(sql)
            result = cursor.fetchone()
            last_task_id = result[0]
            conn.commit()

            # insert into forecast_task table
            task_id = last_task_id + 1
            created_time = get_timestamp_s()
            print("Now start store with task_id {0}".format(task_id))
            sql = 'insert into forecast_task values ({0},"{1}",{2},{3},{4},"{5}",{6})'.format(
                task_id, location_name, created_time, RMSE, MAPE, pre_date_str, pre_result)
            cursor.execute(sql)
            conn.commit()

            # insert into forecast_record table
            for result in results:
                date = result[0]
                true_price = result[1]
                forecast_price = result[2]
                print('Insert record ("{0}",{1},{2},{3})'.format(
                    date, true_price, forecast_price, task_id))
                sql = 'insert into forecast_record values ("{0}",{1},{2},{3})'.format(
                    date, true_price, forecast_price, task_id)
                cursor.execute(sql)
                conn.commit()
        

        print("Finish store {0} forecast result to db.csv".format(location_name))
    else:
        print("No location name assigned.")