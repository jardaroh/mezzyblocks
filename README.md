# Blocks for Django
## By Jardar @ A2G Grafisk

Blocks for Django aims to give a centralized functionality layer for building easy to use "blocks/modules" for websited using Mezzanine.


## Requirements
1. Django
2. Mezzanine
3. Mezzanine - Pages


## Installation

1. unpack mezzyblocks to your project folder
2. add mezzyblocks to your installed apps in settings.py
3. add mezzyblocks.middleware.BlocksTemplateContextMiddleware to your middleware in settings.py
4. do a manage.py syncdb


## Usage

1. load block_tags in your template /* {% load block_tags %} */
2. use /* {% block_position "any_position" %} */ wherever in your template
3. in your admin panel, add a block position in the mezzyblocks app /* name of the position should reflect a block_position tag argument in your template */
4. create a new block, select the block's type and give it the position you want


## Creating your own blocktypes

Blocktypes have 1 required file, in the 'mezzyblocks/blocktypes' folder.
A block requires 1 function called 'block_context_processor' taking one argument that is the block object.
'block_context_processor' must return an html string, you can optionally make use of Django's template layer to render your block, import 'render_to_string' from 'django.template.loader'. Make use of it as you otherwise would at the end of a view function.

1. create a new python file in the 'mezzyblocks/blocktypes' folder ending with .py
2. import whatever modules you need for your block to do it's job at the top of the file
3. optionally 'from django.template.loader import render_to_string' if you want to use a template render for your block
4. create a function 'block_context_processor' and give it one argument, like so 'block_context_processor(block):'
5. at the end of the function, return any kind of string, /* This string could for example be html */

You are free to do any type of logic you need within this function, like getting whatever pages you want from the Mezzanine CMS and list links to them or display excerpts for that matter. What you do within the block is entirely up to you.