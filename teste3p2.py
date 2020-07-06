from socket import * 
import platform, psutil, datetime, multiprocessing, os,itertools, time, pickle, threading,sys
# Declarar o valor de serverName
serverName = 'localhost'
# Numero de porta na qual o servidor estara esperando conexoes.
serverPort = int(sys.argv[1])
# Criar o socket. AF_INET e SOCK_STREAM indicam TCP.
serverSocket = socket(AF_INET, SOCK_STREAM)
# Permite encerrar o processo e reutilizar a porta indicada
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Associar o socket a porta escolhida. Primeiro argumento vazio indica
serverSocket.bind(('', serverPort))
# Declarar lista de portas, nesse caso são apensa duas
lista = [12000, 12001]
# Remove a porta que está sendo utilizada pelo próprio processo, para que o processo não envie o lance para si mesmo
lista.remove(serverPort)
# Quantas conexões serão suportadas no servidor
serverSocket.listen()
# Declaração de variáveis globais do programa
lance_atual = 0 
lance_recebido = 0
lance = 0
lance_anterior = 0
j=0
# Função de decisão após o contador zerar
def decisao():
	global lance, lance_atual, lista, lance_anterior
	# Decisão de quem ganhou através dos valores dos lances que os usuários possuem como o seu último 
	# Condição para verificar os valores dos lances de cada processo
	if lance == lance_anterior:
		print("voce não ganhou o leilão no valor de", lance_atual,"\n \n")
		# Comando de saída do programa e voltar ao terminal e deixar uma mensagem
		sys.exit(" abra o programa novamente para que o leilão se reinicie")

	print("leilão encerrado, voce eh o vencedor no valor",lance)
	sys.exit(" abra o programa novamente para que o leilão se reinicie")

def contador():
	global lance, lance_atual,j, temp_encerra
	if j!=1:
		j=1
		while(temp_encerra >= 0):
			print('tempo de encerramento',temp_encerra,'seg \n')
			#se o tempo acabar gera uma mensagem de vencedor e envia var_acaba = -1 para que os outro usuários saibam que o leilão acabou	
			time.sleep(1)
			temp_encerra=temp_encerra-1
		decisao()	
	#tratar os dados recebidos de outros
# Conexao com o servidor

#a = threading.Thread(target=contador,args=(lista,))

def envia_lance(lista):
	global lance_atual, lance, lance_anterior,temp_encerra
	while 1:
		print("o lance está no valor de",lance_atual,"\n")
		lance=int(input("digite um lance  \n"))
		if lance < lance_atual:
			print(" lance não aceito")
		else:	
			lance_atual = lance
			for p in lista:
				# Criacao do socket
				clientSocket = socket(AF_INET, SOCK_STREAM)
				# Conexao com o servidor colocar o remove pra fora da função
				clientSocket.connect((serverName,p))
				# enviando o lance
				clientSocket.send(pickle.dumps(lance))
				# Encerra de SOCKET
				clientSocket.close()
			temp_encerra=5
			contador()
			

def aguardo_de_recebimento_de_lance():
	# Declaração de variávei globais
	global lance, lance_atual, j, lance_recebido, lance_anterior, temp_encerra
	while 1:
		# Aguardar nova conexao
		connectionSocket, addr = serverSocket.accept()
		# Recepcao de dados
		lance_recebido_byte = connectionSocket.recv(1024)
		#encerra a conexão
		connectionSocket.close()
		lance_recebido = pickle.loads(lance_recebido_byte)
		lance_atual = lance_recebido
		n=5
		if lance<=lance_atual:
			lance_anterior = lance
			# começa contador par ao perdedor
		print("o valore recebido é de ",lance_recebido)
	    # Verifica se houve vencedor com var_acaba
	    # Rodar o contador uma única vez
		if(lance_recebido != 0 and j == 0):
			temp_encerra=5
			contador()
			j = j + 1
		print("o lance está no valor de",lance_atual,"\n")
# Implementa o thread de enviar lance
t = threading.Thread(target=envia_lance,args=(lista,))
# Inicia thread de enviar lances
t.start()
aguardo_de_recebimento_de_lance()
t.join()


