from copy import deepcopy
import sys
from sympy import symbols, Eq, solve

def addBuf(buf,a,mas_x,cykl):
    buf.append(["Базис","B"]+[f"X{n+1}" for n in range(len(a[0])-1)])
    for i in range(len(a)-1):
        if mas_x[i]==-1:buf.append([f"X{len(a)+i+1}"]+[round(g,1) for g in a[i]])
        else:buf.append([f"X{mas_x[i]+1}"]+[round(g,1) for g in a[i]])
    buf.append([f"F(X{cykl})"]+[round(g,1) for g in a[len(a)-1]])
    buf.append(["========"]*(len(a[0])+1))
    cykl+=1
    
def simplex_metod(mas):
    buf=[]
    _c,a,b=mas[0],mas[1],[[i] for i in mas[2]]
    size=len(_c)
    for i in range(len(a)): a[i].extend([1 if j == i else 0 for j in range(len(a))])
    mas_x,c=[-1]*len(b),[0]
    c.extend([-x for x in _c])
    c.extend([0 for i in range(len(a))])
    for i in range(len(a)):b[i].extend(a[i])
    a=b
    a.append(c)
    cykl=1
    addBuf(buf,a,mas_x,cykl)
    while(any(e < 0 for e in a[len(a)-1][1:len(a[0])])):
        y = a[len(a)-1].index(min([a[len(a)-1][i] if a[len(a)-1][i]!=0 else float('inf') for i in range(1,len(a))]))
        d=[a[i][0]/a[i][y] if a[i][y]!=0 else float('inf')  for i in range(len(a)-1)]
        x=d.index(min(d, key=abs))
        mas_x[x]=y-1
        ota=[[a[j][y]*a[x][i]/a[x][y] if j!=x else str(a[x][y]) for i in range(len(a[0]))] for j in range(len(a))]
        a=[[a[j][i]-ota[j][i] if not isinstance(ota[j][i],str) else a[j][i]/float(ota[j][i]) for i in range(len(a[0]))] for j in range(len(a))]    
        cykl+=1
        addBuf(buf,a,mas_x,cykl)    
    return ["1",[[a[mas_x.index(i)][0] if i in mas_x else 0 for i in range(size)],a[len(a)-1][0]],buf]
def solve_linear_system(stroka, xmas):
    coefficients=[[stroka[1][j][i] for j in range(len(stroka[1]))] for i in range(len(stroka[1][0]))]
    constants = deepcopy(stroka[0])
    for i in range(len(xmas[0])-1,-1,-1):
        if xmas[0][i]==0:
            coefficients.pop(i)
            constants.pop(i)
    res = [sum([stroka[1][i][j] * xmas[0][j] for j in range(len(xmas[0]))]) - stroka[2][i] for i in range(len(stroka[2]))]
    for i in range(len(res)):
        if res[i] != 0:
            coefficients.append([0 if i!=j else 1 for j in range(len(res))])
            constants.append(0)
    variables = symbols(' '.join(f'x{i}' for i in range(1, len(coefficients[0]) + 1)))
    equations = [Eq(sum(c * v for c, v in zip(coeff_row, variables)), constant) for coeff_row, constant in zip(coefficients, constants)]
    return solve(equations, variables)

def shadow(mas):
    var_a=solve_linear_system(mas[0],simplex_metod(deepcopy(mas[0]))[1])
    m=deepcopy([mas[0][0]]+[[[round(i*(1+mas[1][1]/100),2) for i in x] for x in mas[0][1]]]+[mas[0][2]])
    var_b=solve_linear_system(m,simplex_metod(deepcopy(m))[1])
    return ["3",[[[round(var_a[i],3) for i in var_a.keys()],[simplex_metod(deepcopy(mas[0]))[1]]],[[sum([var_b[i]-var_a[i] for i in var_a.keys()])],[simplex_metod(deepcopy(m))[1]]],[simplex_metod([[i*(1+mas[1][2]/100) for i in mas[0][0]]]+mas[0][1:])[1]]]]
   
s=['3', [[[3.0, 4.0, 3.0, 1.0], [[7.0, 2.0, 2.0, 6.0], [5.0, 8.0, 4.0, 3.0], [2.0, 4.0, 1.0, 8.0]], [80.0, 480.0, 130.0]], [5.0, -99.0, 5.0]]]

for row in shadow(s[1]):
    print(row)