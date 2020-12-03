######################################################################################################################
########################################### Howard Auto Gen Tools 20201109 ###########################################
######################################################################################################################

import pandas as pd

#new IP modify these###############################
register_settings = ['Normal', 'COEF_RANDOM', 'ENABLE_RANDOM', 'TUNE_ASSIST', 'MAX', 'MIN', 'YIIR_OUTER_NR', 'ISOLATE_NR', 'UVIIR', 'EDGE_UVS', 'Dither', 'GLOBAL_UVS']
register_settings = ['NORMAL','COEF_RANDOM','ENABLE_RANDOM','TUNE_ASSIST','MAX','MIN','Y_IIR_OUTER_NR','ISOLATE_NR','DITHER']
register_settings = ['Normal', 'Normal-A', 'ADJRATE', 'RGBIR_LENS_MODE', 'RANDOM_CENTER']
register_settings = ['Normal','P_RANDOM','ENABLE_RANDOM','TUNE_ASSIST','MAX','MIN']
register_settings = ['Normal']
excel_df = pd.read_excel("ISP_Config_gray_nlsc.xlsx")
###################################################

RTL_NET_NAME = 'RTL Net Name'

TABS = '      '
postfix = ' \ \n'
postfix = ' '
MERGE = False
LINEBYLINE = MERGE

if not LINEBYLINE:
    postfix = '\n'
else:
    postfix = ' '

if MERGE:
    f = open("all.txt", "w")

for register_setting in register_settings:
    df = pd.DataFrame(excel_df, columns=[register_setting, RTL_NET_NAME])
    if not MERGE:
        f = open(register_setting + ".txt", "w")
    if LINEBYLINE:
        f.write('`define {} '.format(register_setting))

    for row in df.iloc[0:].values.tolist():
        if str(row[0]) != 'random':
            if int(row[0]) >= 0:
                f.write('sets.' + str(row[1]) + ' == ' + str(row[0]) + ';')
            else:
                to_unsigned = "unsigned'(15'(" + str(row[0]) + "))"
                f.write('sets.' + str(row[1]) + ' == ' +  to_unsigned  + ';')
            f.write(postfix)
                
    f.write('\n')
    if not MERGE:
        f.close()
if MERGE:
    f.close()