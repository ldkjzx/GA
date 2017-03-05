#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jarod Zheng'

'''
#Genetic Algorithm#

	Template/Target 
		* 进化模版，指示进化方向和最终形态

	Gene
		* 三角形
		* 三点位置（x，y），颜色 rbga

	Body 
		* 由1000个Gene组成

	Population 
		* 由20个继承个体+3个变异个体组成

	Selection 
		* 从种群中选择与进化模版差异最小的个体

	Original 
		* 初代，完全随机的个体

==============================
	Crossover
		* 基于选择个体进行随机有限偏移量计算
		* 偏移量为1,0,-1
		* 新一代基因在原基因基础上随机偏移形成
		* 偏移边界，新一代基因属性必须在最大边界和最小边界之间
		* 进而形成新一代种群

	Mutation 
		* 偏移量为-10~10间任意数值
		* 形成变异个体

	Generation 
		* 遗传代数，用t表示
		* t=0, 初代
		* t=100000, 10万代终止
		* 抽样检查，每1000代获取适应性强个体打印出来
'''

import datetime, time, sys, os, argparse, copy

from PIL import Image, ImageDraw
from random import randint as _r



# Configuration
GENE_VOLUME = 1000	# the volume of gene in one single body 
GENE_OFFSET = 20	# the max offset range of child's gene based on parent's
GENE_MUTATE = 100	# the max offset range of mutated gene based on parent's
MAX_GENERATION = 100000	# the maximun generations in the world
SAMPLE_RATE = 10000	# how many generations to get one boy print out

# Evolution Taget
TARGET_PATH = os.path.join(os.path.abspath('.'), 'pic', 'Target.png')
TARGET_IMAGE = Image.open(TARGET_PATH)
IMAGE_HEIGHT = TARGET_IMAGE.size[0]
IMAGE_WIDTH = TARGET_IMAGE.size[0]
TARGET_PIXELS = [TARGET_IMAGE.getpixel((x,y)) for x in range(TARGET_IMAGE.size[0]) for y in range(TARGET_IMAGE.size[1])]


# Public Function: get random offset value based on the given value
def rmInRange(old_value, offset, minsize, maxsize): 
	new_value = old_value + _r(-offset, offset)
	new_value = max(minsize, min(new_value, maxsize))
	return new_value

# Basic Element of Gene: Point
class Point(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y			

	def random(self):
		rm_point = Point()
		rm_point.x = _r(0, IMAGE_WIDTH)
		rm_point.y = _r(0, IMAGE_HEIGHT)
		#rm_point.x = rmInRange(200, GENE_OFFSET, 0, IMAGE_WIDTH)
		#rm_point.y = rmInRange(200, GENE_OFFSET, 0, IMAGE_HEIGHT)
		return rm_point

	def cld_point(self):
		cld_point = Point()
		cld_point.x = rmInRange(self.x, GENE_OFFSET, 0, IMAGE_WIDTH)
		cld_point.y = rmInRange(self.y, GENE_OFFSET, 0, IMAGE_HEIGHT)
		return cld_point

	def mut_point(self):
		mut_point = Point()
		mut_point.x = rmInRange(self.x, GENE_MUTATE, 0, IMAGE_WIDTH)
		mut_point.y = rmInRange(self.y, GENE_MUTATE, 0, IMAGE_HEIGHT)
		return mut_point

	def getPoint(self):
		return (self.x, self.y)

# Basic Element of Gene: Color
class Color(object):
	def __init__(self, r=255, g=255, b=255, a=255):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def random(self):
		rm_color = Color()
		rm_color.r = _r(0,255)
		rm_color.g = _r(0,255)
		rm_color.b = _r(0,255)
		#rm_color.a = _r(85,170)
		return rm_color

	def cld_color(self):
		cld_color = Color()
		for attr in ['r', 'g', 'b']:
			setattr(cld_color, attr, rmInRange(getattr(self, attr), GENE_OFFSET, 0, 255))
		return cld_color

	def mut_color(self):
		mut_color = Color()
		for attr in ['r', 'g', 'b']:
			setattr(mut_color, attr, rmInRange(getattr(self, attr), GENE_OFFSET, 0, 255))
		return mut_color

	def getColor(self):
		return (self.r, self.b, self.g, self.a)


# Build Gene with basic Elements: Triangles
class Gene(object):
	def __init__(self):
		self.point_1 = Point()
		self.point_2 = Point()
		#self.point_3 = Point()
		self.color = Color()

	def origin(self):
		o_gene = Gene()
		o_gene.point_1 = Point().random()
		o_gene.point_2 = o_gene.point_1.cld_point()
		#o_gene.point_3 = o_gene.point_2.cld_point()
		#o_gene.point_2 = Point().random()
		#o_gene.point_3 = Point().random()
		o_gene.color = Color().random()
		return o_gene

	def cld_gene(self):
		cld_gene = Gene()
		cld_gene.point_1 = self.point_1.cld_point()
		cld_gene.point_2 = self.point_2.cld_point()
		#cld_gene.point_3 = self.point_3.cld_point()
		cld_gene.color = self.color.cld_color()
		return cld_gene

	def mut_gene(self):
		mut_gene = Gene()
		mut_gene.point_1 = self.point_1.mut_point()
		mut_gene.point_2 = self.point_2.mut_point()
		#mut_gene.point_3 = self.point_3.mut_point()
		mut_gene.color = self.color.mut_color()
	
		return mut_gene


	def active(self):
		temp_image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255,255,255))
		draw = ImageDraw.Draw(temp_image)
		draw.polygon([self.point_1.getPoint(), self.point_2.getPoint(), self.point_3.getPoint()], fill=self.color.getColor())


# Build Body based on Genes
class Body(object):
	def __init__(self):
		self.gene = []

	def bodyCreation(self):
		temp_body = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255,255,255))
		draw = ImageDraw.Draw(temp_body)

		for i in range(GENE_VOLUME):
			draw.line((self.gene[i].point_1.getPoint(), self.gene[i].point_2.getPoint()), fill=self.gene[i].color.getColor())

		return temp_body

	def origin(self):
		origin = Body()
		for i in range(GENE_VOLUME):
			origin.gene.append(Gene().origin())

		return origin

	def child(self):
		child = Body()
		for i in range(GENE_VOLUME):
			child.gene.append(self.gene[i].cld_gene())

		return child

	def mutate(self):
		mutate = Body()
		for i in range(GENE_VOLUME):
			mutate.gene.append(self.gene[i].mut_gene())

	def getPixels(self):
		temp_image = self.bodyCreation()
		pixels = [temp_image.getpixel((x,y)) for x in range(temp_image.size[0]) for y in range(temp_image.size[1])]

		return pixels


# Create evolution rules and trigger the generations
class GodsHand(object): 
	def __init__(self, body):
		self.parent = body
		self.pixels = self.parent.getPixels()
		self.g = 0


	def diff(self):
		diff = 0
		for i in range(len(TARGET_PIXELS)):
			diff_r = abs(TARGET_PIXELS[i][0] - self.pixels[i][0])
			diff_g = abs(TARGET_PIXELS[i][1] - self.pixels[i][1])
			diff_b = abs(TARGET_PIXELS[i][2] - self.pixels[i][2])
			diff = diff + diff_r + diff_b + diff_g

		return diff

	def evolution(self):
		while True:
			if self.g > MAX_GENERATION:
				break

			self.child = self.parent.child()
			parent_diff = GodsHand(self.parent).diff()
			child_diff = GodsHand(self.child).diff()

			if child_diff < parent_diff:
				self.parent = self.child
			
			if self.g % 100 == 0:
				print('Generation: %d' % self.g)
				print('Completed: %d / %d' % (self.g, MAX_GENERATION))
				print('Parent Difference: %d ==> Child Difference: %d' % (parent_diff, child_diff))
				print (datetime.datetime.now())
				print ('-----------------------------------------------')
			
			if self.g % SAMPLE_RATE == 0:
				self.parent.bodyCreation().save(os.path.join(os.path.abspath('.'), 'pic', '%s.png' % self.g))

			self.g += 1



################################################
def main():

	
	
	Adam = Body().origin()	# Create the original body Adam
	GodsHand(Adam).evolution()	# Put Adam in God's Hand and start the evolution

	'''
	Adam.bodyCreation().save(os.getcwd()+'/pic/Adam.png')
	Adam.child().bodyCreation().save(os.getcwd()+'/pic/Adam2.png')
	Adam.child().child().bodyCreation().save(os.getcwd()+'/pic/Adam3.png')
	'''
	# 差异值计算速度
	'''
	print (datetime.datetime.now())
	print(GodsHand(Adam).diff())
	print (datetime.datetime.now())
	'''


if __name__=='__main__':
	main()



