import pandas as pd
import numpy as np
import math
import sys 
import plotly.express as px 

DILUTION_DICT = {'D01': 200,
				'D02': 2000, 
				'D03': 20000,
				'D04': 40000,
				'D05': 80000,
				'D06': 160000,
				'D07': 320000,
				'D08': 640000, 
				'D09': 1280000,
				'D10': 2560000,
				'D11': 5120000,
				'D12': 10240000, 
				"D13": 20480000, 
				"D14": 40960000,
				"D15": 40960000 * 2, 
				"D16": 40960000 * 4}

from decimal import Decimal

MIN_FLOAT = -9999999

def analysis(input_data, plate_map, output_name):
    
	s1, s2 = list(), list(),
	for well in [(i[0], int(i[1:])) for i in input_data['Well']]:
	    try:
	        desc = plate_map.loc[well[0], str(well[1])].split()
	        if len(desc) == 2:
	            s1.append(desc[0]+ ' ' +desc[1])
	            s2.append('')

	        elif len(desc) == 3:
	            s1.append(desc[0] + ' ' + desc[1])

	            Dilution = desc[2]
	            if len(Dilution) == 2 and Dilution[0] == "D":
	                Dilution = '0'.join(list(Dilution))

	            s2.append(Dilution)
	    except:
	        s1.append("NA")
	        s2.append("NA")
	input_data["Vector"] = s1
	input_data["Condition"] = s2

	sorted_input_data = input_data.sort_values(["Vector", "Condition", "Well"], ascending = (True, True, True))
	sorted_input_data = sorted_input_data.loc[sorted_input_data['Vector'].str.contains('NTC') == False ]
	sorted_input_data = sorted_input_data[['Vector', 'Condition', 'Well',  'Conc(copies/µL)' , 'Accepted Droplets']]
	sorted_input_data = sorted_input_data[sorted_input_data['Vector']!="NA"]

	def format_conc(x) : 
		if x == 'No Call':
			return 'No Call'
		else:
			return str(float(x.replace(',', '')))

	sorted_input_data['Conc(copies/µL)']= (sorted_input_data['Conc(copies/µL)'].apply(lambda x: format_conc(x)))

	def get_dilution(Cond, dilution_dict):
	    return dilution_dict[Cond]

	sorted_input_data['Dilution Factor'] = sorted_input_data['Condition'].apply(lambda x: get_dilution(x, DILUTION_DICT)) 


	def get_vg(sample, dilution, conc, accepted_droplets):
	    if conc == "No Call" or float(conc) >= 1000000 or int(accepted_droplets)<10000:
	        
	        return MIN_FLOAT
	    else:
	        if 'ITR' in sample:
	            return 100*25*dilution*float(conc)
	        else:
	            return 200*25*dilution*float(conc)

	sorted_input_data['vg/ml'] = sorted_input_data.apply(lambda x: get_vg(x['Vector'], x['Dilution Factor'], x['Conc(copies/µL)'], x['Accepted Droplets']), axis=1)


	calculations = sorted_input_data[(sorted_input_data['Conc(copies/µL)'] != 'No Call')  & 
	                                 (sorted_input_data['Conc(copies/µL)'] != '1000000.00' ) &
	                                (sorted_input_data['Accepted Droplets'] >= 10000)].groupby(['Vector', 'Condition'])['vg/ml'].aggregate([np.mean, np.std]).reset_index()
	def get_mean(sample, dilution):
	    return float(calculations[(calculations['Vector'] == sample) & (calculations['Condition'] == dilution)]['mean'])
	def get_std(sample, dilution):
	    return float(calculations[(calculations['Vector'] == sample) & (calculations['Condition'] == dilution)]['std'])
	sorted_input_data['mean'] = sorted_input_data.apply(lambda x: get_mean(x['Vector'], x['Condition']), axis=1)
	sorted_input_data['std'] = sorted_input_data.apply(lambda x: get_std(x['Vector'], x['Condition']), axis=1)
	sorted_input_data['RSD'] = round(sorted_input_data['std']/sorted_input_data['mean'] * 100,2)


	linearity_dict = dict()
	for i in set(sorted_input_data["Vector"]):
	    vector_data = sorted_input_data[sorted_input_data['Vector'] == i]
	    for index in range(len(sorted(set(vector_data['Condition'])))-1):
	        
	        cur = [i for i in vector_data[(vector_data['Vector'] == i) & (vector_data['Condition'] == sorted(set(vector_data['Condition']))[index])]['vg/ml'] if i != MIN_FLOAT]
	        next = [i for i in vector_data[(vector_data['Vector'] == i) & \
	                (vector_data['Condition'] == sorted(set(vector_data['Condition']))[index+1])]['vg/ml'] if i != MIN_FLOAT]
	        
	        mean_cur = np.mean(cur)
	        mean_next = np.mean(next) 
	        RSD = round(mean_cur/mean_next,3)
	        linearity_dict[(i , sorted(set(vector_data['Condition']))[index])] = RSD


	def populate_rsd(Condition, Vector):
	    index = (Vector, Condition)
	    return round(linearity_dict.get(index, MIN_FLOAT) ,2)
	    

	sorted_input_data['linearity'] = sorted_input_data.apply(lambda x: populate_rsd(x['Condition'], x['Vector']), axis=1)
	def convert_to_science(x):
	    if x != MIN_FLOAT:
	        return '%.2E'% Decimal(str(x))
	    else:
	        return(str(x))
	               
	sorted_input_data['Dilution Factor'] = sorted_input_data['Dilution Factor'].apply(lambda x: convert_to_science(x))
	sorted_input_data['mean'] = sorted_input_data['mean'].apply(lambda x: convert_to_science(x))
	sorted_input_data['std'] = sorted_input_data['std'].apply(lambda x: convert_to_science(x))
	sorted_input_data_NTC = input_data.sort_values(["Vector", "Condition", "Well"], ascending = (True, True, True))
	sorted_input_data_NTC = sorted_input_data_NTC.loc[sorted_input_data_NTC['Vector'].str.contains('NTC') ]

	sorted_input_data_NTC['Conc(copies/µL)'] = pd.to_numeric(sorted_input_data_NTC['Conc(copies/µL)'])
	NTC_calculations = sorted_input_data_NTC[(sorted_input_data_NTC['Conc(copies/µL)'] != 'No Call')& 
	                                 (sorted_input_data_NTC['Conc(copies/µL)'] != '1000000.00' ) &
	                                (sorted_input_data_NTC['Accepted Droplets'] >= 10000)].groupby(['Vector'])['Conc(copies/µL)'].aggregate([np.mean]).reset_index()


	sorted_input_data['vg/ml'] = pd.to_numeric(sorted_input_data['vg/ml'])
	summary_sorted_input_data = sorted_input_data[sorted_input_data['vg/ml'] != MIN_FLOAT]
	summary_sorted_input_data = summary_sorted_input_data.groupby(['Vector'])['vg/ml'].aggregate([np.mean, np.std]).reset_index()
	summary_sorted_input_data["RSD"] = round(summary_sorted_input_data['std']/summary_sorted_input_data['mean'] * 100,2)
	summary_sorted_input_data['mean'] = summary_sorted_input_data['mean'].apply(lambda x: convert_to_science(x))
	summary_sorted_input_data['std'] = summary_sorted_input_data['std'].apply(lambda x: convert_to_science(x))
	sorted_input_data['vg/ml'] = sorted_input_data['vg/ml'].apply(lambda x: convert_to_science(x))


	prev = ""
	mean = []
	std = []
	RSD = []
	Linearity = []
	for i in sorted_input_data.iterrows():
	    curr = (i[1]['Vector'], i[1]["Condition"])
	    if curr != prev :
	        mean.append(i[1]['mean'] if i[1]['mean'] != MIN_FLOAT else '')
	        std.append(i[1]['std'] if i[1]['std'] != MIN_FLOAT else '')
	        RSD.append(i[1]['RSD'] if i[1]['RSD'] != MIN_FLOAT else '')
	        Linearity.append(i[1]['linearity'] if i[1]['linearity'] != MIN_FLOAT else '')
	    else:
	        mean.append('')
	        std.append('')
	        RSD.append('')
	        Linearity.append('')
	    prev = curr
	sorted_input_data['mean'] = mean
	sorted_input_data['std'] = std
	sorted_input_data['RSD'] = RSD
	sorted_input_data['linearity'] = Linearity

	sorted_input_data = sorted_input_data.merge(summary_sorted_input_data, left_on='Vector', right_on='Vector',
	          suffixes=('', '_summary'))




	mean = []
	std = []
	RSD = []
	prev = ""

	for i in sorted_input_data.iterrows():
	    curr = (i[1]['Vector'])
	    if curr != prev :
	        mean.append(i[1]['mean_summary'] if i[1]['mean_summary'] != MIN_FLOAT else '')
	        std.append(i[1]['std_summary'] if i[1]['std_summary'] != MIN_FLOAT else '')
	        RSD.append(i[1]['RSD_summary'] if i[1]['RSD_summary'] != MIN_FLOAT else '')
	    else:
	        mean.append('')
	        std.append('')
	        RSD.append('')
	    prev = curr
	sorted_input_data['mean_summary'] = mean
	sorted_input_data['std_summary'] = std
	sorted_input_data['RSD_summary'] = RSD

	columns = []
	for i in sorted_input_data_NTC:
	    if i in sorted_input_data:
	        columns.append(i)


	sorted_input_data_NTC = sorted_input_data_NTC[columns]
	sorted_input_data_NTC = sorted_input_data_NTC.merge(NTC_calculations, left_on='Vector', right_on='Vector')


	mean = []

	prev = ""

	for i in sorted_input_data_NTC.iterrows():
	    curr = (i[1]['Vector'])
	    if curr != prev :
	        mean.append(i[1]['mean'] if i[1]['mean'] != MIN_FLOAT else '')
	      
	    else:
	        mean.append('')
	       
	    prev = curr
	sorted_input_data_NTC['mean'] = mean
	sorted_input_data_NTC


	result = pd.concat([sorted_input_data, sorted_input_data_NTC], ignore_index=True, sort=False) 
	unique_vector = set(result['Vector'])
	colors = list(px.colors.qualitative.T10)
	colors = [i for i in colors if i !='#E45756']
	colors = 2*list(colors)
	colors = colors[:len(unique_vector)]
	colors_dict = dict(zip(unique_vector, colors))

	def _RSD_problem(val, props = '', subset = None):
		if val == '':
			return None
		elif float(val) > 8:
			return props
		return None

	def _Lin_problem(val, props = '', subset = None):
		if val == '':
			return None
		elif float(val) >= 1.1 or float(val) <= 0.9:
			return props
		return None

	def highlight_colors(x) :
		lis = []
		df1 = pd.DataFrame('', index=x.index, columns=x.columns)

		for i in x['Vector']:
			color = colors_dict[i]
			df1.loc[(x['Vector'] == i) ]  = 'background-color: ' + color
		
		return df1

    
	result = result.style.applymap(_Lin_problem, props  = 'color:red;font-weight:bold', subset=pd.IndexSlice[:, ['linearity']])
	result.applymap(_RSD_problem, props  = 'color:red;font-weight:bold', subset=pd.IndexSlice[:, ['RSD']])
	result.apply(highlight_colors, axis = None)

	with pd.ExcelWriter(output_name) as writer:
	    result.to_excel(writer, sheet_name='Output_Data', index = False)
	    NTC_calculations.to_excel(writer, sheet_name='NTC_Summary', index = False)
	    summary_sorted_input_data.to_excel(writer, sheet_name='Full_Summary', index = False)

	print("PROCESS COMPLETE")

if __name__ == "__main__":
	out_put = sys.argv[1]
	input_data = pd.read_csv(out_put + "/input_data.csv", encoding = 'utf8')
	channel = set(input_data['Target'])
	plate_map = pd.read_csv(out_put + "/plate_map.csv",  index_col = "Map")
	for i in channel:
		channel_input_data = input_data[input_data['Target'] == i]
		analysis(channel_input_data, plate_map, out_put + "/output channel " + str(i) + '.xlsx')

