def answer(m):
    import fractions
    from fractions import Fraction

    def lcm(a, b):
        lcm_int = a * b // fractions.gcd(a, b)
        return lcm_int

    def order_matrix(m, terminal_states):
        """Puts all terminal states at bottom of matrix. Returns matrix and dict of swaps from->to i.e {2:3, 3:2, 1:1,...etc"""
        swaps = dict()
        ordered_m = []
        for i, val in enumerate(m):
            if i not in terminal_states:
                ordered_m.append(m[i])
                if not i == ordered_m.index(m[i]):
                    swaps[i] = ordered_m.index(m[i])
        for i, val in enumerate(m):
            if i in terminal_states:
                ordered_m.append(m[i])
        return (ordered_m, swaps)

    def find_terminals(m):
        terminal_states = []
        for i, row in enumerate(m):
            if sum(row) == 0:
                terminal_states.append(i)
        return terminal_states

    def build_qr(m, terminal_states):
        q_matrix = [[] for n in range(len(m[0]) - len(terminal_states))]
        r_matrix = [[] for n in range(len(m[0]) - len(terminal_states))]
        index = 0
        for i, row in enumerate(m):
            for j, val in enumerate(row):
                if i not in terminal_states and j not in terminal_states:
                    q_matrix[index].append(Fraction(val, sum(row)))
                elif i not in terminal_states:
                    r_matrix[index].append(Fraction(val, sum(row)))
            if i not in terminal_states:
                index += 1

        return q_matrix, r_matrix

    def fill_i_matrix(m):
        """Makes and fills square identity matrix of size m x m"""
        i_matrix = []
        for i in range(0, m):
            i_matrix.append([])
            for j in range(0, m):
                if i == j:
                    i_matrix[i].append(1)
                else:
                    i_matrix[i].append(0)
        return i_matrix

    def sub_matrices(m1, m2):
        """Subtract matrix m2 from matrix m1 and returns matrix m3"""
        m3 = [[] for n in range(len(m1))]
        for i, row in enumerate(m1):
            for j, val in enumerate(m1):
                m3[i].append(m1[i][j] - m2[i][j])
        return m3

    def mult_matrices(m1, m2):
        """Multiply matrix m1 by matrix m2 and return matrix m3.
           Throws error if multiplication not possible."""
        m3 = [[0 for n in range(len(m2[0]))] for i in
              range(len(m1))]  # len(m3) to match len m1
        # assert len(m1[0]) == len(m2)  # Change to if statement if faulty
        for i in range(len(m1)):  # row in m1
            for n in range(len(m2[0])):  # col in m2
                for j in range(len(m1[0])):  # col in m1
                    m3[i][n] += (m1[i][j] * m2[j][n])
        return m3

    def inverse_matrix(m):
        """Finds and returns inverse of matrix"""
        inverse = [[0 for n in range(0, 2 * len(m))] for n in range(0, len(m))]
        for i in range(0, len(m)):
            for j in range(0, len(m)):
                inverse[i][j] = m[i][j]
        for i in range(0, len(m)):
            for j in range(len(m), 2 * len(m)):
                if i == j - len(m):
                    inverse[i][j] = 1
                else:
                    inverse[i][j] = 0
        for i in range(0, len(m)):
            for j in range(0, len(m)):
                if not i == j:
                    proportion_flt = Fraction(inverse[j][i], inverse[i][i])
                    for k in range(0, 2 * len(m)):
                        inverse[j][k] -= proportion_flt * inverse[i][k]

        for i in range(0, len(m)):
            a = inverse[i][i]
            for j in range(0, 2 * len(m)):
                inverse[i][j] /= a
        for i in range(0, len(m)):
            for j in range(0, len(m)):
                del inverse[i][0]

        return inverse

    if m == [[0]]:
        return [1,1]

    terminal_states = find_terminals(m)
    q_matrix = build_qr(m, terminal_states)[0]
    r_matrix = build_qr(m, terminal_states)[1]
    inverse = inverse_matrix(
        sub_matrices(fill_i_matrix(len(q_matrix)), q_matrix))
    b_matrix = mult_matrices(inverse, r_matrix)
    lcm_int = 1
    if len(b_matrix) >= 1:
        for j in b_matrix[0]:
            lcm_int = lcm(lcm_int, j.denominator)
    else:
        for j in b_matrix:
            lcm_int = lcm(lcm_int, j.denominator)

    answer_matrix = []
    if len(b_matrix) >= 1:
        for j in b_matrix[0]:
            answer_matrix.append(j.numerator * (lcm_int // j.denominator))
        answer_matrix.append(lcm_int)
    else:
        for j in b_matrix:
            answer_matrix.append(j.numerator * (lcm_int // j.denominator))
        answer_matrix.append(lcm_int)
    return answer_matrix


# print(answer([
#     [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
#     [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
#     [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
#     [0, 0, 0, 0, 0, 0],  # s3 is terminal
#     [0, 0, 0, 0, 0, 0],  # s4 is terminal
#     [0, 0, 0, 0, 0, 0],  # s5 is terminal
# ]))
# print(answer([[0, 2, 1, 0, 0],
#               [0, 0, 0, 3, 4],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0]]))

# print(answer([[0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
# print(answer([[0, 2, 1, 1, 1],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0]]))
# print(answer([[0, 2, 1, 1, 1],
#               [0, 0, 0, 0, 0],
#               [0, 0, 1, 1, 0],
#               [0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0]]))
print(answer([[0]]))