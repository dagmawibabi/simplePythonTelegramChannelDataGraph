import json
import datetime 
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import tkinter as tk

# Set font to one that supports emojis 
rcParams['font.family'] = 'Segoe UI Emoji'  

# Globals 
data = {}
channelName = ''
messages = []
messagesCount = 0;
messageTypes = ['service', 'message']

userMessages = []
serviceMessages  = []
userMessagesCount = 0
serviceMessagesCount = 0
reactionsCount = {}
paidReactionsCount = 0
emojiReactionsCount = 0
totalReactionsCount = 0

msgCountByYear = {}
msgCountByMonth = {}
msgCountByDay = {}
channelBirthdate = ''
channelLastPost = ''

# Read Export 
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    messages = data['messages']

# Analysis
def analysis():
    global reactionsCount, paidReactionsCount, messagesCount, userMessagesCount, serviceMessagesCount, msgCountByDay, emojiReactionsCount, channelBirthdate, channelLastPost,totalReactionsCount, channelName
    # Service and User Messages 
    for message in messages:
        if(message['type'] == 'service'):
            serviceMessages.append(message)
        else:
            userMessages.append(message)
    # Message Count By Year
    for message in userMessages:
        dt = datetime.datetime.fromtimestamp(int(message['date_unixtime']))
        if(dt.year not in msgCountByYear):
            msgCountByYear[dt.year] = 0
        msgCountByYear[dt.year] += 1 
        if(dt.month not in msgCountByMonth):
            msgCountByMonth[dt.month] = 0
        msgCountByMonth[dt.month] += 1 
        if(dt.day not in msgCountByDay):
            msgCountByDay[dt.day] = 0
        msgCountByDay[dt.day] += 1 
    
    # Reaction Count 
    for message in messages:
        if('reactions' in message):
            for reaction in message['reactions']:
                if reaction['type'] == 'emoji':
                    if(reaction['emoji'] not in reactionsCount):
                        reactionsCount[reaction['emoji']] = 0
                    reactionsCount[reaction['emoji']] += reaction['count']
                if reaction['type'] == 'paid':
                    paidReactionsCount += reaction['count']
    reactionsCount = dict(sorted(reactionsCount.items(), key=lambda item: item[1]))
    reactionsCount['paid'] = paidReactionsCount
    # Count Service and User Messages 
    channelName = data['name']
    messagesCount = len(messages)
    userMessagesCount = len(userMessages)
    serviceMessagesCount = len(serviceMessages)
    emojiReactionsCount = sum(reactionsCount.values())
    channelBirthdateTimestamp = datetime.datetime.fromtimestamp(int(messages[0]['date_unixtime']))
    channelBirthdate = channelBirthdateTimestamp.strftime("%Y-%m-%d")
    channelLastPostTimestamp = datetime.datetime.fromtimestamp(int(messages[-1]['date_unixtime']))
    channelLastPost = channelLastPostTimestamp.strftime("%Y-%m-%d")
    totalReactionsCount = emojiReactionsCount + paidReactionsCount
    # PRINT 
    print("--------------------------------------------------------------")
    print("channelName: ", channelName)
    print("--------------------------------------------------------------")
    print("yearsActive: ", len(msgCountByYear) - 1)
    print("channelBirthdate: ", channelBirthdate)
    print("channelLastPost: ", channelLastPost)
    print("--------------------------------------------------------------")
    print("messagesCount: ", messagesCount)
    print("userMessagesCount: ", userMessagesCount)
    print("serviceMessagesCount: ", serviceMessagesCount)
    print("--------------------------------------------------------------")
    print("paidReactionsCount: ", paidReactionsCount)
    print("emojiReactionsCount: ", emojiReactionsCount)
    print("totalReactionsCount: ", totalReactionsCount)
    print("--------------------------------------------------------------")
    
analysis()

# Reactions Count 
def reactionsCountBarGraph(): 
    # PLOT
    keys = list(reactionsCount.keys())[-20:]
    values = list(reactionsCount.values())[-20:]
    # Create bar chart
    colors = ['#1f77b4' if k != 'paid' else 'orange' for k in keys]
    plt.bar(keys, values, color=colors, width=0.5)
    # Add labels and title
    plt.xlabel('Reactions')
    plt.ylabel('Count')
    plt.title('Reactions Count')
    # Display the plot
    plt.show()
# reactionsCountBarGraph()

# Reactions Count 
def reactionsCountHeatMap():
    # PLOT
    keys = list(reactionsCount.keys())[-30:]
    values = list(reactionsCount.values())[-30:]
    # Convert to 4x5 grid (you can reshape based on your data size)
    grid_values = np.array(values).reshape(5, 6)
    grid_labels = np.array(keys).reshape(5, 6)
    plt.figure(figsize=(10, 6))
    plt.imshow(grid_values, cmap='YlOrRd') # YlOrRd viridis coolwarm
    # Annotate with emojis
    for i in range(5):
        for j in range(6):
            emoji = grid_labels[i, j]
            count = grid_values[i, j]
            plt.text(j, i, f'{emoji}\n{count}', ha='center', va='center', fontsize=12)
    plt.colorbar(label='Reaction Count')
    plt.title("Reaction Heatmap")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
# reactionsCountHeatMap()

# Service vs User Messages 
def serviceVsUserMessagesBarGraph():
    keys = ['Service Messages', 'User Messages']
    values = [serviceMessagesCount, userMessagesCount]
    plt.figure(figsize=(6, 4))
    plt.bar(keys, values)
    plt.yscale('log')  # Apply logarithmic scale
    plt.title("Reaction Counts (Log Scale)")
    plt.ylabel("Count (log scale)")
    plt.tight_layout()
    plt.show()
# serviceVsUserMessagesBarGraph()

# Messages Per Year Bar Graph
def messagesPerYearBarGraph():
    keys = list(msgCountByYear.keys())
    values = list(msgCountByYear.values())
    plt.bar(keys, values)
    plt.xlabel('Year')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Year')
    plt.show()
# messagesPerYearBarGraph() 

# Messages Per Year Bar Graph Sorted
def messagesPerYearBarGraphSorted():
    sorted_items = sorted(msgCountByYear.items(), key=lambda item: item[1], reverse=True)
    keys = [str(k) for k, _ in sorted_items]  # Convert to string to prevent x-axis auto-scaling
    values = [v for _, v in sorted_items]
    plt.bar(keys, values)
    plt.xlabel('Year')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Year')
    plt.show()
# messagesPerYearBarGraphSorted() 

# Messages Per Year Heat Map
def messagesPerYearHeatMap():
    # Ensure all years from 2018 to 2025 are present
    years = list(range(2018, 2026))
    values = [msgCountByYear.get(year, 0) for year in years]

    # Reshape into 2 rows x 4 columns
    grid_values = np.array(values).reshape(2, 4)
    grid_labels = np.array(years).reshape(2, 4)

    plt.figure(figsize=(8, 4))
    plt.imshow(grid_values, cmap='viridis')
    plt.title('Message Count Heatmap by Year')

    # Annotate cells with year
    for i in range(2):
        for j in range(4):
            plt.text(j, i, str(grid_labels[i, j]), ha='center', va='center', fontsize=12)

    plt.colorbar(label='Message Count')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
# messagesPerYearHeatMap() 

# Messages Per Month Bar Graph
def messagesPerMonthBarGraph():
    sorted_items = sorted(msgCountByMonth.items())
    # sorted_items = sorted(msgCountByMonth.items(), key=lambda item: item[1], reverse=True)
    keys = [str(k) for k, _ in sorted_items]  # Convert to string to prevent x-axis auto-scaling
    values = [v for _, v in sorted_items]
    plt.bar(keys, values)
    plt.xticks(ticks=keys)
    plt.xlabel('Month')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Month')
    plt.show()
# messagesPerMonthBarGraph() 

# Messages Per Month Bar Graph Sorted
def messagesPerMonthBarGraphSorted():
    sorted_items = sorted(msgCountByMonth.items(), key=lambda item: item[1], reverse=True)
    keys = [str(k) for k, _ in sorted_items]  # Convert to string to prevent x-axis auto-scaling
    values = [v for _, v in sorted_items]
    plt.bar(keys, values)
    plt.xticks(ticks=keys)
    plt.xlabel('Month')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Month')
    plt.show()
# messagesPerMonthBarGraphSorted() 

# Messages Per Month Heat Map
def messagesPerMonthHeatMap():
    # Make sure all months 1–12 are accounted for
    months = list(range(1, 13))
    values = [msgCountByMonth.get(month, 0) for month in months]

    # Reshape to 3 rows x 4 columns
    grid_values = np.array(values).reshape(3, 4)
    grid_labels = np.array(months).reshape(3, 4)

    plt.figure(figsize=(8, 5))
    plt.imshow(grid_values, cmap='Oranges')

    # Add annotations
    for i in range(3):
        for j in range(4):
            month_num = grid_labels[i, j]
            plt.text(j, i, f'{month_num}', ha='center', va='center', fontsize=12, color='black')

    plt.title('Message Count Heatmap by Month')
    plt.colorbar(label='Message Count')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
# messagesPerMonthHeatMap() 

# Messages Per Day Bar Graph
def messagesPerDayBarGraph():
    sorted_items = sorted(msgCountByDay.items())
    keys = [str(k) for k, _ in sorted_items]  # Convert to string to prevent x-axis auto-scaling
    values = [v for _, v in sorted_items]
    plt.bar(keys, values)
    plt.xticks(ticks=keys)
    plt.xlabel('Day')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Day')
    plt.show()
# messagesPerDayBarGraph() 

# Messages Per Day Bar Graph Sorted
def messagesPerDayBarGraphSorted():
    sorted_items = sorted(msgCountByDay.items(), key=lambda item: item[1], reverse=True)
    keys = [str(k) for k, _ in sorted_items]  # Convert to string to prevent x-axis auto-scaling
    values = [v for _, v in sorted_items]
    plt.bar(keys, values)
    plt.xticks(ticks=keys)
    plt.xlabel('Day')
    plt.ylabel('Message Count')
    plt.title('Message Count Per Day')
    plt.show()
# messagesPerDayBarGraphSorted() 

# Messages Per Day Heat Map
def messagesPerDayHeatMap():
    # Sort by day number (1 to 31, not value)
    sorted_items = sorted(msgCountByDay.items())
    days = [k for k, _ in sorted_items]
    counts = [v for _, v in sorted_items]

    # Pad to 35 values (5 rows x 7 columns)
    while len(counts) < 35:
        counts.append(0)
        days.append('')  # Empty label for extra cells

    # Convert to 2D arrays
    grid_values = np.array(counts).reshape(5, 7)
    grid_labels = np.array(days).reshape(5, 7)

    plt.figure(figsize=(10, 6))
    plt.imshow(grid_values, cmap='YlOrRd')
    plt.title('Message Count Heatmap by Day of Month')
    
    # Annotate each cell with the day number
    for i in range(5):
        for j in range(7):
            label = str(grid_labels[i, j]) if grid_labels[i, j] != '' else ''
            plt.text(j, i, label, ha='center', va='center', color='black', fontsize=12)

    plt.colorbar(label='Message Count')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
# messagesPerDayHeatMap() 


def window():
    # Create main window
    root = tk.Tk()
    root.title("Telegram Channel Stats")
    root.geometry("720x600")

    # Outer container for padding
    container = tk.Frame(root, padx=20, pady=20)
    container.pack(fill='both', expand=True)

    # Header label
    label1 = tk.Label(container, text=f"{channelName} Stats", font=('Helvetica', 16, 'bold'))
    label1.grid(row=0, column=0, columnspan=3, pady=10)

    # === First row: Three grouped boxes ===
    # Box 1: Year Active & Birthdate
    box1 = tk.Frame(container, bd=2, relief='groove', padx=10, pady=10)
    box1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    tk.Label(box1, text=f"Years Active: {len(msgCountByYear) - 1}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box1, text=f"Channel Birthdate: {channelBirthdate}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box1, text=f"Last Post: {channelLastPost}", font=('Helvetica', 10)).pack(anchor='w')

    # Box 2: Messages, User, and Service Messages Count
    box2 = tk.Frame(container, bd=2, relief='groove', padx=10, pady=10)
    box2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
    tk.Label(box2, text=f"Messages Count: {messagesCount}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box2, text=f"User Messages Count: {userMessagesCount}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box2, text=f"Service Messages Count: {serviceMessagesCount}", font=('Helvetica', 10)).pack(anchor='w')

    # Box 3: Emoji and Paid Reactions Count
    box3 = tk.Frame(container, bd=2, relief='groove', padx=10, pady=10)
    box3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
    tk.Label(box3, text=f"Emoji Reactions: {emojiReactionsCount}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box3, text=f"Paid Reactions: {paidReactionsCount}", font=('Helvetica', 10)).pack(anchor='w')
    tk.Label(box3, text=f"Total Reactions: {totalReactionsCount}", font=('Helvetica', 10)).pack(anchor='w')

    # Sub-header
    label2 = tk.Label(container, text="Choose a Graph to Display", font=('Helvetica', 16, 'bold'))
    label2.grid(row=2, column=0, columnspan=3, pady=10)

    # Buttons for graphs
    buttons = [
        ("Messages Per Day Bar Graph", messagesPerDayBarGraph),
        ("Messages Per Day Bar Graph (Sorted)", messagesPerDayBarGraphSorted),
        ("Messages Per Day Heat Map", messagesPerDayHeatMap),


        ("Messages Per Month Bar Graph", messagesPerMonthBarGraph),
        ("Messages Per Month Bar Graph (Sorted)", messagesPerMonthBarGraphSorted),
        ("Messages Per Month Heat Map", messagesPerMonthHeatMap),

        ("Messages Per Year Bar Graph", messagesPerYearBarGraph),
        ("Messages Per Year Bar Graph (Sorted)", messagesPerYearBarGraphSorted),
        ("Messages Per Year Heat Map", messagesPerYearHeatMap),

        ("Reactions Count Bar Graph", reactionsCountBarGraph),
        ("Reactions Count Heat Map", reactionsCountHeatMap),
        ("Service vs User Messages", serviceVsUserMessagesBarGraph),
    ]

    for i, (text, func) in enumerate(buttons):
        row = i // 3 + 3  # Start from row 3
        col = i % 3
        tk.Button(container, text=text, command=func, width=30).grid(row=row, column=col, padx=5, pady=5)

    root.mainloop()

window()