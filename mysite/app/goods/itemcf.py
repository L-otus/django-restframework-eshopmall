import numpy as np
import xlrd
from mysite import settings


def cos_sim(a, b):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    cos = np.dot(a,b)/(a_norm * b_norm)
    return cos

def get_sim(dim,m1,m2):
    sim=np.zeros((dim,dim))
    #print(np.shape(sim))
    #print(m2[1])
    for i in range(dim):
        for j in range(dim):
            if i==j:
                sim[i][j]=0
            else:
                sim[i][j]=cos_sim(m1[i],m2[j])
    return sim

def get_simdish(order,sim,dish_ls):
    recomend_num=np.argsort(-sim[order-1])
    #print(recomend_num+1)
    #print(dish_ls[order])
    sim_num=[]
    sim_dish=[]
    for i in range(10):
        sim_num.append((recomend_num[i]))
    for i in range(10):
        sim_dish.append(dish_ls[sim_num[i]])

    return recomend_num+1

def rec(dish_id):
    label_path='{0}{1}'.format(settings.STATIC_ROOT,'excel/菜品标签.xls')
    print(label_path)
    dish_label=xlrd.open_workbook(label_path)
    sheet=dish_label.sheets()
    dish=[]
    num=sheet[0].nrows
    col=sheet[0].ncols
    for i in range(1,num):
        dish.append(sheet[0].cell_value(i,0))
    label_all=np.zeros((num-1,col-1))
    label=sheet[0].cell_value(0,1)
    for i in range(1,num):
        for j in range(1,col):
            label_all[i-1][j-1]=int(sheet[0].cell_value(i,j))
    sim=get_sim(35,label_all,label_all)
    #print(sim)
    return get_simdish(dish_id,sim,dish)

if __name__ == '__main__':
    rec(3)