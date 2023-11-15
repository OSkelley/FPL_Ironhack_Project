from flask import Flask, request, jsonify, abort
import pymysql
import os
import math

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv("MySQL_password"),
    'db': 'comment_toxicity',
    'cursorclass': pymysql.cursors.DictCursor
}

# Database connection function
def get_db_connection():
    return pymysql.connect(**db_config)


@app.route('/')
def homepage():
    return '''
    <html>
    <head>
        <title>Fantasy Premier League API</title>
        <style>
            body { 
                text-align: center; 
                font-family: Arial, sans-serif;
            }
            .container {
                width: 80%;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>This is a football statistic API</h1>
            <p>This API has data from two sources: Fantasy Premier League & FBREF. The data contains a wide variety of player statistics from the Premier League 2017-2023</p>

            <h2>Available Endpoints:</h2>
            <ul style="list-style: none;">
                <li><b>/fbref</b>: Fetch data from FBREF. Can filter by player_id, gameweek, comment length, and date.</li>
                <li><b>/fpl</b>: Fetch data from FPL. Filters similar to Big Query comments.</li>
            </ul>
        </div>
    </body>
    </html>
    '''

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}

@app.route("/players", methods = ['GET'])
def player(player_id):
    db_conn = pymysql.connect(host="localhost",
                              user="root", 
                              password=os.getenv('MySQL_Pass'), 
                              database="fpl_data",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select
                            p.first_name,
                            p.second_name,
                            f.season,
                            p.player_id
                            from fpl_data.player p
                            join fpl_data.fpl f on f.player = p.player_id
                            where p.player_id = %s
        """, (player_id, ))
        player = cursor.fetchone()
        if not player:
            abort(404)
        player = remove_null_fields(player)
        # movie['bechdelTest'] = movie['bechdelScore'] == 3
    
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM fpl_data.fpl f WHERE f.player=%s", (player_id, ))
        fpl = cursor.fetchall()
    player['assists'] = [f['assists'] for f in fpl]
    
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM fpl_data.fbref f WHERE f.player=%s", (player_id, ))
        fbref = cursor.fetchall()
    player['data'] = [remove_null_fields(b) for b in fbref]

    db_conn.close()
    return player


@app.route("/players")
@auth.required
def movies():
    # URL parameters
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = bool(int(request.args.get('include_details', 0)))

    db_conn = pymysql.connect(host="localhost",
                              user="root", 
                              password=os.getenv('MySQL_Pass'), 
                              database="fpl_data",
                              cursorclass=pymysql.cursors.DictCursor)
    # Get the movies
    with db_conn.cursor() as cursor:
        cursor.execute("""
            select
	            p.first_name,
                p.second_name,
                f.season,
                p.player_id
                from fpl_data.player p
                join fpl_data.fpl f on f.player = p.player_id
                order by p.player_id
                limit %s
                offset %s
        """, (page_size, page * page_size))
        players = cursor.fetchall()
        player_ids = [player['player_id'] for player in players]
    
    if include_details:
        # Get fbref
        with db_conn.cursor() as cursor:
            placeholder = ','.join(['%s'] * len(player_ids))
            cursor.execute(f"""SELECT f.*, 
                                FROM fpl_data.fbref f
                                WHERE player_id IN ({placeholder})""",
                        player_ids)
            fbref = cursor.fetchall()
        fbref_dict = defaultdict(list)
        for obj in fbref:
            fbref_dict[obj['player_id']].append(obj['fbref'])
        
        # Get fpl
        with db_conn.cursor() as cursor:
            placeholder = ','.join(['%s'] * len(player_ids))
            cursor.execute(f"""
                SELECT
                    MP.movieId,
                    P.personId,
                    P.primaryName AS name,
                    P.birthYear,
                    P.deathYear,
                    MP.category AS role
                FROM MoviesPeople MP
                JOIN People P on P.personId = MP.personId
                WHERE movieId IN ({placeholder})
            """, movie_ids)
            people = cursor.fetchall()
        people_dict = defaultdict(list)
        for obj in people:
            movieId = obj['movieId']
            del obj['movieId']
            people_dict[movieId].append(obj)

        # Merge genres and people into movies
        for movie in movies:
            movieId = movie['movieId']
            movie['genres'] = genres_dict[movieId]
            movie['people'] = people_dict[movieId]

    # Get the total movies count
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM Movies")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)

    db_conn.close()
    return {
        'movies': movies,
        'next_page': f'/movies?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/movies?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }
