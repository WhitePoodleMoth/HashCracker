import HC.BFH

def main(*args, **kwards):
	lista_hash = ["fcd6eb393e783a20e3db79db0ef57c49","b845f8a24f6821855a4cba4c5a422416"]
	_hc = HC.BFH.HashCracker(lista_hash,"MD5",10,500,3)
	_hc.Crack()
	if (_hc.Checker()):
		quit()

if __name__=="__main__":
	main()
