
import numpy as np
from matplotlib import pyplot as plt

# assisting functions, main function at line 236
# function no.1 : organizing data into a 2D list
    # dropping \n, changing uppercase to lower case and removing multiple spaces
    # and removing axis titles from the data table.
def orgazining_data(unorganized_list):
    data = []
    for item in unorganized_list:
        organized = item.replace("\n", "").replace("\t"," ").strip()
        if 'x axis' in item.lower():
            x_axis = item[7:].strip()
        elif 'y axis' in item.lower():
            y_axis = item[8:].strip()
        elif organized != "":  # appending only lines that are not empy
            data.append(organized.lower().strip())
        # turning data to a 2-D list of floats
    organized_2D_list = []
    for i in range(0, len(data)):
        removing_multiple_spaces = ' '.join(data[i].split())
        organized_2D_list.append(removing_multiple_spaces.split(" "))
    for item in organized_2D_list:
        for j in range(0, len(item)):
            try:
                item[j] = float(item[j])
            except(ValueError):
                continue
    return (organized_2D_list,x_axis,y_axis)


# function no. 2: finding out if data is in rows or columns
def columns_or_rows(list_2D):
    first_item_is_string=0
    for item in list_2D:
        if type(item[0])==str:
            first_item_is_string+=1
    if first_item_is_string==4:
        return "rows"
    else:
        return "columns"


#function no.3 : checking the data for missing cells\ uncertenties<=0
def data_check(list_2D):
    #checking for missing cells
    for item in list_2D:
        if len(item)!=len(list_2D[0]):
            return "Input file error: Data lists are not the same length"
    if columns_or_rows(list_2D)=="rows": #if data is organized in rows
        for row in list_2D:
            if row[0][0]=="d": #checking only uncertenties
                for cell in row:
                    try:
                        if cell<=0:
                            return "Input file error: Not all uncertainties are positive"
                    except(TypeError):
                        continue
    else: #data in columns
        for i in range(0,4):
            if list_2D[0][i][0]=="d": #checking only uncertenties
                for row in list_2D:
                    if row == list_2D[0]: #first row does not contain numbers
                        continue
                    elif row[i]<=0:
                        return "Input file error: Not all uncertainties are positive"
    return ("all good")


#function no. 4: making a dictionary with needed objects for calculations
def dictionary_of_needed_objects(list_2D):
    objects={}
    xs=[]
    ys=[]
    dys=[]
    dxs=[]
    #checking if data is in rows\columns and seperating x values,y values and dy values.
    if columns_or_rows(list_2D)=="rows":
        for item in list_2D:
            if item[0]=='x':
                xs=item[1:]
            elif item[0]=='y':
                ys=item[1:]
            elif item[0]=='dy':
                dys=item[1:]
            elif item[0]=='dx':
                dxs=item[1:]
    else: #if data is in columns
        for i in range(0,4):
            if list_2D[0][i]=='x':
                for row in list_2D:
                    if type(row[i]) == float:
                        xs.append(row[i])
            elif list_2D[0][i]=='y':
                for row in list_2D:
                    if type(row[i]) == float:
                        ys.append(row[i])
            elif list_2D[0][i]=='dy':
                for row in list_2D:
                    if type(row[i])==float:
                        dys.append(row[i])
            elif list_2D[0][i]=='dx':
                for row in list_2D:
                    if type(row[i])==float:
                        dxs.append(row[i])
    objects["xs"]=xs
    objects["ys"]=ys
    objects["dys"]=dys
    objects["dxs"]=dxs
    N=len(xs)
    objects['N']=N

    # list of yi * xi
    xys=[]
    for i in range(0,(len(xs))):
        xys.append(xs[i]*ys[i])
    # list of dy squared
    dys_squared=[]
    for i in range(0, (len(xs))):
        dys_squared.append(dys[i]**2)
    # list of x squared
    xs_squared=[]
    for i in range(0, len(xs)):
        xs_squared.append(xs[i]**2)

    #calculating function parameters
    #a
    a=(wa(xys,dys)-(wa(xs,dys)*wa(ys,dys)))/(wa(xs_squared,dys)-wa(xs,dys)**2)
    objects["a"]=a

    #calculating b
    b=wa(ys,dys)-a*wa(xs,dys)
    objects['b']=b

    #calculating da
    da_squared= wa(dys_squared,dys)/(N*(wa(xs_squared,dys)-(wa(xs,dys))**2))
    objects['da']=(da_squared)**0.5

    #calculating db
    db_squared=(wa(dys_squared,dys)*wa(xs_squared,dys))/(N*(wa(xs_squared,dys)-(wa(xs,dys))**2))
    objects['db']=(db_squared)**0.5

    #calculating chi squared (and reduced)
    chi_squared=0
    for i in range(0,len(xs)):
        chi_squared+=((ys[i]-(a*xs[i]+b))/dys[i])**2
    chi_squared_reduced=chi_squared/(N-2)
    objects['chi_squared_reduced']=chi_squared_reduced
    objects['chi_squared']=chi_squared

    return objects

    #calculating b


#function no.5 calculating weighted average (wa)
def wa(zs,dys):
    summ_of_zs_over_squared_dys=0
    summ_of_1_over_squared_dys=0
    for i in range(0,len(zs)):
        summ_of_zs_over_squared_dys+=(zs[i]/(dys[i]**2))
        summ_of_1_over_squared_dys+=1/(dys[i]**2)
    return summ_of_zs_over_squared_dys/summ_of_1_over_squared_dys


#function no. 6 organizing data for the Bonus assignment
def orgazining_data_bonus(unorganized_list):
    data = []
    for item in unorganized_list:
        organized = item.replace("\n", "").replace("\t"," ").strip()
        if 'x axis' in item.lower():
            x_axis = item[7:].strip()
        elif 'y axis' in item.lower():
            y_axis = item[8:].strip()
        elif organized != "":  # appending only lines that are not empy
            data.append(organized.lower().strip())
        # turning data to a 2-D list of floats
    organized_2D_list = []
    for i in range(0, len(data)):
        removing_multiple_spaces = ' '.join(data[i].split())
        organized_2D_list.append(removing_multiple_spaces.split(" "))
    for item in organized_2D_list:
        for j in range(0, len(item)):
            try:
                item[j] = float(item[j])
            except(ValueError):
                continue
    a_data=organized_2D_list.pop(-2)
    b_data=organized_2D_list.pop(-1)
    return (organized_2D_list, x_axis, y_axis,a_data,b_data)


#function no.7 making dictionary for bonus assignment:
def dictionary_Bonus(list_2D):
    objects={}
    xs=[]
    ys=[]
    dys=[]
    dxs=[]
    #checking if data is in rows\columns and seperating x values,y values and dy values.
    if columns_or_rows(list_2D)=="rows":
        for item in list_2D:
            if item[0]=='x':
                xs=item[1:]
            elif item[0]=='y':
                ys=item[1:]
            elif item[0]=='dy':
                dys=item[1:]
            elif item[0]=='dx':
                dxs=item[1:]
    else: #if data is in columns
        for i in range(0,4):
            if list_2D[0][i]=='x':
                for row in list_2D:
                    if type(row[i]) == float:
                        xs.append(row[i])
            elif list_2D[0][i]=='y':
                for row in list_2D:
                    if type(row[i]) == float:
                        ys.append(row[i])
            elif list_2D[0][i]=='dy':
                for row in list_2D:
                    if type(row[i])==float:
                        dys.append(row[i])
            elif list_2D[0][i]=='dx':
                for row in list_2D:
                    if type(row[i])==float:
                        dxs.append(row[i])
    objects["xs"]=xs
    objects["ys"]=ys
    objects["dys"]=dys
    objects["dxs"]=dxs
    N=len(xs)
    objects['N']=N
    return objects

# Main function
def fit_linear(filename):
    filename_string=str(filename)
    file_open=open(filename_string,'r')
    raw_data=file_open.readlines()
    file_open.close()

    data_2D_list=orgazining_data(raw_data)[0]
    x_axis=orgazining_data(raw_data)[1]
    y_axis=orgazining_data(raw_data)[2]
    if data_check(data_2D_list)!="all good":
        print(data_check(data_2D_list))
        return None
    elif len(data_2D_list)<4 or len(data_2D_list[0])<4:
        print ("Input file error: File doesn't contain enough data points")
        return None
    dic=dictionary_of_needed_objects(data_2D_list)

    print("a =",dic["a"],"+-",dic['da'])
    print("b =",dic['b'],"+-",dic['db'])
    print("chi2 =",dic['chi_squared'])
    print("chi2_reduced =",dic['chi_squared_reduced'])

    plt.figure()
    plt.plot([min(dic['xs']),max(dic['xs'])],[min(dic['xs'])*dic['a']+dic['b'],dic['b']+dic['a']*max(dic['xs'])],'r-',zorder=0)
    plt.errorbar(dic["xs"],dic['ys'],xerr=dic['dxs'],yerr=dic['dys'],ecolor='b',fmt='none',zorder=5)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig("linear_fit.SVG")
    plt.show()

#Bonus - i didn't write the bonus in the most readable way,
# basicly what i've done for the graph of chi2(a) is created two lists
# for x and y axes. the x list is just all a values. and for the y axis
# the list is all the chi2's from a whole iteration for a single b value.
# each b value i reset the list to an empty list. and if in the iteration i got
# a value less than the last one, the the list is saved.
def search_best_parameter(filename):
    filename_string=str(filename)
    file_open=open(filename_string,'r')
    raw_data=file_open.readlines()
    file_open.close()

    data_2D_list=orgazining_data_bonus(raw_data)[0]
    x_axis=orgazining_data(raw_data)[1]
    y_axis=orgazining_data(raw_data)[2]
    a_data=orgazining_data_bonus(raw_data)[3][1:]
    b_data=orgazining_data_bonus(raw_data)[4][1:]
    dic=dictionary_Bonus(data_2D_list)
    if data_check(data_2D_list)!="all good":
        print(data_check(data_2D_list))
        return None
    elif len(data_2D_list)<4 or len(data_2D_list[0])<4:
        print ("Input file error: File doesn't contain enough data points")
        return None
    b=b_data[0]-b_data[2]
    a=a_data[0]-a_data[2]
    ideal_b = b_data[0]
    ideal_a = a_data[0]
    chi2 = 999999999999
    chi2_of_a=[]
    h=0
    ideal_chi2_of_a=[]
    range_a=[]
    if b_data[2]>0:
        while b<b_data[1]:
            h=0
            b=b+b_data[2]
            a=a_data[0]-a_data[2]
            chi2_of_a = []
            if a_data[2]>0:
                while a<a_data[1]:
                    a=a+a_data[2]
                    if a not in range_a:
                        range_a.append(a)
                    chi_squared=0
                    for i in range(0,dic['N']):
                        chi_squared+=((dic['ys'][i]-(a*dic['xs'][i]+b))/dic['dys'][i])**2
                    chi2_of_a.append(chi_squared)
                    if chi_squared<chi2:
                        chi2=chi_squared
                        ideal_a=a
                        ideal_b=b
                        h=1

            else:
                while a > a_data[1]:
                    a = a + a_data[2]
                    if a not in range_a:
                        range_a.append(a)
                    chi_squared = 0
                    for i in range(0, dic['N']):
                        chi_squared += ((dic['ys'][i] - (a * dic['xs'][i] + b)) / dic['dys'][i]) ** 2
                    chi2_of_a.append(chi_squared)
                    if chi_squared < chi2:
                        chi2 = chi_squared
                        ideal_a = a
                        ideal_b = b
                        h=1
            if h==1:
                ideal_chi2_of_a=chi2_of_a
    else:
        while b>b_data[1]:
            h=0
            b=b+b_data[2]
            a=a_data[0]-a_data[2]
            chi2_of_a=[]
            if a_data[2]>0:
                while a<a_data[1]:
                    a=a+a_data[2]
                    if a not in range_a:
                        range_a.append(a)
                    chi_squared=0
                    for i in range(0,dic['N']):
                        chi_squared+=((dic['ys'][i]-(a*dic['xs'][i]+b))/dic['dys'][i])**2
                    chi2_of_a.append(chi_squared)
                    if chi_squared<chi2:
                        chi2=chi_squared
                        ideal_a=a
                        ideal_b=b
                        h=1
            else:
                while a > a_data[1]:
                    a = a + a_data[2]
                    if a not in range_a:
                        range_a.append(a)
                    chi_squared = 0
                    for i in range(0, dic['N']):
                        chi_squared += ((dic[ys][i] - (a * dic[xs][i] + b)) / dic[dys][i]) ** 2
                    chi2_of_a.append(chi_squared)
                    if chi_squared < chi2:
                        chi2 = chi_squared
                        ideal_a = a
                        ideal_b = b
                        h=1
            if h == 1:
                ideal_chi2_of_a = chi2_of_a
    print("a=",ideal_a,"+-",a_data[2])
    print("b=", ideal_b, "+-", b_data[2])
    print("chi2=",chi2)
    print("chi2_reduced",chi2/(dic['N']-2))
    plt.figure(1)
    plt.plot([min(dic['xs']),max(dic['xs'])],[min(dic['xs'])*ideal_a+ideal_b,ideal_b+ideal_a*max(dic['xs'])],'r-',zorder=0)
    plt.errorbar(dic["xs"],dic['ys'],xerr=dic['dxs'],yerr=dic['dys'],ecolor='b',fmt='none',zorder=5)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig("linear_fit.SVG")
    plt.show()
    plt.figure(2)
    plt.plot(range_a,ideal_chi2_of_a)
    plt.xlabel("a")
    plt.ylabel("chi2(a,b={}".format(ideal_b))
    plt.savefig("numeric_sampling.SVG")
    plt.show()
