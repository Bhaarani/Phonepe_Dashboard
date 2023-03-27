import glob
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector


mydatabase=mysql.connector.connect(
host="localhost",
user="root",
port="3306",
password="",
)
mycursor= mydatabase.cursor(buffered=True)


mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_pulse")
mydatabase.commit()
mycursor.close()





engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="phonepe_pulse"))



path_state = (glob.glob(r"C:\Users\Dhivi\Desktop\phonepe_Dataset\pulse\data\*\*\country\india\state\*\*\*.json", recursive = True))

payments_type_statewise = pd.DataFrame()
users_by_device_statewise = pd.DataFrame()
reg_user_statewise = pd.DataFrame()

trans_in_district_statewise = pd.DataFrame()
user_in_district_statewise = pd.DataFrame()

trans_in_city_statewise = pd.DataFrame()
trans_in_pin_statewise = pd.DataFrame()

user_in_city_statewise = pd.DataFrame()
user_in_pin_statewise = pd.DataFrame()


splt_lst = []
for i in path_state:
    splt_lst = i.split('\\')
    if splt_lst[7] =="aggregated":

        if splt_lst[8] == "transaction":

            DF = pd.read_json(i)
            j = DF.loc["transactionData", "data"]
            j = pd.json_normalize(j, record_path=['paymentInstruments'], meta=["name"])

            j["Year"] = splt_lst[13]

            j["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            j["Quater"] = x[0]

            payments_type_statewise = pd.concat([payments_type_statewise, j])





        if splt_lst[8] == "user":

            DF = pd.read_json(i)

            a = DF.loc["usersByDevice", "data"]
            if a == None:
                continue
            a = pd.json_normalize(a)

            b = DF.loc["aggregated", "data"]
            if b == None:
                continue
            b = pd.json_normalize(b)

            a["Year"] = b["Year"] = splt_lst[13]

            a["State"] = b["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            a["Quater"] = b["Quater"] = x[0]


            users_by_device_statewise = pd.concat([users_by_device_statewise, a])



            reg_user_statewise = pd.concat([reg_user_statewise, b])




    if splt_lst[7] =="map":

        if splt_lst[8] == "transaction":

            DF = pd.read_json(i)

            a = DF.loc["hoverDataList", "data"]
            a = pd.json_normalize(a, record_path=["metric"], meta=["name"])
            a.columns = ["Type", "Count", "Amount", "District"]

            a["Year"] = splt_lst[13]

            a["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            a["Quater"] = x[0]

            trans_in_district_statewise = pd.concat([trans_in_district_statewise, a])



        if splt_lst[8] == "user":
            DF = pd.read_json(i)

            a = DF.loc["hoverData", "data"]
            a = pd.DataFrame(a)
            a = a.transpose()
            a.reset_index(inplace=True)
            a.columns = ["City", "RegUser", "AppOpens"]

            a["Year"] = splt_lst[13]

            a["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            a["Quater"] = x[0]

            user_in_district_statewise = pd.concat([user_in_district_statewise, a])



    if splt_lst[7] =="top":

        if splt_lst[8] == "transaction":
            DF = pd.read_json(i)

            a = DF.loc["districts", "data"]
            a = pd.json_normalize(a)
            a.columns = ["City", "Total", "Count", "Amount"]

            b = DF.loc["pincodes", "data"]
            b = pd.json_normalize(b)
            b.columns = ["Pincode", "Total", "Count", "Amount"]

            a["Year"] = b["Year"] = splt_lst[13]

            a["State"] = b["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            a["Quater"] = b["Quater"] = x[0]

            trans_in_city_statewise = pd.concat([trans_in_city_statewise, a])



            trans_in_pin_statewise = pd.concat([trans_in_pin_statewise, b])



        if splt_lst[8] == "user":
            DF = pd.read_json(i)

            a = DF.loc["districts", "data"]
            a = pd.DataFrame(a)
            a.columns = ["District", "DistrictRegUser"]

            b = DF.loc["pincodes", "data"]
            b = pd.DataFrame(b)
            b.columns = ["Pincodes", "PincodeRegUser"]

            a["Year"] = b["Year"] = splt_lst[13]

            a["State"] = b["State"] = splt_lst[12]

            x = splt_lst[14].split(".")
            a["Quater"] = b["Quater"] = x[0]

            user_in_city_statewise = pd.concat([user_in_city_statewise, a])

            user_in_pin_statewise = pd.concat([user_in_pin_statewise, b])


payments_type_statewise.to_sql("payments_type_statewise", con=engine, if_exists='replace')
users_by_device_statewise.to_sql("users_by_device_statewise", con=engine, if_exists='replace')
reg_user_statewise.to_sql("reg_user_statewise", con=engine, if_exists='replace')
trans_in_district_statewise.to_sql("trans_in_district_statewise", con=engine, if_exists='replace')
user_in_district_statewise.to_sql("user_in_district_statewise", con=engine, if_exists='replace')
trans_in_city_statewise.to_sql("trans_in_city_statewise", con=engine, if_exists='replace')
trans_in_pin_statewise.to_sql("trans_in_pin_statewise", con=engine, if_exists='replace')
user_in_city_statewise.to_sql("user_in_city_statewise", con=engine, if_exists='replace')
user_in_pin_statewise.to_sql("user_in_pin_statewise", con=engine, if_exists='replace')
