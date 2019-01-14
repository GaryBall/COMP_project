import pandas as pd
import numpy as np
from DB_module import *

import mainmenu_module as menu


def main():

    calculate_vote('pB')
    menu.show_project()


def calculate_vote(project_name):
    """
    This function works to calculate the vote results. It could be applied on more than 3 people,
    but the algorithm of 4 or more people is complicated. If you want to understand how this code works,
    please check our report to find the reference.

    @type project_name: string
    @param project_name: the project name to be processed.
    @return:
    """
    data1 = get_if_from_db(project_name)
    if data1 == ():
        return 0

    # change the data to DataFrame to pre-process before calculation
    df = pd.DataFrame(list(data1))
    del df[0]
    vote_matrix = df.values
    # Change integer to float
    vote_matrix = vote_matrix * 1.0
    matrix_len = len(vote_matrix)

    # calculate the situation which only have 3 members
    if matrix_len == 3:
        for i in range(matrix_len):
            for j in range(matrix_len):
                if j == (i+1) % 3:
                    vote_matrix[i, j] = vote_matrix[i][j] * 1.00 / vote_matrix[i, (j+1) % 3]
                    vote_matrix[i, (j+1) % 3] = 1.0 / vote_matrix[i, j]

                elif i == j:
                    vote_matrix[i, j] = 1

        result_list = [0 for _ in range(3)]
        for i in range(len(vote_matrix)):
            result_list[i] = 1.0 / (vote_matrix[i][i] + vote_matrix[(i+1) % 3, i-1]
                                    + vote_matrix[(i+2) % 3, i-2])
        return result_list

    # calculate the situation which have more than 4 members
    elif matrix_len >= 3:

        # the first-level loop to calculate allocation for member 'i'.
        result_list = [0 for _ in range(matrix_len)]
        for i in range(matrix_len):
            # The second-level loop to calculate item1 for different j
            item1 = [0 for _ in range(matrix_len)]
            for j in range(matrix_len):
                if i == j:
                    pass
                else:
                    rho1 = cal_rho(i, j, vote_matrix)
                    tau_1 = [0 for _ in range(matrix_len)]
                    # the 3-level loop to calculate the sum of tau[k]
                    for k in range(matrix_len):
                        if k == i or k == j:
                            tau_1[k] = 0
                            pass
                        else:
                            tau_1[k] = cal_tau(i, j, k, vote_matrix)

                    sigma_tau1 = np.sum(tau_1)
                    item1[j] = 1.0/(1 + rho1 + sigma_tau1)
            sigma_item1 = np.sum(item1)

            # the second-level loop to calculate item2
            item2 = [0 for _ in range(matrix_len)]
            for j in range(matrix_len):
                if j == i:
                    tau_1[k] = 0
                    pass
                else:
                    rho2 = cal_rho(j, i, vote_matrix)
                    tau_2 = [0 for _ in range(matrix_len)]
                    # the 3-level loop to calculate the sum of tau[k]
                    for k in range(matrix_len):
                        if k == i or k == j:
                            tau_1[k] = 0
                            pass
                        else:
                            tau_2[k] = cal_tau(j, i, k, vote_matrix)

                    sigma_tau2 = np.sum(tau_2)
                    item2[j] = 1.0 / (1 + rho2 + sigma_tau2)

            sigma_item2 = np.sum(item2)
            result_list[i] = 1.0*(1 - sigma_item1) / matrix_len \
                             + 1.0 * sigma_item2 / matrix_len
        return result_list


def cal_rho(i, j, matrix):
    """
    Calculate the rho with the index i and j.
    Aggregator 'rho' is the arithmetic means of matrix element with the index ij

    @type i: int
    @param i: index
    @type i: int
    @param j: index
    @type matrix: numpy arranger
    @param matrix: the vote result matrix
    @return:
    """

    sum = 0
    for m in range(len(matrix)):
        if matrix[m, i] == 0 or matrix[m, j] == 0:
            pass
        else:
            sum += 1.0 * matrix[m, i] / matrix[m, j]

    rho = sum / (len(matrix)-2)
    return rho


def cal_tau(i, j, k, matrix):
    """
        Calculate the tau with the index i ,j and k.
        Aggregator 'tau' is the arithmetic means of matrix element with the lower index ik and upper index -j

        @type i, j, k: int
        @param i, j, k: index
        @type matrix: numpy arranger
        @param matrix: the vote result matrix
        @return:
        """
    sum = 0
    for m in range(len(matrix)):
        if matrix[m, k] == 0 or matrix[m, j] == 0:
            pass
        elif m == i:
            pass
        else:
            sum += 1.0 * matrix[m, k] / matrix[m, j]

    tau = sum / (len(matrix)-3)
    return tau


if __name__ == '__main__':
    main()
