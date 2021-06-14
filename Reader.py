import re
import Helper as H

def parse_pgn(pgn:str) -> (dict,str):
    pgn=pgn.split("\n")
    pgn=list(filter(lambda x:x!="",pgn))

    pgn_data={}
    movetext=pgn[-1]

    for p in pgn:
        if len(p)>1 and  p[0]=="[" and p[-1]=="]":
            p=p[1:-1] # remove square braces
            p_split=p.split(" ",maxsplit=1)
            key=p_split[0]
            value=p_split[1][1:-1] # remove quote marks
            pgn_data[key]=value

    return pgn_data,movetext

def parse_san_movetext(movetext:str) -> [(str,dict)]:
    """
    Parse movetext which is in standard-algebric notation
    """
    moves=re.split("\s?\d+\.{1}\s{1}",movetext)
    parsed_moves=[]
    for (i,m) in enumerate(moves[1:]):
        if (i==len(moves)-2): m=re.sub("\d+\-{1}\d+","",m)
        white_black=re.split("\s{1}\d+\.{3}\s{1}",m)

        # analyse white
        white_str,white_dets=parse_san_move(white_black[0].split(" ")[0])
        white_dets.update({"colour":"white","move_num":i})
        parsed_moves+=[(white_str,white_dets)]

        if len(white_black)==2:
            # analyse black
            black_str,black_dets=parse_san_move(white_black[1].split(" ")[0])
            black_dets.update({"colour":"black","move_num":i})
            parsed_moves+=[(black_str,black_dets)]

    return parsed_moves

def parse_san_move(move:str) -> (str,dict):
    move_str=""
    move_dets={}

    if move in H.special_move_dict:
        move_dets["special"]=True
        move_str="performs {}".format(H.special_move_dict[move])
        move_dets["move_name"]=H.special_move_dict[move]

    else:
        move_dets["special"]=False
        piece=H.pieces_dict[move[0]] if move[0] in H.pieces_dict else "pawn"
        move_dets["piece"]=piece

        new_position=re.sub("[KQRBNx+#]","",move)
        move_dets["new_position"]=new_position

        move_str+="moves {} to {}".format(piece,new_position)

        # takes a piece
        if "x" in move:
            move_dets["take"]=True
            move_str+=" and takes a piece"
        else: move_dets["take"]=False

        # places in check
        if "+" in move:
            move_dets["check"]=True
            move_str+=" and places opponent in check"
        else: move_dets["check"]=False

        # places in checkmate
        if "#" in move:
            move_dets["checkmate"]=True
            move_dets["check"]=True
            move_str+=" and places opponent in checkmate"
        else: move_dets["checkmate"]=False

        move_str+="."

    return move_str,move_dets
