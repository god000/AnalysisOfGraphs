#instument = 'EURUSD'

# файлик с рабочего стояла, кодировка UTF-8 Это важно
f_in = open(r'C:\\Users\\GOD\\Desktop\\AnalysisOfGraphs\\EURUSD60.txt')
lines_in = f_in.readlines()
count_up = 0
count_down = 0
line_splited = ''
delta = 0.0
mas = []
mas_closed = []
mas_time = []
time = ''

### SMA Parametrs
mas_sma_green = []
mas_sma_red = []
green_period = 15
red_period = 30

###
mas_orders = []


#print(lines_in)

# На эту строку забей
f_out = open('C:\\Users\\GOD\\Desktop\\res_analiz.txt', 'w')
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
# Этот массив предназначен для подсчета количества комбинаций мартина( mas[num] = value, num - количество шагов мартина, value - количество цепочек, которые встерчались в истории)
mas_combo = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
cur_count_combo = 1
max_count_combo = 1
isFinishedCombo = False
do_while = True
num_max_combo = 0
#  Входим в цикл, и как только находится подпоследовательность маритна( следующий элемент != текущему элементу ), то зацикливается до тех пор, пока не закончится подпоследовательность мартина ( след эл == текущ. эл)
print(len(mas))
while(do_while):
	while (isFinishedCombo == False):
		cur_count_combo+=1
		if(i == (len(mas)-3)):
			isFinishedCombo = True
			do_while = False
		i+=1		
		if(mas[i]==mas[i+1]):
			isFinishedCombo = True
	#print(i)
	if(cur_count_combo > max_count_combo):
		max_count_combo = cur_count_combo
		num_max_combo = i
	mas_combo[cur_count_combo]+=1
	cur_count_combo = 0 
	isFinishedCombo = False

i = 3
count_proffitable_3 = 0
count_loose_3 = 0
# Тут я посчиткал колиечство удачных и неудачных ставок, если подряд идет две свечи однго цвета, и делаем ставку на то, что следующая будет такго же цвета
while (i != len(mas)):
	if(mas[i]==mas[i-1] and mas[i]==mas[i-2] and mas[i]!=mas[i-3]):
		count_proffitable_3+=1
	elif(mas[i]!=mas[i-1] and mas[i]!=mas[i-2] and mas[i]==mas[i-3]):
		count_loose_3+=1
	i+=1

i = 4
count_proffitable_4 = 0
count_loose_4 = 0
# Тоже самое, только для уже 3х свечей
while (i != len(mas)):
	if(mas[i]==mas[i-1] and mas[i]==mas[i-2] and mas[i]==mas[i-3] and mas[i]!=mas[i-4]):
		count_proffitable_4+=1
	elif(mas[i]!=mas[i-1] and mas[i]!=mas[i-2] and mas[i]!=mas[i-3] and mas[i]==mas[i-4]):
		count_loose_4+=1
	i+=1
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
                

#red
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
		print('-----new order-----')
		#print('cur_pos: ',cur_pos*100000,'i: ', 192-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
		while(mas_buy_and_sell[i] and i<len(mas_closed)-1):
			i+=1
			cur_pos = cur_pos + (mas_closed[i] - mas_closed[i-1])
			print('cur_pos: ',cur_pos*100000,'i: ', len(mas)-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
			
		mas_orders.append(cur_pos*100000)
	cur_pos = 0
	if(mas_buy_and_sell[i]==False):
		mas_index_orders.append(i)
		#cur_pos = cur_pos + (mas_closed[i-1] - mas_closed[i])
		print('-----new order-----')			
		#print('cur_pos: ',cur_pos*100000,'i: ', 192-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
		
		while(mas_buy_and_sell[i]==False and i<len(mas_closed)-1):
			i+=1			
			cur_pos = cur_pos + (mas_closed[i-1] - mas_closed[i])			
			print('cur_pos: ',cur_pos*100000,'i: ', len(mas)-i, '[',mas_time[i],']', 'buy and sell: ', mas_buy_and_sell[i])
			
		mas_orders.append(cur_pos*100000)
			


#print(mas_buy_and_sell)
cur_pos = 0
profit = 0
loose = 0
for cur_pos in mas_orders:
	if(cur_pos>0):
		profit = profit + cur_pos
	else:
		loose = loose + cur_pos
print('count orders: ', len(mas_orders))

print('profit point: ', profit)
print('loose point: ', loose)
print('total point: ', profit+loose)
#print(mas_orders)
#print(mas_index_orders)
print('\n\n\n\n') 
#print(mas_sma_red)
#------------------------------------------------------
print(mas_combo)
print(len(mas))
print('count_up: ' + str(count_up))	#Количество свечей вверх		
print('count_down: ' + str(count_down))	#Количество свечей вниз
print()
print('max_count_combo: ',max_count_combo-1) #максимальная длина мартина 
print('num_max_combo: ', num_max_combo) #последний индекс самой длинной последователности мартина jff
i = 0	
#Три подряд(количество вин/лус ставок)
print('count_proffitable_3: ' + str(count_proffitable_3)) 			
print('count_loose_3: ' + str(count_loose_3))	
#Четыре подряд(количество вин/лус ставок)
print('count_proffitable_4: ' + str(count_proffitable_4))			
print('count_loose_4: ' + str(count_loose_4))																																																																																																																																									
f_out.close()	
