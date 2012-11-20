from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlquote

from mezzanine.conf import settings
from mezzanine.pages import page_processors
from mezzanine.pages.models import Page
from mezzanine.pages.views import page as page_view
from mezzanine.utils.urls import path_to_slug

from mezzyblocks.models import Block

# A template context middleware that will get and append any appropriate
# blocks to the template context
class BlocksTemplateContextMiddleware(object):

	ifblocks = False

	def process_block(self, block):
		module = __import__( "mezzyblocks.blocktypes." + block.blocktype.path, fromlist='block_context_processor')
		html = module.block_context_processor(block)
		return html

	def process_request(self, request):
		try: # Hope that we find the Page object
			slug = request.path[1: -1] # remove the first and last slash from the request path
			page = Page.objects.get(slug=slug)
		except Page.DoesNotExist:
			print "Did not find any Page with path: "+request.path
			page = False

		if page: # We found a matching Page object

			try: # Attempt to find blocks for our Page object
				blocks = page.block_set.filter(published=True)

				try: # Time to add our blocks to the template context!
					response.context_data.blocks = {}
				except:
					non = False

				if blocks: # If we found any blocks at all

					blocks_temp = []
					i = 0
					for block in blocks:
						# Wrap the block in a special DIV container for a2gcms blocks
						# process the block and insert it
						# at the end we close the wrapping DIV container
						#
						# XXX: This will render the block, regardless of if
						# it's actually included in the template or not.  It's
						# also hard-coding HTML, instead of relying on django
						# template-processing.
						# I'm thinking this does not belong here, but rather
						# in the template of the tag-processing.
						# It's unclear if there's a point to a2gcms_block.
						# One reason to have it could be hookability from
						# javascript, but in that case the blocktype and
						# probably an ID should be included as attributes.
						# If hookability is the point, it *definitively*
						# belongs in the template or a static, keeping the
						# HTML with the javascript.
						# Possible exception only if it's part of a clearly
						# defined API.
						html = '<div class="a2gcms_block">'
						html += self.process_block(block)
						html += '</div>'
						block.html = html
						blocks_temp.append(block)
						#print html
						i = i+1

						
					# response.context_data.blocks = blocks_temp
					request.blocks = blocks_temp
					self.ifblocks = i

			except Block.DoesNotExist:
				print "We found no blocks..."
				blocks = False
		return None

	def process_template_response(self, request, response):

		print self.ifblocks

		if self.ifblocks:
			response.context_data.ifblocks = self.ifblocks

		self.ifblocks = False

		return response

