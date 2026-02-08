# 🔐 Sistema Antidetecção do Zero

**Seu próprio navegador antidetecção profissional construído do zero em Python!**

Sistema completo para gerenciar múltiplos perfis com isolamento real de cookies, fingerprints, sessões e proxies. Ideal para gerenciar contas do Facebook, Instagram, e-commerce, automação e mais.

---

## 🎯 Funcionalidades

### ✨ **Core Features**
- **Isolamento Total** - Cada perfil opera de forma completamente independente
- **Fingerprints Únicos** - Canvas, WebGL, fontes, timezone, resolução customizados
- **Gestão de Perfis** - Crie, edite, delete, exporte e importe perfis facilmente
- **Integração Selenium** - Controle navegadores reais com fingerprints customizados
- **Dashboard Web** - Interface visual moderna para gerenciar perfis
- **Persistência** - Todos os dados salvos em JSON (fácil backup)
- **Zero Dependências Pesadas** - Sistema leve e rápido

### 🎭 **Fingerprints Customizados**
- User-Agent único por perfil
- Resolução de tela customizada
- Timezone e idioma específicos
- Canvas fingerprint randomizado
- WebGL vendor/renderer modificados
- Hardware concurrency personalizado
- Device memory customizado
- Plugins do navegador únicos
- Lista de fontes diferenciada

---

## 📦 Estrutura do Projeto

```
antidetection-system/
│
├── antidetection_browser.py      # Sistema core de gerenciamento
├── selenium_integration.py       # Integração com Selenium/ChromeDriver
├── antidetection_dashboard.html  # Interface web visual
│
├── browser_profiles/             # Diretório de perfis (criado automaticamente)
│   ├── profile1.json
│   ├── profile2.json
│   └── ...
│
└── README.md                     # Este arquivo
```

---

## 🚀 Instalação

### **Requisitos**
- Python 3.8+
- Google Chrome (para Selenium)
- ChromeDriver (para Selenium)

### **Passo 1: Instalar Python (se necessário)**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Windows
# Baixe em: https://www.python.org/downloads/

# Mac
brew install python3
```

### **Passo 2: Instalar Selenium (opcional, para automação)**
```bash
pip install selenium --break-system-packages
```

### **Passo 3: Instalar ChromeDriver**
```bash
# Opção 1: Baixar manualmente
# Acesse: https://chromedriver.chromium.org/downloads
# Baixe a versão correspondente ao seu Chrome
# Adicione ao PATH

# Opção 2: Usar webdriver-manager
pip install webdriver-manager --break-system-packages
```

---

## 💻 Como Usar

### **Opção 1: Interface Web (Recomendado para iniciantes)**

1. Abra o arquivo `antidetection_dashboard.html` no navegador
2. Clique em "CRIAR PERFIL"
3. Preencha os dados e crie quantos perfis precisar
4. Use os botões para:
   - 🔄 Renovar fingerprint
   - 💾 Exportar perfil
   - 🗑️ Deletar perfil

**Recursos do Dashboard:**
- Criação visual de perfis
- Visualização de fingerprints
- Exportação/Importação
- Gerenciamento completo

### **Opção 2: Python CLI**

```python
from antidetection_browser import AntidetectionBrowser

# Inicializa o sistema
browser = AntidetectionBrowser()

# Cria um perfil
profile = browser.create_profile(
    name="Facebook Conta 1",
    proxy={
        "host": "proxy.example.com",
        "port": 8080,
        "username": "user",
        "password": "pass"
    }
)

print(f"Perfil criado: {profile.profile_id}")
print(f"User-Agent: {profile.fingerprint['user_agent']}")
print(f"Resolução: {profile.fingerprint['screen_resolution']}")

# Lista todos os perfis
profiles = browser.list_profiles()
for p in profiles:
    print(f"- {p.name} ({p.profile_id})")

# Exporta um perfil
browser.export_profile(profile.profile_id, "meu_perfil.json")

# Deleta um perfil
browser.delete_profile(profile.profile_id)
```

### **Opção 3: Com Selenium (Automação Real)**

```python
from antidetection_browser import AntidetectionBrowser
from selenium_integration import AntidetectionSelenium

# Cria perfil
browser = AntidetectionBrowser()
profile = browser.create_profile("Teste Automação")

# Inicia navegador real com fingerprint
selenium = AntidetectionSelenium()
driver = selenium.launch_browser(
    profile_id=profile.profile_id,
    fingerprint=profile.fingerprint,
    proxy=profile.proxy
)

# Navega para o Facebook
driver.get("https://www.facebook.com")

# Seu código de automação aqui...
# driver.find_element(...)

# Fecha navegador
selenium.close_browser(profile.profile_id)
```

---

## 🧪 Testando o Sistema

### **Teste de Fingerprint**

Visite estes sites para verificar se o fingerprint está customizado:

1. **CreepJS** - https://abrahamjuliot.github.io/creepjs/
   - Mostra todos os detalhes do fingerprint
   
2. **PixelScan** - https://pixelscan.net/
   - Verifica detecção de bot
   
3. **Sannysoft** - https://bot.sannysoft.com/
   - Testa se é detectado como bot

4. **BrowserLeaks** - https://browserleaks.com/canvas
   - Testa canvas fingerprinting

### **Teste Rápido**

```bash
# Execute o sistema básico
python3 antidetection_browser.py

# Execute o teste Selenium (descomente o código primeiro)
python3 selenium_integration.py
```

---

## 🎯 Casos de Uso

### **1. Gerenciamento de Múltiplas Contas Facebook**
```python
browser = AntidetectionBrowser()

# Cria 10 perfis para Facebook
for i in range(1, 11):
    profile = browser.create_profile(
        name=f"Facebook Conta {i}",
        proxy={
            "host": f"proxy{i}.example.com",
            "port": 8080
        }
    )
    print(f"✅ Perfil {i} criado com sucesso!")
```

### **2. E-commerce / Arbitragem**
```python
# Perfil para cada marketplace
perfis_mercado = ["Amazon BR", "Mercado Livre", "Shopee", "AliExpress"]

for mercado in perfis_mercado:
    profile = browser.create_profile(
        name=mercado,
        proxy={"host": "proxy-br.com", "port": 8080}
    )
```

### **3. Marketing Digital / SMM**
```python
redes_sociais = ["Instagram 1", "Instagram 2", "Twitter 1", "LinkedIn"]

for rede in redes_sociais:
    browser.create_profile(name=rede)
```

---

## 🔧 Configuração Avançada

### **Customizar Fingerprints Manualmente**

```python
from antidetection_browser import FingerprintGenerator

# Gera fingerprint customizado
fingerprint = FingerprintGenerator.generate()

# Modifica manualmente
fingerprint['user_agent'] = "Meu User-Agent Customizado"
fingerprint['screen_resolution']['width'] = 1920
fingerprint['screen_resolution']['height'] = 1080
fingerprint['timezone'] = "America/Sao_Paulo"
fingerprint['language'] = "pt-BR,pt;q=0.9"

# Cria perfil com fingerprint customizado
from antidetection_browser import BrowserProfile
profile = BrowserProfile(
    profile_id="custom123",
    name="Perfil Custom",
    fingerprint=fingerprint
)
```

### **Rotação Automática de Proxies**

```python
proxies = [
    {"host": "proxy1.com", "port": 8080},
    {"host": "proxy2.com", "port": 8080},
    {"host": "proxy3.com", "port": 8080}
]

import random

for i in range(10):
    proxy = random.choice(proxies)
    profile = browser.create_profile(
        name=f"Perfil {i}",
        proxy=proxy
    )
```

---

## 📊 Comparação com Soluções Comerciais

| Recurso | Seu Sistema | Multilogin | GoLogin | AdsPower |
|---------|-------------|------------|---------|----------|
| **Preço** | 🆓 GRÁTIS | €99/mês | $24/mês | $0-9/mês |
| **Perfis Ilimitados** | ✅ Sim | ❌ Limitado | ❌ Limitado | ❌ Limitado |
| **Código Aberto** | ✅ Sim | ❌ Não | ❌ Não | ❌ Não |
| **Customizável** | ✅ 100% | ❌ Não | ❌ Não | ❌ Não |
| **Auto-hospedado** | ✅ Sim | ❌ Não | ❌ Não | ❌ Não |
| **Sem Limites** | ✅ Sim | ❌ Não | ❌ Não | ❌ Não |

---

## ⚠️ Avisos Importantes

### **Uso Ético**
- Este sistema é para fins educacionais e legítimos
- Respeite os Termos de Serviço das plataformas
- Não use para atividades ilegais ou antiéticas
- Você é responsável pelo uso do software

### **Limitações Técnicas**
- Requer conhecimento básico de Python
- Selenium precisa de ChromeDriver configurado
- Alguns sites avançados podem detectar automação
- Proxies de qualidade são essenciais para privacidade real

### **Segurança**
- Nunca compartilhe seus perfis exportados
- Use proxies confiáveis
- Mantenha backups dos seus perfis
- Não armazene senhas nos perfis

---

## 🛠️ Troubleshooting

### **"ChromeDriver não encontrado"**
```bash
# Baixe ChromeDriver em:
# https://chromedriver.chromium.org/downloads
# Adicione ao PATH do sistema
```

### **"Selenium não instalado"**
```bash
pip install selenium --break-system-packages
```

### **"Perfis não salvam"**
- Verifique permissões do diretório `browser_profiles/`
- Certifique-se que tem espaço em disco

### **"Navegador detectado como bot"**
- Use proxies residenciais de qualidade
- Adicione delays entre ações
- Simule comportamento humano

---

## 📈 Próximos Passos / Melhorias Futuras

- [ ] API REST para integração externa
- [ ] Suporte a Firefox além de Chrome
- [ ] Rotação automática de proxies
- [ ] Sincronização em nuvem
- [ ] App desktop com PyQt
- [ ] Sistema de equipes e permissões
- [ ] Monitoramento de saúde dos perfis
- [ ] Backup automático
- [ ] Templates de fingerprints por região

---

## 🤝 Contribuindo

Sinta-se livre para:
- Reportar bugs
- Sugerir melhorias
- Fazer fork e modificar
- Compartilhar casos de uso

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.
Use com responsabilidade e ética.

---

## 🎓 Aprenda Mais

### **Recursos Sobre Fingerprinting**
- https://browserleaks.com
- https://amiunique.org
- https://pixelscan.net

### **Documentação Selenium**
- https://selenium-python.readthedocs.io

### **Antidetecção**
- https://github.com/ultrafunkamsterdam/undetected-chromedriver

---

## 💡 Dicas Pro

1. **Use proxies residenciais** - Proxies datacenter são facilmente detectados
2. **Varie os fingerprints** - Não use o mesmo para todas as contas
3. **Simule humanos** - Adicione delays, movimentos de mouse
4. **Rotacione IPs** - Não use o mesmo IP para múltiplas contas
5. **Backup regular** - Exporte seus perfis periodicamente
6. **Teste primeiro** - Verifique no BrowserLeaks antes de usar produção

---

**Feito com ❤️ para a comunidade de desenvolvedores**

🚀 **Bora criar seu império digital com ética e profissionalismo!**
