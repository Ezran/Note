import argparse
import sqlite3
from os.path import expanduser

#global variables
DB_PATH = expanduser('~') + '/.note.db' #won't work with windows

def add(args):
	c.execute("insert into main values (?,?)",(args.t or "", args.m))

def print_list(args):
	print
	id_opt = ""
	if args.id:
		id_opt = "oid,"
		print "ID   Tag         Note"
		print "---  ----------  ------------"    
	else:
		print "Tag         Note"
		print "----------  ------------"    

	if not args.all:
		for row in c.execute("select all " + id_opt + "type,note from main where type=(?)",(args.t,)):
			if not args.id:
				print row[0].ljust(11), row[1].ljust(11)
			else:
				print str(row[0]).ljust(4), row[1].ljust(11), row[2].ljust(11)
	else:	
		for row in c.execute("select all " + id_opt + "type,note from main"):
			if not args.id:
				print row[0].ljust(11), row[1].ljust(11)
			else:
				print str(row[0]).ljust(4), row[1].ljust(11), row[2].ljust(11)
	print 

def delete(args):
	if args.purge:
		conf = raw_input("Confirm delete all? [y/n]: ")
		if conf == 'y':
			c.execute("drop table main")
			print "Confirmed."
		else:
			print "Cancelled."
	else:
		try:
			c.execute('delete from main where oid=?',args.i)
		except sqlite3.Error as e:
			print "And error occured while deleting: " + e.args[0]
	
#initialize the arg parser
parser = argparse.ArgumentParser(description='A simple note keeping program.')
subparsers = parser.add_subparsers(help='Sub-command help')

add_parser = subparsers.add_parser('add',help='Add a note')
add_parser.add_argument('-t',help='Include note tag')
add_parser.add_argument('-m',help='Note text',required=True)
add_parser.set_defaults(func=add)

view_parser = subparsers.add_parser('ls',help='View notes')
view_parser.add_argument('-i','--id',help="List IDs of notes",action='store_true',default=None)
view_group = view_parser.add_mutually_exclusive_group(required=True)
view_group.add_argument('--all','-a',help='Show all notes',action='store_true')
view_group.add_argument('-t',help='Show tagged notes (blank for untagged notes)', const="", nargs='?')
view_parser.set_defaults(func=print_list)

del_parser = subparsers.add_parser('rm',help='Delete a note')
del_group = del_parser.add_mutually_exclusive_group(required=True)
del_group.add_argument('--purge',help='Delete all existing notes',action='store_true')
del_group.add_argument('-i',help="Note ID to be deleted")
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
