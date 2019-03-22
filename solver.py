def solve_sudoku(A):
    # total_blanks 记录当前数独有多少个需要被填的空
    total_blanks = 0

    # candidates 记录当前某个空的预选值
    candidates = {}

    for i in range(9):
        for j in range(9):
            if A[i, j] is None:
                total_blanks += 1
                candidates[(i, j)] = [_ for _ in range(1, 10)]

    while total_blanks > 0:
        last_total_blanks = total_blanks

        for i in range(9):
            for j in range(9):
                if A[i, j] is not None:
                    # 更新该行其他的预选值
                    for k in range(9):
                        if k != j and A[i, k] == A[i, j]:
                            return None
                        if k != j and A[i, k] is None:
                            try:
                                candidates[(i, k)].remove(A[i, j])

                                if len(candidates[(i, k)]) == 1:
                                    A[i, k] = candidates[(i, k)][0]
                                    total_blanks -= 1
                            except ValueError:
                                pass

                    # 更新该列其他的预选值
                    for k in range(9):
                        if k != i and A[k, j] == A[i, j]:
                            return None
                        if k != i and A[k, j] is None:
                            try:
                                candidates[(k, j)].remove(A[i, j])

                                if len(candidates[(k, j)]) == 1:
                                    A[k, j] = candidates[(k, j)][0]
                                    total_blanks -= 1
                            except ValueError:
                                pass

                    # 剔除该九宫格其他存在的值
                    row = 3 * (i // 3)
                    col = 3 * (j // 3)
                    for m in range(row, row + 3):
                        for n in range(col, col + 3):
                            if m != i and n != j and A[i, j] == A[m, n]:
                                return None
                            if m != i and n != j and A[m, n] is None:
                                try:
                                    candidates[(m, n)].remove(A[i, j])

                                    if len(candidates[(m, n)]) == 1:
                                        A[m, n] = candidates[(m, n)][0]
                                        total_blanks -= 1
                                except ValueError:
                                    pass

        if last_total_blanks == total_blanks:
            min_coord = None
            for i in range(9):
                for j in range(9):
                    if A[i, j] is None:
                        if min_coord is None or len(candidates[i, j]) < len(
                                candidates[min_coord]):
                            min_coord = (i, j)

            for n in candidates[min_coord]:
                A[min_coord] = n
                r = solve_sudoku(A.copy())
                if r is not None:
                    return r
            return None
    return A


if __name__ == '__main__':
    import numpy as np
    # yapf: disable
    A = np.array([
        [6, None, None, 9, 4, None, 3, None, None],
        [4, 5, None, None, None, None, 7, None, None],
        [1, None, None, 8, None, None, 5, None, 4],
        [3, None, 4, None, None, None, 2, 1, None],
        [2, 9, None, None, None, None, None, 3, 7],
        [None, 7, 1, None, None, None, 4, None, 8],
        [9, None, 5, None, None, 2, None, None, 6],
        [7, None, 2, None, None, None, None, 5, 3],
        [None, None, 6, None, 7, 1, None, None, 2]
        ])
    print(solve_sudoku(A))
