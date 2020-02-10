# Messenger
###### disclaimer: padrões e o modo como a informação é apresentada não se tornou uma prioridade, tendo o foco estado na implementação do programa em si.
### Features
1. Add Users 
> Implementado através de um Set, de forma a garantir unicidade entre os Utilizadores. Simplesmente regista o nome de todos os Utilizadores.
2. Log In
> Permite iniciar sessão como um dos Utilizadores registados no Set referido acima

2.1 Seguir Users
>> Uma vez que não é possivel colocar estruturas de dados nested, surgiu a necessidade de criar um Set para cada Utilizador, com os Users que o mesmo segue. Assim, em conjunto com o Set descrito em 1. e através de aperações entre Sets (diferença, interseção) é possível saber dos Users registados, quais não são seguidos por um dado Utilizador.

2.2 Ler Mensagens
>> As mensagens estão armazenadas numa Hash, mais uma vez, uma por utilizador. A key é aumentada no estilo "msg-x", sendo x o numero da respetiva mensagem, sendo esta contagem feita com uma função também do Redis. Desta forma é possível saber a ordem as mensagens enviadas para o sistema.

2.3 Escrever Mensagem
>> Simplesmente adiciona mais uma entrada na dita Hash do respetivo utilizador.

2.4 Log Out
>> Autoexplicativo


3. Sair
> Autoexplicativo
