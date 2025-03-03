import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

projection = 12*3 #months

def makeLineplot(line1=None, line2=None, line3=None, line4=None, line5=None):
    global fig, axes  
    sns.set_theme(style="darkgrid")

    df = pd.DataFrame({
        "date": pd.date_range(start=datetime.date.today(), periods=len(line1), freq="M"),
        "NatWest - Digital Regular Saver": line1,
        "Chase - Boosted Saver": line2,
        "Barclays Flexible Cash ISA": line3,
        "S&P 500": line4
    }).melt(id_vars="date", var_name="category", value_name="Pounds")

    sns.lineplot(data=df, x="date", y="Pounds", hue="category", errorbar=('ci',95))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))  # %b -> "Jan", "Feb", etc.
    plt.xticks(rotation=0)

    plt.show()

def getNatWest(projectionLength):
    slumpDeposit = 0 #Initial investement
    aer = 6 #% Annual Equivalent Rate - Compounded Interest
    aerAfter5k = 1.49
    monthlyDeposit = 150
    balance = [0]
    interestEarned = [0]

    for m in range(projectionLength):
        prevBalance = balance[-1]
        monthlyAer = aer/12
        
        if(prevBalance > 5000):
            monthlyAer = aerAfter5k/12

        interest = prevBalance*monthlyAer/100
        newBalance = prevBalance + monthlyDeposit + interest
        balance.append(newBalance)
        interestEarned.append(interestEarned[-1] + interest)

    return {"balance": balance, "interest": interestEarned}

def getChase(projectionLength):
    slumpDeposit = 1000 #Initial investement
    boostedAer = 4.5 #% Annual Equivalent Rate - Compounded Interest
    aer = 3
    monthlyDeposit = 150

    balance = [slumpDeposit]
    interestEarned = [0]

    for m in range(projectionLength):
        prevBalance = balance[-1]
        monthlyAer = boostedAer/12
        if m>6:
            monthlyAer = 3/12

        interest = prevBalance*monthlyAer/100
        newBalance = prevBalance + monthlyDeposit + interest
        balance.append(newBalance)
        interestEarned.append(interestEarned[-1] + interest)

    return {"balance": balance, "interest": interestEarned}

def getBarclays(projectionLength):
    slumpDeposit = 1000 #Initial investement
    aer = 4.05 #% Annual Equivalent Rate - Compounded Interest
    monthlyDeposit = 150

    balance = [slumpDeposit]
    interestEarned = [0]

    for m in range(projectionLength):
        prevBalance = balance[-1]
        monthlyAer = aer/12

        if (m%12 == 0 and m !=0): #new month of the year
            prevBalance += monthlyDeposit * 12
        interest = prevBalance * monthlyAer/100
        newBalance = prevBalance
        balance.append(newBalance)
        interestEarned.append(interestEarned[-1] + interest)

    return {"balance": balance, "interest": interestEarned}

def getSP500(projectionLength):
    slumpDeposit = 1000 #Initial investement
    aer = 6.37 #% Annual Equivalent Rate - Compounded Interest
    monthlyDeposit = 150

    balance = [slumpDeposit]
    interestEarned = [0]

    for m in range(projectionLength):
        prevBalance = balance[-1]
        monthlyAer = aer/12

        interest = prevBalance*monthlyAer/100
        newBalance = prevBalance + monthlyDeposit + interest
        balance.append(newBalance)
        interestEarned.append(interestEarned[-1] + interest)

    return {"balance": balance, "interest": interestEarned}

NatWestBalance, NatWestInterest = getNatWest(projection).values()
ChaseBalance, ChaseInterest = getChase(projection).values()
BarclaysBalance, BarclaysInterest = getBarclays(projection).values()
SPBalance, SPInterest = getSP500(projection).values()

makeLineplot(NatWestInterest, ChaseInterest, BarclaysInterest, SPInterest)
# makeLineplot(NatWestBalance, ChaseBalance, BarclaysBalance, SPBalance)