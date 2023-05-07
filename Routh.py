import sys

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


# A method used to plot the poles of the system.
def plot(roots):
    plt.scatter(roots.real, roots.imag, marker='x')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Poles of TF')
    plt.axhline(y=0, color='black')
    plt.axvline(x=0, color='black')
    plt.show()
    sys.exit()


# A method used to print the Routh table.
def table_print(table, order):
    print("The Routh table is:")
    for row in range(order + 1):
        table[row] = np.round(table[row], decimals=3)
        print('\t\t'.join(map(str, table[row])))

# A method to print when there is a one zero and the reciprocal is not working (palindrome)
def zero_table_print(table , order , index1):
    print("The Routh table is:")
    if (order - (i + 2)) == 1:
        for row in range(order + 1):
            if(row == index1):
                print('a \t\t' , table[index1][1])
            else:
                table[row] = np.round(table[row], decimals=3)
                print('\t\t'.join(map(str, table[row])))

    elif (order - (i + 2)) == 2:
        for row in range(order + 1):
            if(row == index1):
                print('a \t\t' , table[index1][1])
            elif(row == index1+1):
                print('b')
            else:
                table[row] = np.round(table[row], decimals=3)
                print('\t\t'.join(map(str, table[row])))


# A method used to first check the signs of the given coefficients:
# if they are not having the same sign then the system is unstable without going any further.
def initial_sign_check(roots, p_sign_count, order):
    if p_sign_count < order + 1 and p_sign_count != 0:  # Not all are +ve
        polesN = 0
        print('The system is UnStable.')
        print('The RHS poles are: ')
        for i in range(order):
            if roots[i] > 0 and np.abs(np.real(roots[i])) != 0:
                polesN += 1
                print(roots[i])
        print(f'The number of them is: {polesN}')
        return plot(roots)


# A method is used to check when there are roots on the imaginary axis:
# if they aren't repeated then it states that the system is critically stable.
# if they are repeated then the system states that the system is Unstable due to the repeated poles on the imaginary axis.
def critical_check(roots, order):
    count = 0
    critical_count = 0
    critical_roots = []
    for i in range(order):
        if roots[i] < 0 or np.real(roots[i]) == 0:
            count += 1
            if np.real(roots[i]) == 0:
                critical_count += 1
                critical_roots.append(roots[i])

    if count != order:  # the system is already unstable
        polesN = 0
        print('The system is UnStable.')
        print('The RHS poles are: ')
        for i in range(order):
            if roots[i] > 0 and np.abs(np.real(roots[i])) != 0:
                polesN += 1
                print(roots[i])
        print(f'The number of them is: {polesN}')
        return plot(roots)
    else:
        if len(critical_roots) != len(set(critical_roots)):
            print('The system is unstable. (there are repeated critical roots)')
            print('the poles are:')
            print(set(critical_roots))
            print(f'The number of them is:{len(set(critical_roots))}')
            return plot(roots)
        elif count == order and critical_count > 0:
            print('The system is Critically Stable.')
            return plot(roots)


def one_zero_palindrome_check(roots , order , rh_table , index):
    if (order - index) == 1:
        x = sp.Symbol('x')
        expr1 = ((x * rh_table[index - 2][1]) - (rh_table[index - 1][1] * rh_table[index - 2][0])) / x
        limit_expr1 = sp.limit(expr1, x, 0)
        print(f'a = {limit_expr1}')

    elif (order - index) == 2:
        x = sp.Symbol('x')
        expr1 = ((x * rh_table[index-2][1]) - (rh_table[index-1][1] * rh_table[index-2][0])) / x
        limit_expr1 = sp.limit(expr1, x, 0)
        print(f'a = {limit_expr1}')
        if(limit_expr1 == 0):
            expr2 = ((x * rh_table[index-1][1]) - (rh_table[index][1] * 0)) / x
            limit_expr2 = sp.limit(expr2, x, 0)
            print(f'b = {limit_expr2}')
        elif(limit_expr1 == sp.oo):
            y = sp.Symbol('y')
            expr2 = ((y * rh_table[index-1][1]) - (rh_table[index][1] * 0)) / y
            limit_expr2 = sp.limit(expr2, y, sp.oo)
            print(f'b = {limit_expr2}')
        elif(limit_expr1 == -sp.oo):
            y = sp.Symbol('y')
            expr2 = ((y * rh_table[index - 1][1]) - (rh_table[index][1] * 0)) / y
            limit_expr2 = sp.limit(expr2, y, -sp.oo)
            print(f'b = {limit_expr2}')

    count = 0
    for i in range(order):
        if roots[i] < 0 or np.real(roots[i]) == 0:
            count += 1
    if count != order:  # the system is already unstable
        polesN = 0
        print('The system is UnStable.')
        print('The RHS poles are: ')
        for i in range(order):
            if roots[i] > 0 and np.abs(np.real(roots[i])) != 0:
                polesN += 1
                print(roots[i])
        print(f'The number of them is: {polesN}')
        return plot(roots)
    else:
        print('The system is Stable.')
        return plot(roots)

# A method that generates Routh table.
def routh_table(coefficients, order, zeroMethodFlag, FF):
    n = len(coefficients)
    # an array initially consisting of 2 rows
    rh_table = [[], []]
    for i in range(n):
        rh_table[i % 2].append(coefficients[i])

    i = 0
    while True:
        # putting the Zeros
        if len(rh_table[i]) > len(rh_table[i + 1]) and rh_table[i][len(rh_table[i]) - 1] != 0:
            rh_table[i + 1].append(0)
        # removing additional Zeros
        if rh_table[i][len(rh_table[i]) - 1] == 0:
            rh_table[i].pop()
        # Adding the new Rows
        if len(rh_table[i]) > 1:
            rh_table.append([])
        # Zero exists
        if rh_table[i + 1][0] == 0:
            All_zeros = True

            for x in range(len(rh_table[i + 1]) - 1):
                if rh_table[i + 1][x] != 0:
                    All_zeros = False

            # all row is zeros and not palindrome or one zero and not palindrome => use reciprocal roots
            if (zeroMethodFlag == False and All_zeros and ((order - (i + 1)) != 1)) or (
                    rh_table[i + 1][0] == 0 and All_zeros == False and ((order - (i + 1)) != 1) and zeroMethodFlag == False):
                zeroMethodFlag = True
                coefficients.reverse()
                return routh_table(coefficients, order, zeroMethodFlag, FF)

            # all row is zeros and palindrome
            elif All_zeros and ((order - (i + 1)) != 1):  # not s^1
                power = order - i  # order eli for order abo zeros
                for j in range(len(rh_table[i + 1]) - 1):  # <
                    rh_table[i + 1][j] = rh_table[i][j] * power
                    power -= 2

            # one zero and palindrome
            elif All_zeros == False and ((order - (i + 1)) != 1):  # not s^1
                FF = False
                if ((order - (i + 2)) == 1):        # 1 unknown 1 row
                    rh_table[i + 1].pop()
                    if len(rh_table[i + 1]) > 1:
                        rh_table.append([])
                    rh_table[i + 2].append('a')
                    rh_table[i + 3].append(rh_table[i][len(rh_table[i]) - 1])
                    zero_table_print(rh_table, order, i + 2)
                    one_zero_palindrome_check(roots, order, rh_table, i + 2)
                elif ((order - (i + 2)) == 2):  # 2 unknown 2 rows
                    rh_table[i + 1].pop()
                    if len(rh_table[i + 1]) > 1:
                        rh_table.append([])
                        rh_table.append([])
                    rh_table[i + 2].append('a')
                    rh_table[i + 2].append(rh_table[i][len(rh_table[i]) - 1])
                    rh_table[i + 3].append('b')
                    rh_table[i + 4].append(rh_table[i][len(rh_table[i]) - 1])
                    zero_table_print(rh_table, order, i + 2)
                    one_zero_palindrome_check(roots, order, rh_table, i + 2)


                # rh_table[i + 1].pop()
                # if len(rh_table[i+1]) > 1:
                #     rh_table.append([])
                #     rh_table.append([])
                # rh_table[i + 2].append('a')
                # rh_table[i + 2].append(rh_table[i][len(rh_table[i]) - 1])
                # rh_table[i + 3].append('b')
                # rh_table[i + 4].append(rh_table[i][len(rh_table[i]) - 1])
                # zero_table_print(rh_table, order , i+2)
                # one_zero_palindrome_check(roots , order , rh_table , i+2)

            elif (order - (i + 1)) == 1:  # critical stable s^1
                FF = False
                rh_table[i + 1].pop()
                rh_table[i + 2].append(rh_table[i][len(rh_table[i]) - 1])
                table_print(rh_table, order)
                critical_check(roots, order)

        if (len(rh_table[i]) > 1) and FF:
            for j in range(len(rh_table[i]) - 1):
                rh_table[i + 2].append(
                    (rh_table[i + 1][0] * rh_table[i][j + 1] - rh_table[i][0] * rh_table[i + 1][j + 1]) /
                    rh_table[i + 1][0])
        elif len(rh_table[i]) == 1:
            break
        i += 1

    table_print(rh_table, order)
    return rh_table


# A method to check that the stability (the starter method)
def stability_check(coefficients, order, roots):
    stabilityFlag = True
    zeroMethodFlag = False
    FF = True
    table = routh_table(coefficients, order, zeroMethodFlag, FF)

    for i in range(order):
        if roots[i] > 0:
            stabilityFlag = False
    if stabilityFlag == True:
        print('The system is Stable.')
        return plot(roots)
    else:
        polesN = 0
        print('The system is UnStable.')
        print('The RHS poles are: ')
        for i in range(order):
            if roots[i] > 0 and np.abs(np.real(roots[i])) != 0:
                polesN += 1
                print(roots[i])
        print(f'The number of them is: {polesN}')
        return plot(roots)


#####################################################################
order = int(input('Enter the order of the characteristic equation:'))
coeff = []
p_sign_count = 0
for i in range(order + 1):
    c = int(input(f'Enter coeff of s^{order - i}: '))
    coeff.append(c)
    if c > 0:
        p_sign_count += 1

roots = np.roots(coeff)
roots = np.round(roots, decimals=6)

initial_sign_check(roots, p_sign_count, order)
stability_check(coeff, order, roots)
