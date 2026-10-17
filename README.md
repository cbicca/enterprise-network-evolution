### Enterprise Network Evolution

Este repositório documenta o design, implementação e automação de uma infraestrutura de rede corporativa em constante evolução. O projeto simula o crescimento real de uma empresa de médio a grande porte, progredindo de conceitos fundamentais a arquiteturas modernas de alta disponibilidade, segurança enterprise e NetDevOps. 

### 🛠️ Ambiente de Simulação Nativizada (Linux/Ubuntu)

Diferente das simulações tradicionais, este projeto adota práticas modernas de infraestrutura como software: 

* **Orquestrador:** GNS3 rodando nativamente no Linux Ubuntu.
* **Plataforma de Roteamento:** Containers Docker utilizando a suite de código aberto **FRRouting (FRR)**.
* **Benefício Técnico:** Desempenho nativo com consumo mínimo de recursos através do Kernel Linux, eliminando a dependência de VMs pesadas proprietárias.

### 🏢 Fase 1: O Core da Infraestrutura (Conectividade Matriz-Filial)

A primeira etapa do projeto estabelece a conectividade de tráfego base entre duas localidades geograficamente distantes da corporação (Matriz e Filial). 

### 📋 Escopo Técnico Implementado

* **Endereçamento IP Eficiente:** Segmentação precisa utilizando sub-redes com máscaras personalizadas (/30 e /24).
* **Roteamento Dinâmico:** Implementação do protocolo **OSPF (Open Shortest Path First)** de área única (Área 0) para convergência automática de rotas.
* **Segurança de Gerenciamento:** Acesso centralizado via terminal através do shell de gerenciamento integrado (vtysh).

### 📐 Tabela de Endereçamento IP

DispositivoInterfaceEndereço IPMáscaraFunção
****ROTEADOR-MATRIZ****
eth010.0.0.1/30 (255.255.255.252)Link de Trânsito WAN (Matriz -> Filial)
****ROTEADOR-MATRIZ****
eth1192.168.10.1/24 (255.255.255.0)Gateway da Rede Local (LAN Matriz)
****ROTEADOR-FILIAL****
eth010.0.0.2/30 (255.255.255.252)Link de Trânsito WAN (Filial -> Matriz)
****ROTEADOR-FILIAL****
eth1192.168.20.1/24 (255.255.255.0)Gateway da Rede Local (LAN Filial)

### 🛠️ Desafios Técnicos Superados (Troubleshooting)

Durante o deploy no ecossistema Ubuntu, foram mitigados três gargalos de nível operacional: 

1. **Permissões de Socket Docker:** Ajuste de permissões do arquivo /var/run/docker.sock liberando o controle ao GNS3 Desktop sem privilégios de root.
2. **Isolamento de Console Interativa:** Ajuste do redirecionamento do Telnet para permitir acesso ao tty direto (vtysh) contornando streams de logs infinitos de boot.
3. **Gerenciamento Granular de Daemons:** Ativação explícita do processo background do OSPF (ospfd) através do orquestrador para permitir a inicialização dos pacotes HELLO.

### 🧪 Evidências de Validação

Comunicação convergida com sucesso de ponta a ponta. 

* Comando executado para validação de adjacência: show ip ospf neighbor (Status: FULL).
* Comando executado para checagem de alcançabilidade: ping 192.168.20.1 (100% de sucesso).

### 🚀 Próximas Fases Planejadas

* **Fase 2 (Intermediário):** Redundância de Gateway com HSRP/VRRP, agregação de links (LACP) e primeiros scripts em Python para backup de automação.
* **Fase 3 (Especialista):** Túneis VPN IPsec criptografados, monitoramento avançado com SNMP/Grafana e Provisionamento via Ansible (IaC).
