import pkgutil

from django.db.models.signals import post_syncdb
import models

from mezzyblocks import blocktypes
from models import BlockType, BlockTypeSetting

def blocktypes_setup( sender, **kwargs ):
	"""Will loop over blocktypes, ensure they are present in the database, and
	that their config is also available there."""

	for _, btname, _ in pkgutil.iter_modules(blocktypes.__path__):

		# Make sure the blocktypes are defined in database, keep object around
		# for the blocktype settings later on.
		bt = BlockType.objects.filter( name=btname )
		if bt:
			bt = bt[0]
		else:
			bt = BlockType( name=btname, path=btname )
			bt.save()

		# Get the settings from the blocktype
		btmod = __import__( "mezzyblocks.blocktypes." + bt.name, fromlist='block_settings' )

		print dir(btmod.block_settings)

		# Loop over them, check if they're in DB, add otherwise.
		for btname, btfname, default in btmod.block_settings:
			bts = BlockTypeSetting.objects.filter( blocktype_id=bt.pk, setting_name=btname )
			if not bts:
				bts = BlockTypeSetting( blocktype_id=bt.pk, setting_name=btname, friendly_name=btfname )
				bts.save()

		# All should be good now.

post_syncdb.connect( blocktypes_setup, sender=models )

