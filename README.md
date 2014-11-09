# Coletor de dados Escalável

## AVISO

Esse código **não se propõe a ser um código para ser usado em produção**, mas somente uma **referência** pra quem quiser montar sua própria infraestrutura de coleta distribuída de dados.

Esse código tem deficiências no tratamento de erro e muitos trechos estão num formato monolítico.

**LEIA TODA A DOCUMENTAÇÃO COM CALMA**

## Slides da palestra

https://speakerdeck.com/felipecruz/coleta-massiva-de-dados

## Configurações

O primeiro passo é configurar o arquivo `.env` onde devem ficar as informações utilizadas por alguns componentes desse projeto. Veja o que deve ser configurado:

```ini
KEY_NAME=seu@email.net
AWS_ACCESS_KEY=access_key
AWS_SECRET_KEY=secret_key
KEY_PASS=key_pass

REGION=us-east-1
DEFAULT_INSTANCE_ID=ami-9eaa1cf6
INSTANCE_SIZE=m3.medium
DEFAULT_SECURITY_GROUP=default

SSH_USER=ubuntu
PARAMIKO_DEBUG=True

MASTER_IP=ip_ou_dns_publico_master
SINK_IP=ip_ou_dns_publico_sink
```

## Montando o ambiente na nuvem AWS

Se você tiver uma conta no AWS (aws.amazon.com) e tiver configurado o seu arquivo `.env` corretamente os comandos abaixo irão funcionar corretamente. Caso a configuração `REGION` seja alterada, a configuração `DEFAULT_INSTANCE_ID` também deverá. Além disso, você precisará informar o `DEFAULT_SECURITY_GROUP` correto configurado na sua conta e que permita a conexão nas portas utilizadas.

### Montando o Master

```sh
$ python setup_instances.py master
```

Copie o dns público e modifique o arquivo `.env`. Esse passo pode ser automatizado também mas isso fica com você :) Se tudo der certo, você poderá logar via `ssh` na máquina criada e rodar o comando `tail -f master.log` para acompanhar o log do processo master.

### Montando o Sink

```sh
$ python setup_instances.py sink
```

Copie o dns público e modifique o arquivo `.env`. Esse passo pode ser automatizado também mas isso fica com você :) Se tudo der certo, você poderá logar via `ssh` na máquina criada e rodar o comando `tail -f sink.log` para acompanhar o log do processo sink.

### Montando os Workers

```sh
$ python setup_instances.py worers 2
```

O comando acima cria 2 máquinas `workers` que serão os responsáveis por bsucar a informação. O comando `tail -f worker.log` deverá exibir informações sobre o andamento do processo. 

### Tudo funcionou? Como apagar tudo?

**AVISO!!!!!!**

O script `terminate.py` irá destruir todas as máquinas existentes na região configurada no arquivo `.env`. Se você estiver usando esse código de referência com uma região onde possui máquinas de produção ou melhore o script ou destrua as instâncias manualmente pelo console.

## Rodando no ambiente local

As dependências python estão no arquivo `requirements.txt`

Suba os compoentes nessa sequência:

```sh
$ python voe/queue.py
$ python sink.py
$ python worker.py
```

## Perguntas Frequentes (FAQ)

* O programa não pega os preços corretamente?
 * As companhias aéreas vivem mudando a estrutura dos seus sites, portanto, isso é esperado. O ajuste fica por sua conta. Se quiser contribuir de volta fique a vontade :)
* Os componentes não se conectam?
 * Verifique se os "Security Groups" permitem conexões externas nas portas usadas.

## Contato

Qualquer dúvida, sugestão, crítica: `felipecruz [at] loogica.net`

## Licença 

```Domínio Público 2014```
