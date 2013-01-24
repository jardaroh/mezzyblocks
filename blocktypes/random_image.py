from random import choice

from django.template import Context, Template
from django.template.loader import get_template, render_to_string
from django.core.exceptions import ObjectDoesNotExist

from mezzanine.conf import settings
from mezzanine.galleries.models import Gallery

from mezzyblocks.models import BlockConfig, BlockTypeSetting

# Config options available for this block, name and friendly name.
# Defined here, so they'll be auto-included in database after syncdb.
#
# NOTE: When changing set of available settings, remember syncdb.
block_settings = (
	(
		'gallery', 'Gallery', "RandomGallery",
	),
)


def getSetting( block, setting, default=None ):
	"""Get a settings value configured for a block, or it's default."""
	# value = BlockConfig.objects.get(
	# 	block_id = block.id,
	# 	setting = BlockTypeSetting.objects.get(
	# 		blocktype = block.blocktype_id,
	# 		setting_name = setting )
	# ).value

	# if not value: value = default

	value = default
	try:
		value = BlockConfig.objects.get(
			block_id = block.id,
			setting = BlockTypeSetting.objects.get(
				blocktype = block.blocktype_id,
				setting_name = setting
			)
		).value
	except ObjectDoesNotExist:
		pass

	return value


def block_context_processor(block):

	gallery = getSetting( block, "gallery", block_settings[0][2] )

	# folder = Gallery.objects.get(title=gallery)
	# files = folder.images.all()
	# rand_file = choice(files)

	try:
		folder = Gallery.objects.get(title=gallery)
	except Gallery.DoesNotExist:
		folder = None

	title = ""
	image = None
	if folder:
		files = folder.images.all()
		rand_file = choice(files)

	# title = rand_file.description
	# image = settings.MEDIA_URL+str(rand_file.file)
	# image = image[1:]

		if rand_file:
			title = rand_file.description
			image = settings.MEDIA_URL+str(rand_file.file)
			image = image[1:]

	#Fill this context with any KEY, VALUE pairs
	#to pass them to the template
	c = Context(
		{
			#'title': folder.images,
			'title': title,
			'image': image
		}
	)
	#Return an html string back to the Block Middleware
	html = render_to_string('random_image.html', c)
	return html

