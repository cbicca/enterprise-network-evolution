import os
import docker

print("⚡ Inicializando a Varredura Automatizada de Infraestrutura...")

try:
    # Conecta no cliente Docker nativo do Ubuntu
    client = docker.from_env()
    
    # Cria a pasta de backups no seu computador caso não exista
    os.makedirs('backups_infra', exist_ok=True)
    
    # Busca por TODOS os containers ativos no seu sistema
    containers = client.containers.list()
    
    roteadores_encontrados = 0

    for container in containers:
        # Filtra apenas os containers que estão rodando a imagem do FRRouting
        if "frrouting/frr" in container.image.tags[0]:
            roteadores_encontrados += 1
            # Limpa o nome do container para usar como nome de arquivo
            nome_limpo = container.name.replace(".", "_")
            
            print(f"📦 Roteador localizado: {container.name} [ID: {container.short_id}]")
            print(f"   ↳ Extraindo running-config...")
            
            # Executa o vtysh e captura as configurações atuais
            resultado = container.exec_run('vtysh -c "show running-config"')
            configuracao = resultado.output.decode('utf-8')
            
            # Salva o arquivo com o nome exato daquele roteador
            caminho_arquivo = f"backups_infra/{nome_limpo}_running_config.txt"
            with open(caminho_arquivo, 'w') as arquivo:
                arquivo.write(configuracao)
                
            print(f"   ✅ Salvo em: {caminho_arquivo}\n")
            
    if roteadores_encontrados == 0:
        print("⚠️ Nenhum roteador baseado em FRRouting foi localizado ativo no GNS3.")
    else:
        print(f"🎉 Sucesso! Backup concluído para os {roteadores_encontrados} roteadores ativos.")

except Exception as erro:
    print(f"❌ Falha crítica na automação: {erro}")

