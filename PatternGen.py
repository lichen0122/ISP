######################################################################################################################
########################################### Howard Auto Gen Tools 20201109 ###########################################
######################################################################################################################

import pandas as pd

TAB = '    '
ENDL = '\n'

#new IP modify these##############################################################
IP_NAME = 'ir_nlsc_base_test'
excel_df = pd.read_excel("ir_nlsc_pattern_list.xlsx")
FRAME_NUM = 1
IS_RANDOMIZE = False
PIC_SOURCE_TYPE = 'SSOR_USR_DYNAMIC_RAW12'
IP_SPECIAL_SETTINGS  = '\n' + TAB + TAB + 'sets.tpnr_ir_frame_en = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_ir_frame_sel = 1;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.gray_mode = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.ir_isolate_en = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_tune_assist_en = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_tune_assist_sel = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_half_en = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_pre_frame_en = 1;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_debug_mode = 0;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_y_en = 1;'
IP_SPECIAL_SETTINGS += '\n' + TAB + TAB + 'sets.tpnr_en = 1;'
IP_SPECIAL_SETTINGS = ''
##################################################################################

SIGN = '/***********Howard Auto Gen Tools 20201109***********/\n\n'
EXCEL_COLUMNS = ['testcase','input pattern filename','frame_width','frame_height','rgbir_mode','register setting','number','priority','description']


PATTERN_DEFINE = '`ifndef GUARD_{}_SV\n`define GUARD_{}_SV\n\n'

CLASS_DEF = 'class {} extends {};\n'
UVM_COMPONENT_UTILS = TAB + '`uvm_component_utils({})\n\n'
FUNCTION_NEW = TAB + 'function new(string name="{}", uvm_component parent=null);' + '\n' + TAB + TAB + 'super.new(name, parent);'  + '\n' + TAB+ 'endfunction\n\n'
BUILD_PHASE =  TAB + 'virtual function void build_phase(uvm_phase phase);'        + '\n' + TAB + TAB + 'super.build_phase(phase);' + '\n' + TAB+ 'endfunction\n\n'
CONFIGURE_PHASE  = TAB + 'task configure_phase(uvm_phase phase);' + '\n' + TAB + TAB + 'super.configure_phase(phase);' + '\n' + TAB + TAB + 'phase.raise_objection(this);'

if IS_RANDOMIZE:
    CONFIGURE_PHASE += '\n' + TAB + TAB + 'sets.reset();' + '\n' + TAB + TAB + 'assert(sets.randomize() with'
    CONFIGURE_PHASE += '{}\n{}' + TAB + TAB  + '{});'
else:
    CONFIGURE_PHASE += '\n\n' + TAB + TAB + 'sets.reset();';
    CONFIGURE_PHASE += '\n' + TAB + TAB + 'assert(sets.randomize());';
    CONFIGURE_PHASE += '\n\n{}'
    

CONFIGURE_PHASE += '{}'
#CONFIGURE_PHASE += '\n' + TAB + TAB + 'sets.source_type = SSOR_USR_RAW12;';
#CONFIGURE_PHASE += '\n' + TAB + TAB + 'sets.pic_name = "../../image/{}";'
#CONFIGURE_PHASE += '\n' + TAB + TAB + 'sets.dither_en = 0;'
CONFIGURE_PHASE += '\n' + TAB + TAB + 'sets.post_randomize();'
CONFIGURE_PHASE += '\n\n' + TAB + TAB + 'phase.drop_objection(this);'
CONFIGURE_PHASE += '\n' + TAB + 'endtask\n'
ENDCLASS = 'endclass\n'
END_DEFINE = '`endif\n'


df = pd.DataFrame(excel_df, columns=EXCEL_COLUMNS)
for row in df.iloc[0:].values.tolist():
    ROWS = {}
    count = 0
    for col_name in EXCEL_COLUMNS:
        ROWS.update( {col_name: row[count]} )
        count += 1

    testcase = ROWS['testcase']
    f = open(ROWS['testcase'] + ".sv", "w")
    f.write(SIGN)
    f.write(PATTERN_DEFINE.format(testcase, testcase))
    f.write(CLASS_DEF.format(testcase, IP_NAME))
    f.write(UVM_COMPONENT_UTILS.format(testcase))
    f.write(FUNCTION_NEW.format(testcase))
    f.write(BUILD_PHASE)
    
    if IS_RANDOMIZE:
        register_setting  = TAB + TAB + TAB + 'width  == {};\n'.format(ROWS['frame_width']) if ROWS['frame_width'] != 'random' else ''
        register_setting += TAB + TAB + TAB + 'height == {};\n'.format(ROWS['frame_height']) if ROWS['frame_height'] != 'random' else ''
        register_setting += TAB + TAB + TAB + 'frame_num == {};\n'.format(FRAME_NUM)
    else:
        register_setting  = TAB + TAB + 'sets.width  = {};\n'.format(ROWS['frame_width']) if ROWS['frame_width'] != 'random' else ''
        register_setting += TAB + TAB + 'sets.height = {};\n'.format(ROWS['frame_height']) if ROWS['frame_height'] != 'random' else ''
        register_setting += TAB + TAB + 'sets.frame_num = {};\n'.format(FRAME_NUM)
    
    
    if not ROWS['register setting'] == 'random':
        register_setting_file = open( ROWS['register setting'] + ".txt", "r")
        for line in register_setting_file.readlines():
            if IS_RANDOMIZE:
                register_setting += TAB + TAB + TAB + line.replace('sets.','')
            else:
                register_setting += TAB + TAB + line.replace('==', '=')
        register_setting_file.close()
        #f.write(CONFIGURE_PHASE.format('{', register_setting, '}', ROWS['input pattern filename']))

        
    if ROWS['input pattern filename'] == 'random':
        PIC_SOURCE  = '\n' + TAB + TAB + 'sets.source_type = SSOR_RANDOM;';
    else:
        PIC_SOURCE  = '\n' + TAB + TAB + 'sets.source_type = {};'.format(PIC_SOURCE_TYPE);
        PIC_SOURCE += '\n' + TAB + TAB + 'sets.pic_name = "../../image/{}";'.format(ROWS['input pattern filename'])
        
    if IS_RANDOMIZE:
        f.write(CONFIGURE_PHASE.format('{', register_setting, '}', PIC_SOURCE + IP_SPECIAL_SETTINGS))
    else:
        f.write(CONFIGURE_PHASE.format(register_setting, PIC_SOURCE + IP_SPECIAL_SETTINGS))

    f.write(ENDCLASS)
    f.write(END_DEFINE)

    f.close()
