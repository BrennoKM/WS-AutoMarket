# Warspear-AutoMarket

Esse projeto foi desenvolvido para uso pessoal em um jogo online chamado Warspear, meu objetivo primário foi alcançado e atualizações aqui não estão planejadas. Porém 
minha meta inicialmente era fazer com que o programa funcionasse em segundo plano, mas devido a limitações da biblioteca isso só é possível com ajuda do RDP Wrapper.

No futuro pretendo desenvolver a mesma aplicação com o uso de engenharia reversa, a ideia é obter informações direto da memória e enviar inputs direto pra janela do jogo com a biblioteca Ctypes, 
assim se livrando da dependência de ler capturas de tela e consequentemente tornando o bot mais eficiente e leve computacionalmente.

Minha ideia em deixar esse projeto público é atiçar ideias na mente de quem por ventura chegue aqui. Caso você tenha interesse em colaborar comigo ou possua dúvidas do funcionamento,
entre em contato pelo meu **discord Kobernn**.

## Qual o objetivo da aplicação?
 - Automatizar o processo de venda de itens virtuais.
 - Manter essa automação em execução por tempo inderteminado.
 - Tornar tudo configuravel pra diferentes resoluções de tela.

## Como foi desenvolvido?
 - Utilizei a biblioteca PyAutoGui do Python para desenvolver meu projeto como principal meio de automatizar os processos.
 - Interface gráfica simples e intuitiva feita com a biblioteca Tkinter.

## Como funciona?
O usuário deve configurar a aplicação para sua resolução de tela e salvar capturas de tela individuais dos itens que ele deseja vender. Quando tudo estiver pronto, basta preparar o jogo na tela do mercado e iniciar
o programa para que os itens pre-definidos sejam vendidos automaticamente e repostos conforme a demanda.

## Recursos disponíveis
 - CRUD de itens que podem ser vendidos.
 - CRUD das configurações.
 - Mais de uma variedade de item pode ser vendido simultaneamente de acordo com a demanda individual.
 - Atalhos de teclado (com botão de liga/desliga na interface).

## Como usar
- ### Atalhos
  - **'Esc'** - O bot será interrompido forçadamente caso esteja rodando e também desativará os atalhos.
  - **'L'** - O bot será pausado caso esteja rodando.
  - **'K'** - O bot será iniciado no modo simples.
  - **'O'** - O bot será iniciado no modo contínuo e ficará executando de acordo com o tempo e intervalos definidos.
- ### Atalhos especiais
  - **'Ctrl_r'** - Ativa/desativa os atalhos.
  - **'P'** - Coleta automaticamente o ouro na caixa de correios.
  - **'N'** - O item atual será inserido na lista de venda.
      > Ou seja, quando o bot for iniciado ele irá vender todos os itens da lista de forma que todos sejam vendidos igualmente.
  - **'B'** - Reseta a lista e o item atual será o único.
      > Ou seja, só um tipo item será vendido se houver apenas ele na lista.


## Visão Geral
![image](https://github.com/BrennoKM/WS-AutoMarket/assets/99992197/3af87f23-c01e-4ea2-b8c7-1982abb87711)


