import os
import pandas as pd

directory = "./data"


def HDBresaleindex(filepath="./raw_data/HDBResalePriceIndex1Q2009100Quarterly.csv"):
    """This function reads in the raw HDB resale price index csv file downloaded from
    "https://data.gov.sg/api/action/datastore_search?resource_id=d_14f63e595975691e7c24a27ae4c07c79",
    made some adjustments to the data, and stores the engineered data as csv in data folder.

    Args:
        filepath (str, optional): location where raw file is stored.
        Defaults to "./raw_data/HDBResalePriceIndex1Q2009100Quarterly.csv".
    """
    df = pd.read_csv(filepath)
    # subsets to data starting from 2004-Q1, to provide data points for the past 20 years
    df_new = df[df["quarter"] > "2004"].reset_index()
    df_new[["quarter", "index"]].to_csv(
        "./data/1_HDBResalePriceIndex2009_2024.csv", index=False
    )


def HDBresalemedian(
    filepath="./raw_data/MedianResalePricesforRegisteredApplicationsbyTownandFlatType.csv",
):
    """This function reads in the raw HDB median resale price csv file downloaded from
    "https://data.gov.sg/api/action/datastore_search?resource_id=d_b51323a474ba789fb4cc3db58a3116d4",
    made some adjustments to the data, and stores the engineered data as csv in data folder.

    Args:
        filepath (str, optional): _description_. Defaults to "./raw_data/MedianResalePricesforRegisteredApplicationsbyTownandFlatType.csv".
    """
    df = pd.read_csv(filepath)
    # subsets to data starting from 2020-Q1, to provide data points for the past 5 years
    df_new = df[df["quarter"] > "2020"].reset_index()
    # replaces 'na' and '-' values in the price field with None
    df_new["price"] = df_new["price"].replace({"na": None, "-": None})
    df_new[["quarter", "town", "flat_type", "price"]].to_csv(
        "./data/2_HDBMedianResalePrices2020_2024.csv", index=False
    )


def HDBresaledetails(
    filepath="./raw_data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv",
):
    """This function reads in the raw HDB resale price details csv file downloaded from
    "https://data.gov.sg/api/action/datastore_search?resource_id=d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
    made some adjustments to the data, and stores the engineered data as csv in data folder.

    Args:
        filepath (str, optional): _description_. Defaults to "./raw_data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv".
    """
    df = pd.read_csv(filepath)
    # subsets to data starting from Oct 2023 to provide data points for the past 12 months
    # Also removes redundant field - remaining_lease
    df_new = df[df["month"] > "2023-09"].drop("remaining_lease", axis=1).reset_index()
    df_new[
        [
            "month",
            "town",
            "flat_type",
            "flat_model",
            "floor_area_sqm",
            "resale_price",
            "street_name",
            "block",
            "storey_range",
            "lease_commence_date",
        ]
    ].to_csv("./data/3_HDBResalePricesDetailsOct23_Oct24.csv", index=False)


def CEAagenttxn(
    filepath=[
        "./raw_data/CEASalespersonInformation.csv",
        "./raw_data/CEASalespersonsPropertyTransactionRecordsresidential.csv",
    ]
):
    """This function reads in the raw CEA Agent Info csv file and the raw CEA Agent Transaction records
    downloaded from "https://data.gov.sg/api/action/datastore_search?resource_id=d_07c63be0f37e6e59c07a4ddc2fd87fcb" and
    "https://data.gov.sg/api/action/datastore_search?resource_id=d_ee7e46d3c57f7865790704632b0aef71" respectively. It
    made some adjustments to the data, combines them and stores the engineered data as csv in data folder.

    Args:
        filepath (list, optional): _description_. Defaults to [ "./raw_data/CEASalespersonInformation.csv", "./raw_data/CEASalespersonsPropertyTransactionRecordsresidential.csv", ].
    """
    agentinfo = pd.read_csv(filepath[0])
    CEAtxn = pd.read_csv(filepath[1])
    # converts transaction_date field to datetime format for ease of subsetting
    CEAtxn["transaction_date"] = pd.to_datetime(
        CEAtxn["transaction_date"], format="%b-%Y"
    )
    # Since the focus is on HDB flat resale activity, remove other transaction activities (condo, landed, HED rental etc )
    # subsets to data starting from Oct 2023 to provide data points for past 12 months, also remove records where there is no associated salesperson
    df = CEAtxn[
        (CEAtxn.property_type == "HDB")
        & (CEAtxn.transaction_type == "RESALE")
        & (CEAtxn.transaction_date > "2023-08-01")
        & (CEAtxn.salesperson_reg_num != "-")
    ]
    # Get relevant fields from CEA agent transaction records and left join with CEA agent info to get the corresponding real estate agency tagged to salesperson
    df_new = df[
        ["salesperson_name", "transaction_date", "salesperson_reg_num", "town"]
    ].merge(
        agentinfo[["registration_no", "estate_agent_name"]],
        how="left",
        left_on="salesperson_reg_num",
        right_on="registration_no",
    )
    # Remove redundant field
    df_new.drop("registration_no", axis=1, inplace=True)
    # Relabel the column names
    df_new.columns = [
        "sales_agent_name",
        "resale_transaction_date",
        "sales_agent_reg_num",
        "town",
        "real_estate_company_name",
    ]
    df_new.to_csv("./data/4_CEAAgentTransactionsSep23-Sep24.csv", index=False)


if __name__ == "__main__":
    if "1_HDBResalePriceIndex2009_2024.csv" not in os.listdir(directory):
        HDBresaleindex()
    if "2_HDBMedianResalePrices2020_2024.csv" not in os.listdir(directory):
        HDBresalemedian()
    if "3_HDBResalePricesDetailsOct23_Oct24.csv" not in os.listdir(directory):
        HDBresaledetails()
    if "4_CEAAgentTransactionsSep23-Sep24.csv" not in os.listdir(directory):
        CEAagenttxn()
