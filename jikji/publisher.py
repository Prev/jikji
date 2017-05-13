"""
	jikji/publisher
	----------------
	Publish generated files
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil
from . import utils
from .cprint import cprint

class Publisher :
	""" Publisher Interface
	"""

	def __init__(self) :
		""" Constructor of Publisher
		"""
		pass
	

	def publish(self, generator, generation_result=None) :
		""" Publish implmentation function
		:param generator: Generator object
		:param generation_result: Result list of generation
		"""

		for sucesses, errors, ignores, pagegroup in generation_result :
			if pagegroup :
				pagegroup.after_published(sucesses, errors, ignores)


class LocalPublisher(Publisher) :
	""" Publish to local disk
	"""
	
	def __init__(self, output_root, clear_legacy=False) :
		""" Constructor of LocalPublisher
		:param output_root: Root directory of output files
		:param clear_legacy: Clear legacy files in output dir if True
		"""
		self.output_root = output_root
		self.clear_legacy = clear_legacy



	def publish(self, generator, generation_result=None) :
		""" Publish to local output dir
		"""
		if self.clear_legacy :
			if os.path.exists( self.output_root ) :
				shutil.rmtree( self.output_root )

		cprint.line('Using LocalPublisher')
		cprint.line('Copy output to "%s"' % self.output_root)

		# Copy tmp dir to output dir		
		utils.copytree2(
			src = generator.tmp_output_root,
			dst = self.output_root
		)

		Publisher.publish(self, generator, generation_result)

		


class S3Publisher(Publisher) :
	""" Amazon Simple Storage Service (S3) Publisher
		Require install & configure boto3 (https://boto3.readthedocs.io/)
	"""
	
	def __init__(self, bucket) :
		""" Constructor
		:param bucket: Bucket name of S3
		"""
		self.bucket = bucket


	def publish(self, generator, generation_result) :
		""" Publish to S3
		"""
		import boto3, mimetypes
		from .generator import urltopath
		s3 = boto3.resource('s3')


		cprint.line('Using S3Publisher')
		cprint.line('Upload output to Amazon S3\' bucket "%s"' % self.bucket)


		for sucesses, errors, ignores, pagegroup in generation_result :
			for pageurl in sucesses :
				file = generator.get_tmp_filepath(pageurl)
				object_key = urltopath(pageurl)

				cprint.write('PUT ' + object_key)
				s3.Object(self.bucket, object_key).put(
					Body = open(file, 'rb'),
					ACL = 'public-read',
					ContentType = mimetypes.guess_type(file)[0],
				)
				cprint.ok('\rPUT ' + object_key)

			if pagegroup :
				pagegroup.after_published(sucesses, errors, ignores)



class RestPublisher(Publisher) :
	# TODO
	pass



