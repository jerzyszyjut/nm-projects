import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

makarony = True
reverse_macd = False
path = 'mak_d.csv' if makarony else 'nvda.csv'
filename_template = f"./images/placeholder_{'makarony' if makarony else 'nvda'}_{'reverse' if reverse_macd else 'normal'}.png".replace('placeholder', '{}')

data = pd.read_csv(path)
data['Data'] = pd.to_datetime(data['Data'])

data = data.tail(1000)

short_window = 12
long_window = 26
signal_window = 9
closing_prices = data['Zamkniecie'].values

alpha = 2 / (short_window + 1)
short_ema = [closing_prices[0]]
for i in range(1, len(closing_prices)):
    ema = closing_prices[i] * alpha + short_ema[-1] * (1 - alpha)
    short_ema.append(ema)

alpha = 2 / (long_window + 1)
long_ema = [closing_prices[0]]
for i in range(1, len(closing_prices)):
    ema = closing_prices[i] * alpha + long_ema[-1] * (1 - alpha)
    long_ema.append(ema)

macd_line = [short - long for short, long in zip(short_ema, long_ema)]

alpha_signal = 2 / (signal_window + 1)
signal_line = [macd_line[0]]
for i in range(1, len(macd_line)):
    signal = macd_line[i] * alpha_signal + signal_line[-1] * (1 - alpha_signal)
    signal_line.append(signal)

data = data.tail(len(signal_line))
macd_line = macd_line[-len(signal_line):]
buy_signals = []
sell_signals = []

for i in range(len(signal_line)):
    if i == 0:
        buy_signals.append(False)
        sell_signals.append(False)
        continue
    if signal_line[i] > macd_line[i] and not signal_line[i-1] > macd_line[i-1]:
        macd_line_lower = True
        buy_signals.append(reverse_macd)
        sell_signals.append(not reverse_macd)
    elif signal_line[i] < macd_line[i] and not signal_line[i-1] < macd_line[i-1]:
        macd_line_lower = False
        buy_signals.append(not reverse_macd)
        sell_signals.append(reverse_macd)
    else:
        buy_signals.append(False)
        sell_signals.append(False)

volume_history = []
net_worth_history = []

current_volume = 1000
current_wallet = 0

starting_worth = current_volume * closing_prices[0]

for i in range(len(buy_signals)):
    id = data.index[i]
    if buy_signals[i] and current_wallet > 0:
        current_volume = current_wallet / closing_prices[i]
        current_wallet = 0
        data.loc[id, 'Buy'] = closing_prices[i]
    elif sell_signals[i] and current_volume > 0:
        current_wallet = current_volume * closing_prices[i]
        current_volume = 0
        data.loc[id, 'Sell'] = closing_prices[i]
    data.loc[id, 'Volume'] = current_volume
    data.loc[id, 'Wallet'] = current_wallet + current_volume * closing_prices[i]
    net_worth_history.append(current_wallet + current_volume * closing_prices[i])
    volume_history.append(current_volume)

data.to_csv('macd.csv')

ending_worth = current_wallet + current_volume * closing_prices[-1]
print(f'Starting worth: {starting_worth}')
print(f'Ending worth: {ending_worth}')
print(f'Net worth change: {ending_worth - starting_worth}')

plt.plot(data['Data'], data['Zamkniecie'], label='Closing Prices', color='blue')
plt.ylabel('Closing Prices')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('Closing Prices')
plt.xticks(rotation=45)
first = data.index[0]
last = data.index[-1]
starting_value = data.loc[first, 'Zamkniecie']
ending_value = data.loc[last, 'Zamkniecie']
maximum = max(data['Zamkniecie'])
starting_date = data.loc[first, 'Data']
ending_date = data.loc[last, 'Data']
plt.yticks(list(plt.yticks()[0]) + [starting_value, ending_value, maximum])

for i in range(len(buy_signals)):
    id = data.index[i]
    if buy_signals[i]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='^', color='green')
    elif sell_signals[i]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='v', color='red')

plt.savefig(filename_template.format("closing_prices"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'], macd_line, label='MACD', color='blue')
plt.plot(data['Data'], signal_line, label='Signal Line', color='red')
for i in range(len(buy_signals)):
    id = data.index[i]
    if buy_signals[i]:
        plt.plot(data.loc[id, 'Data'], macd_line[i], marker='^', color='green')
    elif sell_signals[i]:
        plt.plot(data.loc[id, 'Data'], macd_line[i], marker='v', color='red')
plt.ylabel('MACD')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('MACD')
plt.xticks(rotation=45)
plt.savefig(filename_template.format("macd"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'], data['Volume'], label='Volume', color='blue')
plt.ylabel('Volume')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('Volume')
plt.xticks(rotation=45)
plt.savefig(filename_template.format("volume"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'], data['Wallet'], label='Wallet', color='green')
plt.ylabel('Wallet')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('Wallet')
plt.xticks(rotation=45)
plt.savefig(filename_template.format("wallet"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'][300:500], data['Zamkniecie'][300:500], label='Closing Prices', color='blue')
plt.ylabel('Closing Prices')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('Closing Prices')
starting_date = data.loc[data.index[300], 'Data']
ending_date = data.loc[data.index[500], 'Data']
print(starting_date, ending_date)
plt.xticks(rotation=45)
for i in range(len(buy_signals[300:500])):
    index_shifted = i+300
    id = data.index[index_shifted]
    if buy_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='^', color='green')
    elif sell_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='v', color='red')
plt.savefig(filename_template.format("closing_prices_zoom"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'][300:500], macd_line[300:500], label='MACD', color='blue')
plt.plot(data['Data'][300:500], signal_line[300:500], label='Signal Line', color='red')

for i in range(len(buy_signals[300:500])):
    index_shifted = i+300
    id = data.index[index_shifted]
    if buy_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], macd_line[index_shifted], marker='^', color='green')
    elif sell_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], macd_line[index_shifted], marker='v', color='red')
plt.ylabel('MACD')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('MACD')
plt.xticks(rotation=45)
plt.savefig(filename_template.format("macd_zoom"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'][800:], data['Zamkniecie'][800:], label='Closing Prices', color='blue')
plt.ylabel('Closing Prices')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('Closing Prices')
plt.xticks(rotation=45)
starting_date = data.loc[data.index[800], 'Data']
ending_date = data.loc[data.index[-1], 'Data']
print(starting_date, ending_date)
for i in range(len(buy_signals[800:])):
    index_shifted = i+800
    id = data.index[index_shifted]
    if buy_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='^', color='green')
    elif sell_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], data.loc[id, 'Zamkniecie'], marker='v', color='red')
plt.savefig(filename_template.format("closing_prices_zoom_2"), bbox_inches='tight')
plt.close()

plt.plot(data['Data'][800:], macd_line[800:], label='MACD', color='blue')
plt.plot(data['Data'][800:], signal_line[800:], label='Signal Line', color='red')

for i in range(len(buy_signals[800:])):
    index_shifted = i+800
    id = data.index[index_shifted]
    if buy_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], macd_line[index_shifted], marker='^', color='green')
    elif sell_signals[index_shifted]:
        plt.plot(data.loc[id, 'Data'], macd_line[index_shifted], marker='v', color='red')
plt.ylabel('MACD')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.title('MACD')
plt.xticks(rotation=45)
plt.savefig(filename_template.format("macd_zoom_2"), bbox_inches='tight')
plt.close()
