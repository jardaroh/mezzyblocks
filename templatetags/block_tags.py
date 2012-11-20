from django import template
register = template.Library()

@register.inclusion_tag( 'block_position.html', takes_context=True )
def block_position( context, position ):
	"""Will render and return content for a named block position, if a block is defined for it."""

	usedblocks = []
	try:
		blocks = context['request'].blocks
		for block in blocks:
			if block.position.name == position: usedblocks.append( block )
	except AttributeError:
		# No blocks found, no big deal.
		pass

	return { 'blocks': usedblocks,
			 'position': position }

