import sqlite3
 
conn = sqlite3.connect("db\\mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# файлик с рабочего стояла, кодировка UTF-8 Это важно
f_in = open(r'C:\\Users\\GOD\\Desktop\\AnalysisOfGraphs\\Pairs\EURJPY1440.txt')
lines_in = f_in.readlines()
line_splited = ''
delta = 0.0
count_down = 0
count_up = 0
mas = []
mas_closed = []
mas_time = []

### SMA Parametrs
mas_sma_green = []
mas_sma_red = []
green_period = 1
red_period = 2

###
mas_orders = []

cursor.execute("""CREATE TABLE EUR_JPY_D1
              (green_period integer, red_period integer, profit integer,
               count_orders integer, income_points integer, loose_points integer)
           """)
#print(lines_in)
#Распарсиваю файл, чтоб получить mas[] 
for cur_line in lines_in:
	#print(cur_line) 
	line_splited = cur_line.split(',')
	delta = float(line_splited[5]) - float(line_splited[2])
	time = line_splited[0] +' '+ line_splited[1]
	mas_closed.append(float(line_splited[5]));
	mas_time.append(time)
	if delta>0:
		#print(1, end='')
		mas.append(1)
		count_up+=1
	elif delta<0:
		#print(0, end='')
		mas.append(0)
		count_down+=1
	else:
		mas.append(2)

# с этого момента у тебя есть mas[], в котором 1 - зеленая свеча, 0 - крсная свеча, 2 - нейтральная

i = 0

# Подсчет массива со значениями SMA
def count_mas_sma(mas_closed, period):        
        i = period-1
        mas_sma_res = [0.0] * i
        sum = 0
        
        while(i<len(mas_closed)):
                for pos in range(i-period+1,i+1,1):                	
                        sum = sum + mas_closed[pos]
                mas_sma_res.append(sum/period)
                sum = 0
                i+=1

        return mas_sma_res
                
for green_period in range(1,101,1):
	for red_period in range(green_period+1,101,1):		
		mas_orders = []
		mas_sma_green = count_mas_sma(mas_closed,green_period)
		mas_sma_red = count_mas_sma(mas_closed,red_period)
		i = red_period-1
		#for i in range(red_period-1, len(mas_closed)-1,1):

		# mas_buy_ sell - Буллианский массив со значениями сделки на покупку или продажу
		mas_buy_and_sell = [False] * (red_period-1)
		mas_index_orders = []

		for i in range(red_period-1,len(mas_sma_red),1):
			if(mas_sma_green[i]>mas_sma_red[i]):
				mas_buy_and_sell.append(True)
			else:
				mas_buy_and_sell.append(False)
			#print('i: ', 192-i,' buy_and_sell: ', mas_sma_green[i]>mas_sma_red[i])
#------------------------
		i = red_period-1
		while(i<len(mas_closed)-1):
			cur_pos = 0
			if(mas_buy_and_sell[i]):
				mas_index_orders.append(i)
				#cur_pos = cur_pos + (mas_closed[i] - mas_closed[i-1])
				#print('-----new order-----')
				#print('cur_pos: ',cur_pos*100000,'i: ', 192-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
				while(mas_buy_and_sell[i] and i<len(mas_closed)-1):
					i+=1
					cur_pos = cur_pos + (mas_closed[i] - mas_closed[i-1])			
				mas_orders.append(cur_pos*100000)

			cur_pos = 0
			if(mas_buy_and_sell[i]==False):
				mas_index_orders.append(i)
				#cur_pos = cur_pos + (mas_closed[i-1] - mas_closed[i])
				#print('-----new order-----')			
				#print('cur_pos: ',cur_pos*100000,'i: ', 192-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
				
				while(mas_buy_and_sell[i]==False and i<len(mas_closed)-1):
					i+=1			
					cur_pos = cur_pos + (mas_closed[i-1] - mas_closed[i])			
				mas_orders.append(cur_pos*100000) 
					


		#print(mas_buy_and_sell)
		cur_pos = 0
		income = 0
		loose = 0
		for cur_pos in mas_orders:
			if(cur_pos>0):
				income = income + cur_pos
			else:
				loose = loose + cur_pos
		profit = income + loose
		count_orders = len(mas_orders) 
		cursor.execute(""" INSERT INTO EUR_JPY_D1 (green_period, red_period, profit, count_orders, income_points, loose_points)
			VALUES (?,?,?,?,?,?)""", (green_period, red_period, profit, count_orders, income, loose)
			)
		'''print('SMA: (', green_period, ',', red_period, ')' )
		print('count orders: ', len(mas_orders))
		print('incom point: ', income)
		print('loose point: ', loose)
		print('profit: ', profit)
		#print(mas_orders)
		#print(mas_index_orders)
		print('\n\n\n\n') 
		conn.commit()
		#print(mas_sma_red)'''

#------------------------------------------------------				
conn.commit();