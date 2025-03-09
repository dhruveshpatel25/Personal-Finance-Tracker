import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_amount,get_category,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE='finance_data.csv'
    COLUMNS=['date','amount','category','description']
    DATE_FORMAT="%d-%m-%Y"

    #classmethod used so we can modify class-level variables
    @classmethod

    #initialize the csv file
    def initialize_csv(cls):
        try:

            #try to read the csv file
            pd.read_csv(cls.CSV_FILE)

        #if the file is not found 
        except FileNotFoundError:

            #create a new csv file with the specified columns
            df=pd.DataFrame(columns=cls.COLUMNS)

            #save the dataframe to the csv file
            df.to_csv(cls.CSV_FILE,index=False)

    @classmethod

    #add entry
    def add_entry(cls,date,amount,category,description):
        new_entry={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }

        #open the csv file in append mode
        with open(cls.CSV_FILE,"a",newline='') as csvfile:

            #write the new entry to the csv file
            #DictWriter is used to write the dictionary to the csv file
            write=csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)

            #writerow is used to write the row to the csv file
            write.writerow(new_entry)

            #after writing the entry, print the message
            print("Entry added successfully")

    @classmethod

    #get transactions
    def get_transactions(cls,start_date,end_date):

        #read the csv file
        df=pd.read_csv(cls.CSV_FILE)

        #convert the date column to datetime object and over write in date column
        df['date']=pd.to_datetime(df['date'],format=CSV.DATE_FORMAT)

        #convert the start date to date time object from string
        start_date=datetime.strptime(start_date,cls.DATE_FORMAT)

        #convert the end date to date time object from string
        end_date=datetime.strptime(end_date,cls.DATE_FORMAT)

        #check if the current date in csv file is between the start date and end date
        mask=(df['date']>=start_date)&(df['date']<=end_date)

        #locate all the rows which satisfied the previous condition
        filtered_df=df.loc[mask]

        #check if there exist ant data in range
        if filtered_df.empty:

            #if no transactions are found, print the message
            print("No transactions found")
        else:

            #transaction range dates
            print(f"Transactions between {start_date.strftime(CSV.DATE_FORMAT)} and {end_date.strftime(CSV.DATE_FORMAT)}")

            #print all transactions
            #convert to string,no index to be printed,format each date to the specified format
            print(filtered_df.to_string(index=False,formatters={"date":lambda x:x.strftime(CSV.DATE_FORMAT)}))

            #calculate the total income 
            total_income=filtered_df[filtered_df['category']=="Income"]['amount'].sum()

            #calculate the total expense
            total_expense=filtered_df[filtered_df['category']=='Expense']['amount'].sum()

            #print the summary
            print("\nSummary: ")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Savings: {total_income-total_expense:.2f}")

        #return the filtered date 
        return filtered_df

#add new transaction
def add():

    #initialize the csv file
    CSV.initialize_csv()

    #get the date, amount, category and description from the user
    date=get_date("Enter the date (DD-MM-YYYY) or ENTER for today's date: ",allow_default=True)
    amount=get_amount()
    category=get_category()
    description=get_description()

    #add the entry to the csv file
    CSV.add_entry(date,amount,category,description)

#plot the transactions
def plot_transactions(df):

    #set the date as index
    df.set_index('date',inplace=True)

    #resample the data by day
    #sum clculates the total amount for each day
    #reindex fills the missing dates with 0
    income_df=df[df['category']=='Income'].resample('D').sum().reindex(df.index,fill_value=0)
    expense_df=df[df['category']=='Expense'].resample('D').sum().reindex(df.index,fill_value=0)

    #width,height
    plt.figure(figsize=(10,5))

    #(x-axis,y-axis,label,color)
    plt.plot(income_df.index,income_df['amount'],label='Income',color='green')
    plt.plot(expense_df.index,expense_df['amount'],label='Expense',color='red')

    #x-axis label
    plt.xlabel('Date')

    #y-axis label
    plt.ylabel('Amount')

    #title of the plot
    plt.title('Income and Expense Over Time')

    #show legend in plot
    plt.legend()

    #show grid in plot
    plt.grid(True)

    #show the plot
    plt.show()

def main():
    while True:

        #print the menu
        print("\n1. Add new transaction")
        print("2. View transactions")
        print("3. Exit")
        choice=input("Enter your choice: ")

        #check the choice
        if choice=="1":

            #call the add function
            add()
        elif choice=="2":

            #get the start date and end date from the user
            start_date=get_date("Enter the start date (DD-MM-YYYY): ")
            end_date=get_date("Enter the end date (DD-MM-YYYY): ")

            #get the transactions between the start date and end date
            df=CSV.get_transactions(start_date,end_date)

            #if the user wants to plot the transactions
            if input("Do you want to plot the transactions? (y/n): ").lower()=="y":
                plot_transactions(df)

        #if the user wants to exit
        elif choice=="3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3")

if __name__=="__main__":
    main()