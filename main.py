import argparse
import sqlite3

#global variables
DB_PATH = 'note.db'

# TYPE | TEXT

def add():
	str_type = raw_input("Type > ")
	str_text = raw_input("Note > ")
	c.execute("insert into main values (?,?)",(str_type, str_text))

def print_list():
	for row in c.execute("select all type,note from main"):
		print row

def edit():
	print "editzorz"

def delete():
	print "Deleterino"

#initialize the arg parser
parser = argparse.ArgumentParser(description='A simple note keeping program.')
parser.add_argument('cmd', help="[add | edit | view | delete]")
args = parser.parse_args()

#initialize the sqlite database
c = sqlite3.connect(DB_PATH)
c.row_factory = sqlite3.Row
c.execute("create table if not exists main (type,note)")

if args.cmd == 'add':
	add()
elif args.cmd == 'view':
	print_list()
elif args.cmd == 'edit':
	edit()
elif args.cmd == 'delete':
	delete()
else:
	print "Invalid command"
c.commit()
c.close()
exit()
