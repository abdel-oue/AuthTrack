from extraction import extract_data
from api_service import get_country
import database_0 as db


if __name__ == '__main__':

    data = extract_data('./data/small-auth.log')

    con = db.get_connection()
    db.creating_table(con)
    db.insert_to_table(con,data)

    