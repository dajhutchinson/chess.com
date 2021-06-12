import requests, re, json
import pandas as pd

"""
    API CALLS
"""

def fetch_user_profile(username:str) -> pd.Series:
    """
    DESCRIPTION
    fetch details of a user profile inc. id, name, follower count, country, last_online, join date
    """
    url="https://api.chess.com/pub/player/{}".format(username)
    return __request_parse_series(url)

def fetch_user_clubs(username:str) -> pd.DataFrame:
    url="https://api.chess.com/pub/player/{}/clubs".format(username)
    data=__request(url)
    data=data["clubs"]
    df=pd.DataFrame(data)
    return df

def fetch_user_overview_stats(username:str) -> pd.Series:
    """
    DESCRIPTION
    fetch overview of user's stats inc. last, best and overal record for each game category (rapdi, blitz etc.)
    """
    url="https://api.chess.com/pub/player/{}/stats".format(username)
    return __request_parse_series(url)

def fetch_every_game(username:str,printing=False) -> [pd.DataFrame]:
    """
    DESCRIPTION
    fetch details on every game by a user inc. url, pgn (portable game standard), time limit, FE notation etc.
    """
    url="https://api.chess.com/pub/player/{}/games/archives".format(username)
    archives=__request(url)["archives"]
    games=None
    for (i,archive_url) in enumerate(archives):
        if printing: print("{}/{}".format(i+1,len(archives)),end="\r")

        r=requests.get(archive_url)
        if (r.status_code==200):
            data=json.loads(r.text)["games"]
            new_games=pd.DataFrame(data)

        if (i==0): games=new_games
        else: games=games.append(new_games)
    if printing: print(" "*100,end="\r")

    games=games.reset_index().drop(columns=["index"])

    return games

"""
    REQUEST METHODS
"""
def __request(url):
    r=requests.get(url)
    status=r.status_code
    if (status==200):
        data=json.loads(r.text)
        return data
    else:
        print("ERROR status {}".format(status))
        return False

def __request_parse_series(url) -> pd.Series:
    """
    DESCRIPTION
    make a request to `url` and parse returned data into a pandas DataFrame.

    RETURNS
    df - parsed data as df
    OR
    int - `status_code` if request fails (301,304,404,410,429)
    """
    data=__request(url)
    if (data): return pd.Series(data)
    else: return False

def __request_parse_df(url) -> pd.DataFrame:
    """
    DESCRIPTION
    make a request to `url` and parse returned data into a pandas DataFrame.

    RETURNS
    df - parsed data as df
    OR
    int - `status_code` if request fails (301,304,404,410,429)
    """
    data=__request(url)
    if (data): return pd.DataFrame(data)
    else: return False


"""
    FILE METHODS
"""
def __write_to_csv(df:pd.DataFrame,filename:str) -> str:
    df.to_csv(filename)
    return filename

def __read_csv(filename:str) -> pd.DataFrame:
    return pd.read_csv(filename,index_col=0)
