import sqlite3




def create_db():
	db = sqlite3.connect('snake.sqlite')
	cur = db.cursor()
	cur.execute("""
		create table if not exists SCORES (
		players text,
		scores integer
		)
		""")
	cur.execute("""
		create table if not exists RECENT (
		players text
		)
		""")
	db.close()


def get_best():
	db = sqlite3.connect('snake.sqlite')
	cur = db.cursor()
	cur.execute("""
		SELECT players, scores from SCORES
		ORDER by scores DESC
		LIMIT 5 """)
	
	s = cur.fetchall()
	db.close()
	return s

def get_recent_player():
	db = sqlite3.connect('snake.sqlite')
	cur = db.cursor()
	cur.execute("""
		SELECT players from RECENT
		ORDER by ROWID DESC
		LIMIT 1 """)
	for player in cur.fetchall():
		recent_player = player[0]
		
	db.close()


	
	return recent_player


def write_scores(player, score):
	db = sqlite3.connect('snake.sqlite')
	cur = db.cursor()
	cur.execute(f"INSERT INTO SCORES (players, scores) VALUES ('{player}', '{score}')")
	cur.execute(f"INSERT INTO RECENT (players) VALUES ('{player}')")
	db.commit()
	db.close()
