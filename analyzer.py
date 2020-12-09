import stanza

class Analyzer():

	def __init__(self, expression):
		self.nlp = stanza.Pipeline('ja')
		self.expression = expression
		self.data = []

	def load_data_from_path(self, path):
		with open (path, 'r') as fin:
			lines = fin.readlines()
			for line in lines:
				divided = line.split('\t')
				self.data.append(divided[1].strip()) # 0 was the tag type, here we just need 1

	def load_data_directly(self, results):
		for tup in results:
			text = tup[1] # we only need the text, not the tag it came from
			self.data.append(text.strip())

	def analyze_data(self):
		for d in self.data:
			try:
				doc = self.nlp(d)
				print('\nExtracted text: ', d)
				for sentence in doc.sentences:
					# print('printing sentence\n', sentence)
					for word in sentence.words:
						print('{}\t{}\t{}'.format(word.text, word.xpos, word.upos))
			except:
				print('STANZA PROCESSING ERROR: Stanza could not properly handle this text.')

	def write_analysis(self):
		f_name = self.expression + ' analysis.txt'
		print('\n*** WRITING DATA TO FILE: ', f_name, ' ***')
		fout = open(f_name, "w")
		fout.write('Sentences and phrases containing target expression {} ...\n'.format(self.expression))
		for d in self.data:
			fout.write('\nExtracted text: ' + d + '\n')
			try:
				doc = self.nlp(d)
				for sentence in doc.sentences:
					for word in sentence.words:
						line = word.text + '\t' + word.xpos + '\t' + word.upos + '\n'
						fout.write(line)
			except:
				line = 'STANZA PROCESSING ERROR: Stanza could not properly handle this text.\n'
				fout.write(line)
		fout.write('\n')
		fout.close()

if __name__=='__main__':
	analyzer = Analyzer('黒文字')
	analyzer.load_data_from_path('sample.txt')
	analyzer.analyze_data()
	analyzer.write_analysis()


