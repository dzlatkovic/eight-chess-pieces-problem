notation = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

row = [-1, 0, 1, -1, 1, -1, 0, 1]
col = [-1, -1, -1, 0, 0, 1, 1, 1]


def convert(pos):
    x = pos[0]
    return notation[x] + str(pos[1])


def king_attacks(pos):
    x, y = pos
    attacked_by_k = set()
    for i in range(len(row)):
        if 0 < x + row[i] < 9 and 0 < y + col[i] < 9:
            attacked_by_k.add((x + row[i], y + col[i]))
    return attacked_by_k


def rook_attacks(pos):
    x, y = pos
    attacked_by_rook = set()
    for i in range(1, 9):
        attacked_by_rook.add((x, i))
    for j in range(1, 9):
        attacked_by_rook.add((j, y))
    attacked_by_rook.remove((x, y))
    return attacked_by_rook


def bishop_attacks(pos):
    x, y = pos
    return {(i, j)
            for i in range(1, 9)
            for j in (x + y - i, i - x + y)
            if 0 < j < 9} - {pos}


def queen_attacks(pos):
    d = rook_attacks(pos).union(bishop_attacks(pos))
    return d


def knight_attacks(pos):
    x = pos[0]
    y = pos[1]
    s = set()
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i + j in (-3, -1, 1, 3) and i * j != 0 and 0 < x + i < 9 and 0 < y + j < 9:
                s.add((x + i, y + j))
    return s


def add_piece(position, piece_func, pieces, remaining_squares):
    pieces_updated = pieces.union({position})
    remaining_updated = remaining_squares - piece_func(position) - pieces_updated
    return pieces_updated, remaining_updated


def get_coord(q, r1, r2, b1, b2, n1, n2, k):
    return f"Q{convert(q)} R{convert(r1)} R{convert(r2)} B{convert(b1)} B{convert(b2)} N{convert(n1)} N{convert(n2)} " \
           f"K{convert(k)}"


def sort_coord(coord):
    return " ".join(sorted(coord.split()))


all_squares = {(c, r)
               for c in range(1, 9)
               for r in range(1, 9)}

positions_99 = set()
positions_100 = set()

for queen in [(2, 2), (3, 2), (4, 2), (3, 3), (4, 3), (4, 4)]:
    pieces1 = {queen}
    remaining = all_squares - queen_attacks(queen) - pieces1

    for first_bishop in remaining:
        pieces2, remaining1 = add_piece(first_bishop, bishop_attacks, pieces1, remaining)

        for second_bishop in remaining1:
            if (first_bishop[0] + first_bishop[1]) % 2 == (second_bishop[0] + second_bishop[1]) % 2:
                continue
            else:
                pieces3, remaining2 = add_piece(second_bishop, bishop_attacks, pieces2, remaining1)
                if len(queen_attacks(queen)) + len(bishop_attacks(first_bishop)) + \
                        len(bishop_attacks(second_bishop)) < 49:
                    continue

            for first_rook in remaining2:
                if rook_attacks(first_rook).intersection(pieces3):
                    continue
                else:
                    pieces4, remaining3 = add_piece(first_rook, rook_attacks, pieces3, remaining2)

                for second_rook in remaining3:
                    if rook_attacks(second_rook).intersection(pieces4):
                        continue
                    else:
                        pieces5, remaining4 = add_piece(second_rook, rook_attacks, pieces4, remaining3)

                    for first_knight in remaining4:
                        if knight_attacks(first_knight).intersection(pieces5):
                            continue
                        else:
                            pieces6, remaining5 = add_piece(first_knight, knight_attacks, pieces5, remaining4)

                        for second_knight in remaining5:
                            if knight_attacks(second_knight).intersection(pieces6):
                                continue
                            else:
                                pieces7, remaining6 = add_piece(second_knight, knight_attacks, pieces6, remaining5)

                            for king in remaining6:
                                if king_attacks(king).intersection(pieces7):
                                    continue
                                else:
                                    pieces8, remaining7 = add_piece(king, king_attacks, pieces7, remaining6)

                                score = (len(queen_attacks(queen)) + len(rook_attacks(first_rook)) +
                                         len(rook_attacks(second_rook)) + len(bishop_attacks(first_bishop)) +
                                         len(bishop_attacks(second_bishop)) + len(knight_attacks(first_knight)) +
                                         len(knight_attacks(second_knight)) + len(king_attacks(king)))

                                if score == 99 and len(pieces8) == 8:
                                    positions_99.add(sort_coord(get_coord(queen, first_rook, second_rook, first_bishop,
                                                                          second_bishop, first_knight, second_knight,
                                                                          king)))
                                elif score >= 100:
                                    positions_100.add(sort_coord(get_coord(queen, first_rook, second_rook, first_bishop,
                                                                           second_bishop, first_knight, second_knight,
                                                                           king)))


print("Score 99:")
print(*positions_99, sep="\n")

print("\nScore 100+:")
print(*positions_100, sep="\n")
