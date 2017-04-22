"""
	jikji/publisher
	----------------
	Publish generated files
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil
from . import utils

class Publisher :
	""" Publisher Interface
	"""

	def __init__(self, generator) :
		""" Constructor of Publisher
		"""
		self.generator = generator
	

	def publish(self) :
		""" Publish implmentation function
		"""
		pass


class LocalPublisher(Publisher) :
	""" LocalPublisher
	"""
	
	def __init__(self, generator, clear_legacy=False) :
		""" Constructor of LocalPublisher
		:param generator: Generator object
		:param clear_legacy: Clear legacy files in output dir if True
		"""
		Publisher.__init__(self, generator)
		self.clear_legacy = clear_legacy



	def publish(self) :
		""" Publish to local output dir
		"""
		output_root = self.generator.app.settings.OUTPUT_ROOT

		if self.clear_legacy :
			if os.path.exists( output_root ) :
				shutil.rmtree( output_root )

		# Copy tmp dir to output dir		
		utils.copytree2(
			src = self.generator.tmp_output_root,
			dst = output_root
		)

		

class RestPublisher(Publisher) :
	pass


class S3Publisher(Publisher) :
	pass

