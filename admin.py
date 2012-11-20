from mezzyblocks.models import Block, BlockPosition, BlockType, BlockConfig, BlockTypeSetting
from django.db.models.query import QuerySet
from django.contrib import admin

admin.site.register(BlockPosition)

class BlockConfigInline( admin.StackedInline ):
	model = BlockConfig
	extra = 2

	def formfield_for_foreignkey( self, db_field, request, **kwargs ):
		"""formfield_for_foreignkey, set up to limit available settings to
		those available on current blocktype."""
		if db_field.name == 'setting':
			# Note that we *can not* pull a list of which settings are
			# available for a given block type, when we're creating a block.
			# This is because blocks are created without a type, so we don't
			# know which type it'll be, when we're creating the block here.
			# What we do is simply see if we can figure out a block-type, and
			# if not, well... give up.
			# This *can* be fixed, but it'd have to either be browser-side,
			# using javascript to hook on to changes to block-type, then
			# requesting the available settings for the type either from the
			# server, or from something hidden in the HTML, that defines
			# available settings for *all* block-types.
			# Alternative would be a larger re-write of the admin-interface,
			# so that you're choosing block-type before getting presented with
			# the options for it.
			try:
				bt = Block.objects.filter( pk=request.path.strip('/').split('/')[-1] )
				bt = bt.get().blocktype

				# Give a queryset, limiting shown settings to those available on
				# current blocktype.
				kwargs['queryset'] = BlockTypeSetting.objects.filter( blocktype_id=bt )
			except ValueError:
				pass

		return super( BlockConfigInline, self ).formfield_for_foreignkey( db_field, request, **kwargs )

class BlockAdmin( admin.ModelAdmin ):
	inlines = [BlockConfigInline]

admin.site.register( Block, BlockAdmin )

