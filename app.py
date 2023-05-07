#Importing libraries
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import base64


#Function to reframe symbol
def process_symbol(symbol):

    day = datetime.now().day
    
    sym_sp = symbol.split()

    # underlying = symbol[0:10] if symbol[0] == 'B' else symbol[0:6]
    underlying = sym_sp[0]
    month = sym_sp[1][-7:-4]
    day = sym_sp[1][:-7]
    year = sym_sp[1][-4:]
    opt_type = sym_sp[2]
    strike = "{:.2f}".format(float(sym_sp[3]))

    if int(day) < 10:
        return ''.join(['OPTIDX',underlying,month,'  ',str(int(day)),' ',year,opt_type,strike])
    else:
        return ''.join(['OPTIDX',underlying,month,' ',day,' ',year,opt_type,strike])


    

#Calculate qty according to Buy or Sell
def calculate_qty(qty,bs):
    if bs == 'B':
        return qty * 1
    else:
        return qty*(-1)
 
#Download excel file
# def download_excel(df):
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='Sheet1', index=False)
#     writer.save()
#     output.seek(0)
#     return output


#--------------------Streamlit UI -------------------------------------------
st.title('Sheet Converter')

file = st.file_uploader('Upload CSV File')




if file:
    data = pd.read_excel(file)
    st.write(data)
    data['TraderID'] = 10548
    data['ClientTrCode'] = 2683052
    data['ClientCode'] = 'A200'
    data['SeriesCode'] = data['CONTRACT'].apply(process_symbol)
    data['Qty'] = data.apply(lambda x : calculate_qty(x['EXECUTED QTY'],x['BUY SELL']),axis=1)
    data['MktRate'] = data['EXEC PRICE']
    data['OrderNo'] = 1
    data['TradeNo'] = 1
    data['TradeTime'] = 1
    data['TrType'] = 1

    new_df = data[['TraderID','ClientTrCode','ClientCode','SeriesCode','Qty','MktRate','OrderNo','TradeNo','TradeTime','TrType']]


    st.write('Converted Dataframe')
    
    st.dataframe(new_df)

    # output_file = download_excel(new_df)


if st.button('Download Excel'):
    # Create a bytes buffer for the Excel file
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')
    new_df.to_excel(excel_writer, index=False, sheet_name='Sheet1')
    excel_writer.save()
    excel_data = excel_buffer.getvalue()

    # Encode the bytes buffer data in base64
    b64 = base64.b64encode(excel_data).decode()

    # Create a download link
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="my_data.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)