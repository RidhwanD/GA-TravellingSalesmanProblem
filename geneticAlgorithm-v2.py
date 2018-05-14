import random

class FitnessCalc:
	jarak = {}
	kecepatan = {}

	def __init__ (self):
		self.jarak = {
			"S" : {0 : 6.0, 1 : 14.0, 2 : 10.0},
			0 : {1 : 4.0, 3 : 16.0},
			1 : {0 : 4.0, 2 : 4.0, 4 : 15.0},
			2 : {1 : 4.0, 5 : 12.0},
			3 : {0 : 16.0, 4 : 4.0, "G" : 9.0},
			4 : {1 : 15.0, 3 : 4.0, 5 : 4.0, "G" : 9.0},
			5 : {2 : 12.0, 4 : 4.0, "G" : 6.0}
		}

		self.kecepatan = {
			"S" : {0 : 90, 1 : 70, 2 : 60},
			0 : {1 : 40, 3 : 40},
			1 : {0 : 40, 2 : 80, 4 : 60},
			2 : {1 : 60, 5 : 40},
			3 : {0 : 40, 4 : 120, "G" : 70},
			4 : {1 : 60, 3 : 120, 5 : 70, "G" : 80},
			5 : {2 : 40, 4 : 70, "G" : 40}
		}
		

	def getFitness(self, ind):
		route = []
		fitness = 0
		now = "S"
		for i in range (30):
			if (ind.getGene(i) == 1):
				try:
					time = self.jarak[now][i%6]/ (self.kecepatan[now][i%6] if self.kecepatan[now][i%6] <= 60 else 60)
					if (i%6 not in route):
						route.append(i%6)
						fitness += time
						now = i%6
				except (KeyError):
					fitness = fitness
		try:
			time = self.jarak[now]["G"]/(self.kecepatan[now]["G"] if self.kecepatan[now]["G"] <= 60 else 60)
			fitness += time
		except (KeyError):
			fitness += 10
		return 1000 - fitness*60

	def getRoute(self, ind):
		route = []
		now = "S"
		route.append("S")
		for i in range (30):
			if (ind.getGene(i) == 1):
				try:
					self.jarak[now][i%6]
					if (self.convert(i%6) not in route):
						route.append(self.convert(i%6))
						now = i%6
				except (KeyError):
					route = route
		try:
			self.jarak[now]["G"]
			route.append("G")
		except (KeyError):
			route = route
		return route

	def convert(self,a):
		city = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F"}
		return city[a]


class Individu:
	defaultGeneLength = 30
	genes = []
	fitness = 0

	def __init__ (self):
		self.genes = []
		for i in range(self.defaultGeneLength):
			if (random.uniform(0,1) < 0.5):
				self.genes.append(0)
			else:
				self.genes.append(1)

	def getGene(self, index):
		return self.genes[index]

	def setGene(self, index, value):
		self.genes[index] = value

	def getFitness(self):
		if (self.fitness == 0):
			f = FitnessCalc()
			self.fitness = f.getFitness(self)
		return self.fitness


class Populasi:
	individuals = []

	def __init__(self,sial):
		if (sial):
			for i in range(12):
				a = Individu()
				self.individuals.append(a)
		else:
			self.individuals = []

	def getIndividu(self, index):
		return self.individuals[index]

	def addIndividu(self, ind):
		self.individuals.append(ind)

	def removeIndividu(self, ind):
		self.individuals.remove(ind)

	def getFittest(self):
		fittest = self.individuals[0]
		for i in self.individuals:
			if (i.getFitness() > fittest.getFitness()):
				fittest = i
		return fittest


class Algorithm:
	uniformRate = 0.5
	mutationRate = 0.05
	dot = 15

	def crossover2(self, ind1, ind2):
		indnew = Individu()
		for i in range(self.dot):
			indnew.setGene(i,ind1.getGene(i))
		for i in range(self.dot,30):
			indnew.setGene(i,ind2.getGene(i))
		
		return indnew

	def mutate (self,ind1):
		for i in range(30):
			if (random.uniform(0,1) < self.mutationRate):
				ind1.setGene(i,1-ind1.getGene(i))
		return ind1

	def roulleteWheel(self,pop):
		totFitness = 0
		for i in range(12):
			totFitness += pop.getIndividu(i).getFitness()
		rand = random.uniform(0,totFitness)
		count = 0
		i = 0
		while (count < rand):
			count += pop.getIndividu(i).getFitness()
			i += 1
		return pop.getIndividu(i-1)

	def evolvePopulation(self, pop):
		anak = []
		for i in range(12):
			anak.append(self.crossover2(self.roulleteWheel(pop),self.roulleteWheel(pop)))

		for a in anak:
			a = self.mutate(a)
			pop.addIndividu(a)
		
		newPopulasi = Populasi(False)

		for i in range(12):
			newPopulasi.addIndividu(pop.getFittest())
			pop.removeIndividu(pop.getFittest())

		return newPopulasi

#					MAIN PROGRAM

pop = Populasi(True)
algo = Algorithm()
fit = FitnessCalc()

for i in range(1000):
	print pop.getFittest().genes, "Best Fitness:", pop.getFittest().getFitness()
	pop = algo.evolvePopulation(pop)

print "Waktu tempuh: " + str(1000 - pop.getFittest().getFitness())
print "Route: " + str(fit.getRoute(pop.getFittest()))

