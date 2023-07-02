import hashlib
import itertools
import string
import time
import os
from threading import Thread

if os.name == "nt":
	command_clear = "cls"
else:
	command_clear = "clear"

class HashCracker(object):

	def ConfigurarCharlist(self,char_type,char_list="",*args,**kwargs):
		"""
		ConfigurarCharList(char_type,char_list)
		Esta função é usada para organizar e estabelecer a lista de caracteres, que serão utilizados na geração de uma lista de palavras para a wordlist. O parâmetro 'char_type' especifica a categoria de caracteres a serem usados, e 'char_list' é a lista onde você pode determinar quais caracteres exatamente serão utilizados.

		As opções para 'char_type' são:
		0 = Definir 'char_list' como a lista de caracteres personalizada
		1 = Todos os caracteres imprimíveis, incluindo letras (maiúsculas e minúsculas), números, símbolos e caracteres especiais (excluindo acentuações)
		2 = Todas as letras, maiúsculas e minúsculas
		3 = Apenas letras minúsculas
		4 = Apenas letras maiúsculas
		5 = Apenas números
		6 = Dígitos em hexadecimal
		7 = Dígitos em octal
		8 = Símbolos
		9 = Caracteres especiais

		Exemplos de uso:
		ConfigurarCharList(1)
		Nota: Neste caso, 'char_list' conterá letras (maiúsculas e minúsculas), números, símbolos e caracteres especiais.

		ConfigurarCharList(5)
		Nota: Aqui, 'char_list' será composta apenas por números.

		ConfigurarCharList(0, "abcdef123 ")
		Nota: Com esta configuração, 'char_list' será composta pelos caracteres "abcdef123 ", incluindo alguns números, algumas letras e um espaço.
		"""
		if (char_type==0):
			self.char_list = char_list
		elif (char_type==1):
			self.char_list = string.printable
		elif (char_type==2):
			self.char_list = string.ascii_letters
		elif (char_type==3):
			self.char_list = string.ascii_lowercase
		elif (char_type==4):
			self.char_list = string.ascii_uppercase
		elif (char_type==5):
			self.char_list = string.digits
		elif (char_type==6):
			self.char_list = string.hexdigits
		elif (char_type==7):
			self.char_list = string.octdigits
		elif (char_type==8):
			self.char_list = string.punctuation
		elif (char_type==9):
			self.char_list = string.whitespace

	def __init__(self,hash_list,hash_type,char_range,threads,char_type=1,char_list="",*args,**kwargs):
		"""
		HashCracker(hash_list, hash_type, char_range, threads, char_type=1, char_list="")
		Ao criar a instância principal, é necessário definir vários parâmetros. 'hash_list' é uma lista que contém as strings que representam cada hash a ser decifrado. 'hash_type' especifica o tipo de hash. 'char_range' determina o comprimento da string a ser gerada para a força bruta. 'threads' estabelece o número de threads que o sistema utilizará, sendo o mínimo exigido 1. Os próximos parâmetros são opcionais: 'char_type' define os tipos de caracteres que serão utilizados para a wordlist gerada na força bruta e 'char_list' onde é possível especificar os caracteres usados na criação da wordlist.

		Exemplos:
		HashCracker(["ceedb854f1f65aa21a59e6e651cd26a8"], "MD5", 15, 500, 0, "1234567890 ")
		Nota: Neste caso, temos apenas um hash do tipo MD5 para decifrar, utilizando 500 threads em tempo real. O hash será verificado em relação a uma wordlist de 15 caracteres, usando os números de 0 a 9 e um espaço.

		HashCracker(["ceedb854f1f65aa21a59e6e651cd26a8", "0aaac7e3ef2d14e7d6d8b215ecf509d1"], "MD5", 10, 100, 0, "1234567890 ")
		Nota: Aqui, temos dois hashes do tipo MD5 para decifrar, utilizando 100 threads em tempo real. Os hashes serão verificados com base em uma wordlist de 10 caracteres, usando os números de 0 a 9 e um espaço.

		HashCracker(["71a7676bf290b689fc7e6d5d89aba42ef012a448f9226b0667ca5d0fc0d5adfe9e5883b412d42d05584274ad5f8915deb222be781c52ce1f9a61574ed09ca3ca"], "SHA512", 10, 750, 2)
		Nota: Neste exemplo, temos um hash SHA512 a ser decifrado. Será utilizada uma wordlist de até 10 caracteres, contendo todas as letras maiúsculas e minúsculas, com um total de 750 threads.

		Definições de 'hash_type':
		"MD5"
		"SHA1"
		"sha224"
		"SHA256"
		"SHA384"
		"SHA512"
		"SHA512"
		"BLAKE2S"

		Definições para 'char_type':
		0 = Definir 'char_list' como a lista de caracteres personalizada
		1 = Todos os caracteres imprimíveis, incluindo letras (maiúsculas e minúsculas), números, símbolos e caracteres especiais (excluindo acentuações)
		2 = Todas as letras, maiúsculas e minúsculas
		3 = Apenas letras minúsculas
		4 = Apenas letras maiúsculas
		5 = Apenas números
		6 = Dígitos em hexadecimal
		7 = Dígitos em octal
		8 = Símbolos
		9 = Caracteres especiais
		"""
		self.hash_list = hash_list
		self.hash_type = hash_type
		self.char_range = char_range

		self.threads = threads
		self.wordlist = []
		for x in range(0,threads):
			self.wordlist.append([])

		self.ConfigurarCharlist(char_type,char_list)

		self.words_to_gen = 0
		for x in range(self.char_range):
			self.words_to_gen += len(self.char_list)**x

		self.word_generated = 0
		self.word_tested = 0

		self.hash_cracked = []
		self.finish = 0

	def Word2Hash(self,word):
		"""
		Word2Hash(word)
		Esta função simplesmente transforma uma string em hash, de acordo com o tipo de hash estabelecido quando o objeto é instanciado. É utilizada diretamente em conjunto com as combinações geradas.

		Exemplo:
		Word2Hash('conteudo')
		Nota: Na conversão, será gerado um hash correspondente ao tipo definido. Portanto, se o tipo de hash foi configurado como MD5, a string "conteudo" será convertida em seu equivalente hash, retornando "b59853db2f3ef8f156a72e38c30ba7d2".
		"""
		if self.hash_type=="SHA1":
			_hash = hashlib.sha1(word.encode())
		elif self.hash_type=="SHA224":
			_hash = hashlib.sha224(word.encode())
		elif self.hash_type=="SHA256":
			_hash = hashlib.sha256(word.encode())
		elif self.hash_type=="SHA384":
			_hash = hashlib.sha384(word.encode())
		elif self.hash_type=="SHA512":
			_hash = hashlib.sha512(word.encode())
		elif self.hash_type=="BLAKE2B":
			_hash = hashlib.blake2b(word.encode())
		elif self.hash_type=="BLAKE2S":
			_hash = hashlib.blake2s(word.encode())
		elif self.hash_type=="MD5":
			_hash = hashlib.md5(word.encode())
		else:
			_hash = hashlib.md5(word.encode())

		return _hash.hexdigest()
		
	def AgrupadorPalavras(self,limit=100000,*args,**kwargs):
		"""
		AgrupadorPalavras(limite)
		Essa função deve ser chamada sempre que for necessário inicializar e gerar as combinações de hash possíveis. O argumento 'limite' serve para modificar o buffer de palavras pendentes, ajudando a prevenir a sobrecarga de processamento e uso excessivo de memória RAM, otimizando assim o desempenho.

		Exemplo:
		AgrupadorPalavras(10)
		Nota: Se a diferença entre o total de palavras geradas e o total de palavras testadas for inferior a 10, a função vai aguardar um tempo antes de voltar a agrupar as combinações.

		Por padrão, a quantidade de palavras geradas à espera de teste é sempre de 100.000.
		"""
		for num in range(0,self.char_range):
			if not self.finish:
				wordlist_gen = itertools.product(self.char_list,repeat=num)
				id_pos = 0
				for word in wordlist_gen:
					if not self.finish:
						while ((self.word_generated-self.word_tested)>limit):
							time.sleep(0.1)
						word_gen = "".join(word)
						if (len(word_gen)>0):
							self.wordlist[id_pos].append(word_gen)
							self.word_generated += 1
						if (id_pos==len(self.wordlist)-1):
							id_pos = 0
						else:
							id_pos += 1
					else:
						break
			else:
				break

	def TestadorHash(self,thread_id,*args,**kwargs):
		"""
		Esta função é projetada para ser inicializada várias vezes em diversas threads. Sua tarefa é verificar as palavras agrupadas com base em seu próprio ID, gerar o hash correspondente e verificar em toda a lista de hashes para decifrá-los, adicionando-os à lista de hashes decifrados. O 'thread_id' representa a lista interna que fornecerá as palavras para decifrar. Portanto, é crucial que todas as threads sejam inicializadas corretamente para que todas as palavras sejam testadas, mantendo a otimização e o desempenho do script.

		Exemplo:
		TestadorHash(10)
		Nota: Durante a execução do programa, essa função verificará a lista de palavras de ID 10 (na posição 11) e tentará decifrar os hashes usando essas palavras.
		"""
		while not self.finish:
			try:
				temp_word = self.wordlist[thread_id][0]
				word_hash = self.Word2Hash(temp_word)
				for loc,temp_hash in enumerate(self.hash_list):
					if (word_hash==temp_hash):
						self.hash_cracked.append("'{}':'{}'".format(temp_hash,temp_word))
						self.hash_list.pop(loc)
						if (len(self.hash_list)==0):
							self.finish = 1
					else:
						pass
					self.word_tested += 1
				self.wordlist[thread_id].pop(0)
			except:
				time.sleep(0.25)

	def Crack(self,*args,**kwargs):
		"""
		Crack()
		Após ter instanciado o objeto principal com as informações necessárias para decifrar o hash, esta função será usada para iniciar as threads necessárias para a força bruta.

		Exemplo:
		Crack()
		Nota: Após a execução, é necessário verificar se o retorno foi verdadeiro ou falso. Se for falso, indica que ocorreu algum problema e o programa não funcionará corretamente. Se for verdadeiro, pode-se prosseguir com o programa, sabendo que a força bruta já está em andamento.
		"""
		try:
			_temp_var = Thread(target=self.AgrupadorPalavras).start()
			for thread_num in range(self.threads):
				_temp_var = Thread(target=self.TestadorHash, args=[thread_num]).start()
		except:
			return 0
		else:
			return 1

	def Checker(self,*args,**kwargs):
		"""
		Checker()
		Sendo a funcao final onde se verifica e salva todos os registros e hash crackeados em um arquivo
		externo, e verificando se o programa ja terminou e vem atualizando o usuario do status do processo
		de bruteforce.

		Ex: Checker()
		Obs: Apos executar ele deve retornar apenas verdadeiro, assim tendo retorno apos terminar de crackear
		todos os hash, se ocorrer algum problema ele vai persistir e ficar todo momento verificando e atualizando
		o arquivo externo.
		"""
		HashRegistrado = -1
		InicioCronometro = time.time()
		while True:
			try:
				if (HashRegistrado<len(self.hash_cracked)):
					for idhc,hc in enumerate(self.hash_cracked):
						if (idhc>HashRegistrado):
							TempoAtual = time.time()
							with open("HashCracked.txt","a") as save:
								save.write("[{}]\n".format(hc))
							print("[{}]\n".format(hc))
							HashRegistrado += 1
				if (self.finish):
					TempoAtual = time.time()
					for hc in self.hash_cracked:
						print("[{}][{}]".format(hc,(TempoAtual-InicioCronometro)))
					return 1
			except:
				pass
			finally:
				time.sleep(1)
				os.system(command_clear)
		
