### Enterprise Network Evolution

Este repositório documenta o design, implementação e automação de uma infraestrutura de rede corporativa em constante evolução. O projeto simula o crescimento real de uma empresa de médio a grande porte, progredindo de conceitos fundamentais a arquiteturas modernas de alta disponibilidade, segurança enterprise e NetDevOps. 

### 🛠️ Ambiente de Simulação Nativizada (Linux/Ubuntu)

Diferente das simulações tradicionais, este projeto adota práticas modernas de infraestrutura como software: 

* **Orquestrador:** GNS3 rodando nativamente no Linux Ubuntu.
* **Plataforma de Roteamento:** Containers Docker utilizando a suite de código aberto **FRRouting (FRR)**.
* **Motor de Automação:** Python 3 integrado com a **Docker API Client** nativa do Kernel do sistema operacional.

### 🏢 Fase 1: O Core da Infraestrutura (Conectividade Matriz-Filial)

A primeira etapa estabeleceu o tráfego base entre duas localidades geograficamente distantes da corporação (Matriz e Filial) utilizando o protocolo de roteamento dinâmico **OSPF (Open Shortest Path First)** de área única (Área 0). 

### 🤖 Fase 2: Intermediário – Alta Disponibilidade por Contingência e NetDevOps (Automação de Backups)

A empresa cresceu operacionalmente, exigindo uma evolução no design de rede e rotinas técnicas inteligentes para eliminação de falhas humanas na gerência de infraestrutura. 

### 📐 Escopo Técnico e de Contingência Implementado

* **Design de Rotas Flutuantes e Redundância:** Implementação de um cenário de contingência operacional na LAN da Matriz, utilizando rotas estáticas flutuantes com o ROTEADOR-MATRIZ-01 (192.168.10.1) atuando como gateway prioritário de dados e o ROTEADOR-MATRIZ-02 (192.168.10.2) mapeado como nó de backup e balanceamento de tráfego local.
* **Ambiente Virtualizado Isolado:** Criação de um ambiente estável utilizando python3-venv para gerenciar as bibliotecas e dependências de automação de redes no host.

### 🐍 Automação NetDevOps: Script de Backup Dinâmico

Para mitigar os riscos de indisponibilidade de servidores tradicionais de SSH dentro de imagens ultra-enxutas e focar em agilidade de microsserviços, foi desenvolvido o script backup_redes.py baseado na biblioteca oficial docker. 

O código realiza uma **varredura dinâmica** no ecossistema do host Ubuntu, localizando de forma automatizada todas as instâncias de roteadores ativos do fabricante FRRouting e extraindo suas configurações com comandos em segundo plano através do interpretador nativo de rede (vtysh). 

#### Código Fonte de Automação: backup_redes.py

python

import os
import docker

try:
    client = docker.from_env()
    os.makedirs('backups_infra', exist_ok=True)
    containers = client.containers.list()
    roteadores_encontrados = 0

    for container in containers:
        if "frrouting/frr" in container.image.tags:
            roteadores_encontrados += 1
            nome_limpo = container.name.replace(".", "_")
            resultado = container.exec_run('vtysh -c "show running-config"')
            configuracao = resultado.output.decode('utf-8')
            
            with open(f"backups_infra/{nome_limpo}_running_config.txt", 'w') as arquivo:
                arquivo.write(configuracao)
                
    print(f"🎉 Sucesso! Backup concluído para {roteadores_encontrados} roteadores.")
except Exception as erro:
    print(f"❌ Falha crítica: {erro}")

Use o código com cuidado.

### 🛠️ Desafios Técnicos Superados (Troubleshooting)

Durante o deploy desta etapa no ecossistema Ubuntu, foram solucionados dois gargalos cruciais: 

1. **Ambientes Externamente Gerenciados (PEP 668):** Tratamento do bloqueio global de instalação de pacotes Python no Ubuntu recente, implementando o uso correto de ambientes virtuais isolados (venv).
2. **Abstração Base Alpine Linux:** Adaptação da lógica de provisionamento de usuários e portas após constatação de que imagens enxutas e otimizadas de containers FRR não possuem pacotes tradicionais como useradd e servidores SSH de escuta padrão. A barreira foi contornada acionando chamadas sistêmicas seguras via Docker Engine API.

### 🚀 Próximas Fases Planejadas

* **Fase 3 (Especialista):** Conexão segura WAN criptografada via túneis VPN IPsec Site-to-Site e Provisionamento de Infraestrutura como Código de larga escala através de Playbooks do Ansible (IaC).
