import sys

import numpy as np
import matplotlib.pyplot as plt


def plot(roots):
    plt.scatter(roots.real, roots.imag, marker='x')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Poles of TF')
    plt.axhline(y=0, color='black')
    plt.axvline(x=0, color='black')
    plt.show()
    sys.exit()


def table_print(table, order):
    print("The Routh table is:")
    for row in range(order + 1):
        table[row] = np.round(table[row], decimals=3)
        print('\t\t'.join(map(str, table[row])))


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


def critical_check(roots , order):
    count = 0
    critcal_count = 0
    critical_roots = []
    for i in range(order):
        if roots[i] < 0 or np.real(roots[i]) == 0:
            count += 1
            if np.real(roots[i]) == 0:
                critcal_count += 1
                critical_roots.append(roots[i])

    if count != order:                  # the system is already unstable
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
        elif count == order and critcal_count > 0:
            print('The system is Critically Stable.')
            return plot(roots)


def routh_table(coefficients, order, zeroMethodFlag, FF):
    n = len(coefficients)
    #	an array initially consisting of 2 rows
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
        # print(f"order-i {order - i}")
        # print(f"order-(i+1) {order - (i+1)}")
        # print(rh_table)
        # print("fasl 1")
        if rh_table[i + 1][0] == 0:
            # print("awl")
            Flag = True
            for x in range(len(rh_table[i+1]) - 1):
                # print("kam mra")
                if rh_table[i+1][x] != 0:
                    Flag = False

            if (zeroMethodFlag == False and Flag and ((order - (i + 1)) != 1)) or (rh_table[i+1][0] == 0 and Flag == False and ((order - (i + 1)) != 1)):
                # print("a5irn 1")
                zeroMethodFlag = True
                coefficients.reverse()
                return routh_table(coefficients, order, zeroMethodFlag, FF)
            elif Flag and ((order - (i + 1)) != 1):  # not s^1
                # print("a5irn 2")
                power = order - i  # order eli for order abo zeros
                for j in range(len(rh_table[i + 1])-1):  # <
                    rh_table[i + 1][j] = rh_table[i][j] * power
                    power -= 2
            elif (order - (i + 1)) == 1:  # critical stable s^1
                FF = False
                rh_table[i+1].pop()
                rh_table[i + 2].append(rh_table[i][len(rh_table[i]) - 1])
                table_print(rh_table, order)
                critical_check(roots , order)

            # coefficients = [a + b for a, b in zip(coefficients + [0], [0] + coefficients)]
        # print(rh_table)
        if (len(rh_table[i]) > 1) and FF:
            for j in range(len(rh_table[i]) - 1):
                    rh_table[i + 2].append(
                      (rh_table[i + 1][0] * rh_table[i][j + 1] - rh_table[i][0] * rh_table[i + 1][j + 1]) / rh_table[i + 1][0])
        elif len(rh_table[i]) == 1:
            break
        i += 1

    table_print(rh_table, order)
    return rh_table


# def critical_routh_table(coefficients):

def stability_check(coefficients, order, roots):
    stabilityFlag = True
    zeroMethodFlag = False
    FF = True
    table = routh_table(coefficients, order, zeroMethodFlag, FF)
    # check sign
    # for i in range(len(table) - 1):
    #     if table[i][0] * table[i + 1][0] < 0:
    #         flag = 1
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
# plot(roots)
# print(roots)
initial_sign_check(roots, p_sign_count, order)
# critical_check(roots, order, coeff)
stability_check(coeff, order, roots)
