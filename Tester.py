"""
    Test Parser.py
"""

import Parser as P

movetext="1. e4 {[%clk 0:05:00]} 1... e6 {[%clk 0:04:56.3]} 2. d4 {[%clk 0:04:59.1]} 2... d5 {[%clk 0:04:54.9]} 3. e5 {[%clk 0:04:58]} 3... Nc6 {[%clk 0:04:51.4]}"
target_moves_text=["e4 {[%clk 0:05:00]}","e6 {[%clk 0:04:56.3]}","d4 {[%clk 0:04:59.1]}","d5 {[%clk 0:04:54.9]}","e5 {[%clk 0:04:58]}","Nc6 {[%clk 0:04:51.4]}"]

# extract from raw movetext
assert P.extract_moves_from_movetext(movetext)==target_moves_text

# special moves
assert P.special_move("e4")==None
assert P.special_move("O-O")=="kingside castling"
assert P.special_move("O-O-O")=="queenside castling"
assert P.special_move("O")==None

# piece type
assert P.identify_piece("e4")=="pawn"
assert P.identify_piece("a3")=="pawn"
assert P.identify_piece("Ke4")=="king"
assert P.identify_piece("Qe4")=="queen"
assert P.identify_piece("Re4")=="rook"
assert P.identify_piece("Be4")=="bishop"
assert P.identify_piece("Ne4")=="knight"

# takes
assert P.take("xe4")
assert P.take("dxe4")
assert P.take("Kxe4")
assert P.take("Nbxe4")
assert P.take("e4")==False

# checks
assert P.check("e4+")
assert P.check("e4#")
assert P.check("e4")==False

# checkmates
assert P.checkmate("e4+")==False
assert P.checkmate("e4#")
assert P.checkmate("e4")==False

# promotions
assert P.promotion("g4=Q")
assert P.promotion("g4")==None

# ambiguity
assert P.ambiguity("dxe4")=="d"
assert P.ambiguity("e4")==None
assert P.ambiguity("e4")==None
assert P.ambiguity("Nbxe4")=="b"
assert P.ambiguity("Nbe4")=="b"

# end position
assert P.end_position("Nbe4#")=="e4"
assert P.end_position("Nbe4+")=="e4"
assert P.end_position("Nbe4")=="e4"
assert P.end_position("Ne4+")=="e4"
assert P.end_position("e4")=="e4"
assert P.end_position("Ne4")=="e4"

# move details dictionary
assert isinstance(P.parse_move_text("e4"),dict)

returned_dict_pawn=P.parse_move_text("e4") # simple pawn move
assert returned_dict_pawn["piece"]=="pawn"
assert returned_dict_pawn["end_position"]=="e4"
assert returned_dict_pawn["check"]==False
assert returned_dict_pawn["checkmate"]==False
assert returned_dict_pawn["take"]==False
assert returned_dict_pawn["promotion"]==False
assert returned_dict_pawn["promoted_to"]==None
assert returned_dict_pawn["ambiguity"]==None

returned_dict_queen_check=P.parse_move_text("Qxc7+")
assert returned_dict_queen_check["piece"]=="queen"
assert returned_dict_queen_check["end_position"]=="c7"
assert returned_dict_queen_check["check"]==True
assert returned_dict_queen_check["checkmate"]==False
assert returned_dict_queen_check["take"]==True
assert returned_dict_queen_check["promotion"]==False
assert returned_dict_queen_check["promoted_to"]==None
assert returned_dict_queen_check["ambiguity"]==None

returned_dict_ambiguous=P.parse_move_text("dxe4")
assert returned_dict_ambiguous["piece"]=="pawn"
assert returned_dict_ambiguous["end_position"]=="e4"
assert returned_dict_ambiguous["check"]==False
assert returned_dict_ambiguous["checkmate"]==False
assert returned_dict_ambiguous["take"]==True
assert returned_dict_ambiguous["promotion"]==False
assert returned_dict_ambiguous["promoted_to"]==None
assert returned_dict_ambiguous["ambiguity"]=="d"

returned_dict_promotion=P.parse_move_text("bxa1=Q+")
assert returned_dict_promotion["piece"]=="pawn"
assert returned_dict_promotion["end_position"]=="a1"
assert returned_dict_promotion["check"]==True
assert returned_dict_promotion["checkmate"]==False
assert returned_dict_promotion["take"]==True
assert returned_dict_promotion["promotion"]==True
assert returned_dict_promotion["promoted_to"]=="queen"
assert returned_dict_promotion["ambiguity"]=="b"
