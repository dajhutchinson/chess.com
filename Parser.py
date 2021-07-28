"""
    Parse PGN movedata
"""

import re
import Helper as H

"""
    PARSE RAW DATA
"""
def extract_moves_from_movetext(movetext:str) -> [str]:
    """
    DESCRIPTION
    extracts text for each move from raw PGN movedata text.
    return a list of text for each move

    PARAMETERS
    movetext (str) - raw PGN movedata (full string returned by Reader.parse_pgn)

    RETURNS
    [str] - text for each move, in order
    """
    # find all moves by white
    white_moves_text=re.findall("(?<=\d\.{1}\s).*?(?=\})",movetext)
    white_moves_text=[x+"}" for x in white_moves_text]

    # find all moves by black
    black_moves_text=re.findall("(?<=\d\.{3}\s).*?(?=\})",movetext)
    black_moves_text=[x+"}" for x in black_moves_text]

    # zip moves to be in order
    moves_text=[v for x in zip(white_moves_text,black_moves_text) for v in x]
    if len(white_moves_text)>len(black_moves_text): moves_text+=[white_moves_text[-1]]

    return moves_text

"""
    PARSE PGN MOVE
"""

def special_move(text:str) -> str:
    """
    DESCIPTION
    determine whether this move was a special moves (i.e. a castling)

    PARAMETERS
    text (str) - PGN move

    RETURN
    str - name of move (or None if not a special move)
    """
    if text in H.special_move_dict: return H.special_move_dict[text]
    else: return None

def identify_piece(text:str) -> str:
    """
    DESCIPTION
    identify piece which has been moved

    PARAMETERS
    text (str) - PGN move

    RETURN
    str - long form name of piece (e.g. "pawn","rook",...)
    """
    if text[0] in H.pieces_dict: return H.pieces_dict[text[0]]
    return "pawn"

def take(text:str) -> bool:
    """
    DESCRIPTION
    return whether a piece was taken this move.

    PARAMETERS
    text (str) - PGN move

    RETURN
    bool - whether a piece was taken this moves

    NOTE
    does not make any consideration for which piece was taken
    """
    return "x" in text

def check(text:str) -> bool:
    """
    DESCRIPTION
    returns whether a check has occurred

    PARAMETERS
    text (str) - PGN move

    RETURN
    bool - whether this move resulted in a check
    """
    return ("+" in text) or ("#" in text)

def checkmate(text:str) -> bool:
    """
    DESCRIPTION
    returns whether a checkmate has occurred

    PARAMETERS
    text (str) - PGN move

    RETURN
    bool - whether this move resulted in a checkmate
    """
    return "#" in text

def promotion(text:str) -> bool:
    """
    DESCRIPTION
    identify whether a pawn was promoted and, if so, to what piece

    PARAMETERS
    text (str) - PGN move

    RETURN
    bool - whether this move resulted in a checkmate
    """

    if "=" not in text: return None
    else:
        promotion_c=re.findall("(?<=\=).+?",text)[0]
        return H.pieces_dict[promotion_c]

def ambiguity(text) -> str:
    """
    DESCRIPTION
    extract extra info when two pieces of the same type can move to the same position (pawn ambiguity impossible)

    PARAMETERS
    text (str) - PGN move

    RETURN
    str - details of the ambiguity (either initial rank or file of piece which is moved) (`None` if no ambiguity)
    """
    piece_type=identify_piece(text)
    if (piece_type=="pawn") and ("x" in text):
        occurences=re.findall(".{3}(?=\d)",text)
        if len(occurences)==0: return None
        else: return occurences[0][0]
    elif ("x" in text): # take has occurred
        occurences=re.findall(".{4}(?=\d)",text)
        if len(occurences)==0: return None
        else: return occurences[0][1]
    else:
        occurences=re.findall(".{3}(?=\d)",text)
        if len(occurences)==0: return None
        else: return occurences[0][1]

def end_position(text) -> str:
    """
    DESCRIPTION
    identify location of piece at end of move

    PARAMETERS
    text (str) - PGN move

    RETURN
    str - the board position the move ends on
    """
    for c in ["+","#"]: # remove special end notation
        text=text.replace(c,"")
    if "=" in text: # remove promotion text
        text=re.findall(".+?(?=\=[QRBN])",text)[0]
    return text[-2:]

def parse_move_text(text) -> dict:
    """
    DESCRIPTION
    parse details about move to dictionary

    PARAMETERS
    text (str) - PGN move

    RETURN
    dict - details move (what piece, end position, etc.)
    """
    details={}
    details["piece"]=identify_piece(text)
    details["end_position"]=end_position(text)
    details["check"]=check(text)
    details["checkmate"]=checkmate(text)
    details["take"]=take(text)

    p_dets=promotion(text)
    details["promotion"]= False if (not p_dets) else True
    details["promoted_to"]=p_dets

    details["ambiguity"]=ambiguity(text)

    if (details["piece"]=="pawn") and (details["take"]==True): details["ambiguity"]=text[0]
    return details
