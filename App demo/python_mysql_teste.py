import mysql.connector
import xlrd

mydb_data = input("Insira os dados de conexão: " ).split()

mydb = mysql.connector.connect(host = mydb_data[0],
                               user = mydb_data[1],
                               passwd = mydb_data[2],
                               database = mydb_data[3],
                               autocommit=True)

mycursor = mydb.cursor()

show_tab = "SHOW tables from " + mydb_data[3]

mycursor.execute(show_tab)

all_tab = mycursor.fetchall()

for x in all_tab:
    print("Table " + x[0])
    show_col = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + x[0] + "' AND table_schema = '" + mydb_data[3] +"'"
    mycursor.execute(show_col)

    all_col = mycursor.fetchall()

    for y in all_col:
        print(" Column " + y[0])

mod_tab = input("Selecione a tabela a ser modificada: ")
mod_col = input("Selecione as colunas a serem modificadas: ").split()
mod_type = input("Selecione o tipo de modificação: ")
loc = input("Insira o path do arquivo excel: ")    

if int(mod_type):
    try:
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0)
        PK_name = sheet.cell_value(0,0)
        id_list = [str(int(sheet.cell_value(x, 0)))  for x in range(1, sheet.nrows)]
        for x in id_list:
                s_col = "DELETE FROM "+mod_tab+" WHERE "+PK_name+" = "+ x
                mycursor.execute(s_col)
    except:
        s_col = "DROP TABLE "+mod_tab
        mycursor.execute(s_col)
else:
    try:
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0)
        PK_name = sheet.cell_value(0,0)
        id_list = [str(int(sheet.cell_value(x, 0)))  for x in range(1, sheet.nrows)]
        mod_list = [[sheet.cell_value(x, y)  for x in range(1, sheet.nrows)] for y in range(1,len(mod_col)+1)]
        for x in range(len(mod_col)):
            for y in range(len(id_list)):
                val = mod_list[x][y]
                if isinstance(val,str):
                    val = "'"+val+"'"
                else:
                    val = str(int(val))
                s_col = "UPDATE "+mod_tab+" SET "+mod_col[x]+" = "+ val +" WHERE "+PK_name+" = "+id_list[y]
                mycursor.execute(s_col)
    except:
        for x in mod_col:
            s_col = "UPDATE "+mod_tab+" SET "+x+" = null"
            mycursor.execute(s_col)
