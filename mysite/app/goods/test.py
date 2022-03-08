from app.goods.itemcf import rec
a={'ID':rec(2)}
print(a)
res=[]
for i in range(4):
    res.append(a.get('ID')[i])
print(res[2])