# -*- coding: utf-8 -*-
"""
根据原始数据文件及指定的判定规则，增加数据文件的标签列
"""

import pandas as pd
import os
import streamlit as st
from io import BytesIO
import xlsxwriter

# 定义输出Excel的功能
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

ready = False

# 页面绘制
st.title('原始数据处理')
st.info('请上传原始csv文件和指明conditions的excel表格，页面处理后可直接下载处理结果')
st.write(' ')

st.write('请上传原始数据CSV文件')
file0 = st.file_uploader('打开文件',['csv'])

# st.write('请上传条件1的Excel文件')
# file1 = st.file_uploader('打开文件',['xlsx'],key=10)

# st.write('请上传条件2的Excel文件')
# file2 = st.file_uploader('打开文件',['xlsx'],key=11)

op_name = st.text_input('请输入输出文件名','output')

if file0 is not None:
    ready = True

if ready == True:
    ori = pd.read_csv(file0)
    cond1 = pd.read_excel('FigureMatching_Conditions1.xlsx')
    cond2 = pd.read_excel('FigureMatching_Conditions2.xlsx')
    # st.dataframe(ori)
    
    # 转换操作
    ori_image = ori['FMPicture'].values.tolist()
    ori_block = ori['FMBlock'].values.tolist()
    ori_num = ori['FM_trials_loop.thisN'].values.tolist()

    cong = []
    trialtype = []
    corans = []
    itemid = []
    switchtype = []

    for i in ori_image:
        if str(i) == 'nan':
            cong.append('nan')
            trialtype.append('nan')
            corans.append('nan')
            itemid.append('nan')
            
        else:
            data1 = cond1.loc[cond1['FM_trials_image'] == i]
            cong.append(data1['FM_trials_congruency'].values[0])
            trialtype.append(data1['FM_trials_tasktype'].values[0])
            corans.append(data1['FM_trials_correctanswer'].values[0])
            itemid.append(data1['FM_trials_itemID'].values[0])

    for j in range(len(ori_block)):
        if str(ori_num[j]) == 'nan':
            switchtype.append('nan')
        elif ori_block[j] == 'CSCS':
            switchtype.append('CSCS')
        else:
            data2 = cond2.loc[(cond2['block']==ori_block[j]) & (cond2['num']==ori_num[j])]
            switchtype.append(data2['FM_trials_switchtype'].values[0])

    ori['FM_trials_congruency'] = cong
    ori['FM_trials_type'] = trialtype
    ori['FM_trials_correctanswer'] = corans
    ori['FM_trials_itemID'] = itemid
    ori['FM_trials_switchtype'] = switchtype
    op = to_excel(ori)
    filename = op_name + '.xlsx'

    st.download_button('点击下载',data=op,file_name=filename)
else:
    st.write('请先完成文件上传的操作')