#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import MySQLdb
import sys
from article import getLatestArticleID

def main():
	if len( sys.argv ) < 2:
		print 'usage: ' + sys.argv[0] + ' filename [id]'
		return

	db = MySQLdb.connect(
		db="REDACTED",
		use_unicode=True,
		charset='utf8',
		read_default_file="../.my.cnf"
	)
	cur = db.cursor()

	filename = sys.argv[1]
	if len( sys.argv ) >= 3:
		articleID = sys.argv[2]
	else:
		articleID = str( int( getLatestArticleID( cur ) ) + 1 )

	db = MySQLdb.connect( host="REDACTED", user="REDACTED", passwd="REDACTED", db="REDACTED", use_unicode=True, charset='utf8' )
	
	cur = db.cursor()
	
	f = codecs.open( filename, 'r', encoding='utf-8' )
	
	text = f.read()
	
	cur.execute( 'insert into test values (%s, \'%s\');' % (articleID, text.replace('\'', '\\\'') ) )
	
	db.commit()
	
	db.close()

if __name__ == '__main__':
	main()
