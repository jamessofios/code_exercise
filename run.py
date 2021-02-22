#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'James Sofios'
__email__ = 'jamessofios@gmail.com'

import yaml # run "pip install pyyaml"
import boto3 # run "pip install boto3"

def yaml_load(path):
	with open(path, 'r') as fd:
		data = yaml.load(fd, Loader=yaml.FullLoader)
	return data

def main():
	image_id = input('Please enter your ImageID: ')

	path = 'config.yaml'

	data = yaml_load(path)

	server = data.get('server')

	# create a new EC2 instance
	ec2 = boto3.resource('ec2')

	instance = ec2.create_instances(

		BlockDeviceMappings=[
			{
				'DeviceName': server.get('volumes')[0],
				'VirtualName': '/',

				'Ebs': {
					'VolumeSize': server.get('volumes')[0].get('size_gb')
				}
			},
			{
				'DeviceName': server.get('volumes')[1],
				'VirtualName': '/data',

				'Ebs': {
					'VolumeSize': server.get('volumes')[1].get('size_gb')
				}
			}
		],

		ImageId=image_id,

		MinCount=server.get('min_count'),

		MaxCount=server.get('max_count'),

		InstanceType=server.get('instance_type')
	)

	ec2.create_user( UserName=server.get('users')[0].get('login') )

	ec2.create_user( UserName=server.get('users')[1].get('login') )

if __name__ == '__main__':
	main()
