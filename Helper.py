"""
    CHESS dot COM
"""
# Dictionary of descriptions for each game result code
game_result_codes={
    "win":"Win",
    "checkmated":"Checkmated",
    "agreed":"Draw agreed",
    "repetition":"Draw by repetition",
    "timeout":"Timeout",
    "resigned":"Resigned",
    "stalemate":"Stalemate",
    "lose":"Lose",
    "insufficient":"Draw by Insufficient material",
    "50move":"Draw by 50-move rule",
    "abandoned":"Abandoned",
    "kingofthehill":"Opponent king reached the hill",
    "threecheck":"Checked for the 3rd time",
    "timevsinsufficient":"Draw by timeout vs insufficient material",
    "bughousepartnerlose":"Bughouse partner lost"
}

"""
    STANDARD ALGEBRAIC NOTATION (SAN)
"""
special_move_dict={
    "O-O":"kingside castling",
    "O-O-O":"queenside castling"
}

pieces_dict={
    "K":"king",
    "Q":"queen",
    "R":"rook",
    "B":"bishop",
    "N":"knight"
}
