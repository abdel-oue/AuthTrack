from extraction import extract_data
from api_service import get_country
import database_0 as db
import dashboards as plot

def insert_country_to_data(con, data : list):
    for i,line in enumerate(data):
        ip = line[2]
        country = get_country(ip)
        print("Data #",i," : Country : ",country)
        db.insert_country_to_line(con,country,ip)

if __name__ == '__main__':

    data = extract_data('./data/small-auth.log')

    con = db.get_connection()
    #db.creating_table(con)
    #db.insert_to_table(con,data)


    # ----- Getting data from database -----

    #insert_country_to_data(con,data)
    countrylist = db.get_country_failed_attempts(con)
    userlist = db.get_accepted_user_data(con)
    logsdata = db.get_logging_data(con)
    # ----- Drawing plots and writing logs from data achieved from database -----
    plot.draw_countries(countrylist)
    plot.draw_users(userlist)
