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


def write_scores(player, score):
	db = sqlite3.connect('snake.sqlite')
	cur = db.cursor()
	cur.execute(f"INSERT INTO SCORES (players, scores) VALUES ('{player}', '{score}')")
	db.commit()
	db.close()
