---  A simple Python note-taking tool for the command line ---

A simple program I wrote to practice Python, SQL and argument parsing from the command line.

Useage:

	note add -t TAG (optional) -m NOTE (required)

	note ls [-a | -t TAG] (required) -i (optional)

	note rm [--purge | -i ID] (required)

Tags are optional in all cases, you can leave them blank if desired. To remove a note you need to give the proper ID from the -i optional flag on the list command.


To install:

	sudo chmod +x note && cp note /usr/bin/

The database will save to the home directory as .note.db
