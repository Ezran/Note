import argparse
import sqlite3

#global variables
DB_PATH = 'note.db'

def add(args):
	c.execute("insert into main values (?,?)",(args.t or "", args.m))

def print_list(args):
	print
	print "Tag         Note"
	print "----------  ------------"    

	if not args.a:
		for row in c.execute("select all type,note from main where type=(?)",(args.t,)):
			print row[0].ljust(11), row[1].ljust(11)
	else:	
		for row in c.execute("select all type,note from main"):
			print row[0].ljust(11), row[1].ljust(11)
	print 

def delete(args):
	print "Deleterino"

#initialize the arg parser
parser = argparse.ArgumentParser(description='A simple note keeping program.')
subparsers = parser.add_subparsers(help='Sub-command help')

add_parser = subparsers.add_parser('add',help='Add a note')
add_parser.add_argument('-t',help='Include note tag')
add_parser.add_argument('-m',help='Note text',required=True)
add_parser.set_defaults(func=add)

view_parser = subparsers.add_parser('view',help='View notes')
view_group = view_parser.add_mutually_exclusive_group(required=True)
view_group.add_argument('-a',help='Show all notes',action='store_true')
view_group.add_argument('-t',help='Show tagged notes (blank for untagged notes)', const="", nargs='?')
view_parser.set_defaults(func=print_list)

del_parser = subparsers.add_parser('delete',help='Delete a note')
del_group = del_parser.add_mutually_exclusive_group()
del_group.add_argument('--purge',help='Delete all existing notes',action='store_true')
del_group.add_argument('--id',help='ID of the note to be deleted')
del_parser.set_defaults(func=delete)
args = parser.parse_args()

#initialize the sqlite database
c = sqlite3.connect(DB_PATH)
c.row_factory = sqlite3.Row
c.execute("create table if not exists main (type,note)")

#run appropriate function
args.func(args) 

#close the database and exit
c.commit()
c.close()
exit()
