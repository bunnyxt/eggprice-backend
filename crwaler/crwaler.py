#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pymysql
import schedule
import time
import threading
from db import conn


def get_timestamp_s():
    return int(time.time())


def get_time_str(ts_s):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_s))


def crwal_main():
    start_ts = get_timestamp_s()
    try:
        with conn.cursor() as cursor:
            # get last task id
            try:
                sql = 'select * from crwal_task order by id desc limit 1;'
                cursor.execute(sql)
                result = cursor.fetchone()
                last_task_id = result[0]
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            task_id = last_task_id + 1

            # get last url id
            try:
                sql = 'select * from egg_price order by url_id desc limit 1;'
                cursor.execute(sql)
                result = cursor.fetchone()
                last_url_id = result[0]
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e

            # insert task into db
            sql = 'insert into crwal_task values ({0},{1},{2},{3},"crwaling","")'.format(
                task_id, start_ts, 0, last_url_id, task_id)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            print("Crwal task " + str(task_id) +
                  " start at " + get_time_str(start_ts))
            print("Last url id is " + str(last_url_id))

            # try crwal
            url_id = last_url_id + 1
            err_count = 0
            while True:
                # exit
                if err_count > 10:
                    print(
                        "More than 10 errors occurr continuously, end crwal task " + str(task_id))
                    break

                # make soup and find string
                html = urlopen("http://www.cnjidan.com/jiage/" +
                               str(url_id)).read().decode("GBK")
                soup = BeautifulSoup(html, features="lxml")
                string = soup.find('div', {"class": "sner"})

                if string:
                    string = string.get_text()
                else:
                    print("Fail to obtain data from url_id " +
                          str(url_id) + ", ec: " + str(err_count))
                    err_count += 1
                    time.sleep(1)
                    continue

                # pick date location price from string
                date = re.findall(r"据鸡蛋价格网统计，(\d{4})年(\d{2})月(\d{2})日", string)
                location = re.findall(
                    r"据鸡蛋价格网统计，\d{4}年\d{2}月\d{2}日(.+)鸡蛋价格", string)
                price = re.findall(
                    r"据鸡蛋价格网统计，\d{4}年\d{2}月\d{2}日.+鸡蛋价格为:(\d+.?\d+)元/公斤", string)

                # try pick
                try:
                    date_str = '{0}-{1}-{2}'.format(
                        date[0][0], date[0][1], date[0][2])
                    location_str = location[0]
                    price_str = price[0]
                except Exception as e:
                    print(e)
                    print("Fail to obtain data from url_id " +
                          str(url_id) + ", ec: " + str(err_count))
                    err_count += 1
                    time.sleep(1)
                    continue

                # insert price into db
                try:
                    sql = 'insert into egg_price values ({0},"{1}","{2}",{3},{4})'.format(
                        url_id, date_str, location_str, price_str, task_id)
                    cursor.execute(sql)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    raise e
                print("Successfully added data " + date_str + " " + location_str + " " + price_str +
                      " from url_id " + str(url_id))

                url_id += 1
                err_count = 0
                time.sleep(0.1)

            # crwal end
            end_ts = get_timestamp_s()
            try:
                sql = 'update crwal_task set end_time = {0}, status = "finished" where id = {1}'.format(
                    end_ts, task_id)
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            print("Crwal task " + str(task_id) +
                  " end at " + get_time_str(end_ts))

    except Exception as e:
        print(e)
        end_ts = get_timestamp_s()
        print("Crwal task " + str(task_id) + " end at " + get_time_str(end_ts))


def crwal_task():
    threading.Thread(target=crwal_main).start()


if __name__ == "__main__":
    # for debug
    crwal_task()

    # schedule.every(10).minutes.do(crwal_task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)
