#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import MySQLdb

def getLatestArticleID( cur ):
	cur.execute( 'select id from test order by id desc;' )
	rows = cur.fetchall()
	if len( rows ) == 0:
		return '0'
	else:
		return rows[0][0] # 1st element of 1st singleton tuple in list


def transformArticle( text ):
	text = '<article lang="en">\n\t\t\t<section>\n\t\t\t\t<p>' + text + '\t\t\t\t</p>\n\t\t\t</section>\n\t\t</article>'

	exp = re.compile( u'(スチューアト)' )
	text = exp.sub( u'<span class="kana" lang="ja">\g<1></span>', text )
	sectionExp = re.compile( '\n\n\n+' )
	text = sectionExp.sub( '</p>\n\t\t\t</section>\n\t\t\t<section>\n\t\t\t\t<p>', text )
	pExp = re.compile( '\n\n+' )
	text = pExp.sub( '</p>\n\t\t\t\t<p>', text )

	return text
