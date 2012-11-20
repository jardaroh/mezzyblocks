from django.db import models
from mezzanine.pages.models import Page

# Block is dependent on Pages app from Mezzanine
class Block(models.Model):
	title = models.CharField( max_length=35, blank=False, null=False )
	blocktype = models.ForeignKey( "BlockType", blank=False, null=False )
	pages = models.ManyToManyField( Page, blank=True, null=True )
	position = models.ForeignKey( "BlockPosition", blank=False, null=False )
	published = models.BooleanField( blank=True, null=False, default=False )

	def __unicode__(self):
		return self.title

# Positions for blocks
class BlockPosition(models.Model):
	name = models.CharField( max_length=35, blank=False, null=False )
	description = models.TextField( blank=True, null=True )

	def __unicode__(self):
		return self.name

class BlockType(models.Model):
	name = models.CharField( max_length= 35, blank=False, null=False )
	path = models.CharField( max_length=255, blank=False, null=False )

	def __unicode__(self):
		return self.name

class BlockTypeSetting( models.Model ):
	blocktype	  = models.ForeignKey( BlockType )
	setting_name  = models.CharField( max_length=255, blank=False, null=False )
	friendly_name = models.CharField( max_length=255, blank=False, null=False )

	def __unicode__( self ):
		#return "%s.%s" % ( self.blocktype.name, self.setting_name )
		return self.friendly_name

class BlockConfig( models.Model ):
	block		 = models.ForeignKey( Block )
	setting		 = models.ForeignKey( BlockTypeSetting )
	value		 = models.CharField( max_length=255, blank=False, null=False )

	def __unicode__( self ):
		#return "%s.%s: %s" % ( self.setting.blocktype.name, self.setting.setting_name, self.value )
		return "%s: %s" % ( self.setting.friendly_name, self.value )

# NOTE: If caching of any kind (memcached or similar) is implemented, this
# should be kept there.  It doesn't matter if we loose this data, and it's
# only valid for 10 mins anyway.  It'll add extra load to the mysql database,
# etc.  For a proof of concept-level thing, that harly matters, so just
# shoving it in there for now.
#
# NOTE: Data here might be deleted *at will*.  In fact, it probably *should*
# be deleted every time fresh data is fetched, to avoid filling it with old
# crap.
# 
# NOTE: Rule of thumb for using:
#		* Delete *all* data more than 2 hours old for *all* places.
#       * Do we have any data that's less than 11 mins old?  Use it.
#       * Can we fetch data?  If so, use it, update cache, if not:
#       * Do we have any data less than 2 hours old?  Use it.
#       * Give up.
#
# Typical thing to toss in here would be:
#    place   = Norge/Hordaland/Bergen/Sandviken
#    updated = When the data was fetched
#    hour    = "10:30", which hour the data is for
#    thing   = "C" == Celcius
#	 value   = "4" == Number of degrees C
#
# NOTE: Since we won't accumulate logged data, we don't care too much about
# splitting place to a separate table, to keep columns shorter in this one.
# It would give us work, and gain nothing.
#
class YrCache( models.Model ):
	place		= models.CharField( max_length=255, blank=False, null=False )
	updated		= models.DateTimeField( auto_now_add=True, blank=False, null=False)
	hour		= models.CharField( max_length=255, blank=False, null=False )
	thing		= models.CharField( max_length=255, blank=False, null=False )
	value		= models.CharField( max_length=255, blank=False, null=False )

