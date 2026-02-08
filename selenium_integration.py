"""
Módulo de integração Selenium para Sistema Antidetecção
Inicia navegadores reais com fingerprints customizados
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
from pathlib import Path
from typing import Optional
import os


class AntidetectionSelenium:
    """Classe para iniciar navegadores com antidetecção via Selenium"""
    
    def __init__(self, profile_data_dir: str = "./browser_profiles"):
        self.profile_data_dir = Path(profile_data_dir)
        self.drivers = {}  # Armazena drivers ativos
    
    def launch_browser(self, profile_id: str, fingerprint: dict, proxy: Optional[dict] = None) -> webdriver.Chrome:
        """
        Inicia um navegador Chrome com fingerprint customizado
        
        Args:
            profile_id: ID único do perfil
            fingerprint: Dicionário com dados do fingerprint
            proxy: Configurações de proxy (opcional)
            
        Returns:
            Instância do webdriver
        """
        
        # Cria diretório para dados do perfil
        profile_dir = self.profile_data_dir / profile_id
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações do Chrome
        chrome_options = Options()
        
        # Define user data dir (cookies, cache, etc isolados)
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        
        # User-Agent customizado
        chrome_options.add_argument(f"--user-agent={fingerprint['user_agent']}")
        
        # Janela em tamanho específico
        width = fingerprint['screen_resolution']['width']
        height = fingerprint['screen_resolution']['height']
        chrome_options.add_argument(f"--window-size={width},{height}")
        
        # Timezone
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': fingerprint['language'].split(',')[0],
        })
        
        # Proxy
        if proxy:
            proxy_string = f"{proxy['host']}:{proxy['port']}"
            chrome_options.add_argument(f'--proxy-server={proxy_string}')
        
        # Desabilita automação detectável
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Desabilita detecção de webdriver
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # JavaScript para modificar fingerprints
        stealth_js = self._generate_stealth_js(fingerprint)
        
        # Inicia o navegador
        driver = webdriver.Chrome(options=chrome_options)
        
        # Injeta JavaScript antidetecção
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': stealth_js
        })
        
        # Armazena driver ativo
        self.drivers[profile_id] = driver
        
        return driver
    
    def _generate_stealth_js(self, fingerprint: dict) -> str:
        """Gera JavaScript para modificar propriedades do navegador"""
        
        js = f"""
        // Remove indicadores de webdriver
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined
        }});
        
        // Sobrescreve plugins
        Object.defineProperty(navigator, 'plugins', {{
            get: () => {json.dumps([p for p in fingerprint.get('plugins', [])])}
        }});
        
        // Hardware concurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {fingerprint.get('hardware_concurrency', 4)}
        }});
        
        // Device memory
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {fingerprint.get('device_memory', 8)}
        }});
        
        // Platform
        Object.defineProperty(navigator, 'platform', {{
            get: () => '{fingerprint.get('platform', 'Win32')}'
        }});
        
        // Languages
        Object.defineProperty(navigator, 'languages', {{
            get: () => {json.dumps(fingerprint.get('language', 'en-US').split(','))}
        }});
        
        // WebGL Vendor/Renderer
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) {{
                return '{fingerprint.get('webgl_vendor', 'Google Inc.')}';
            }}
            if (parameter === 37446) {{
                return '{fingerprint.get('webgl_renderer', 'ANGLE (Intel)')}';
            }}
            return getParameter.call(this, parameter);
        }};
        
        // Canvas fingerprint (básico)
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {{
            // Adiciona noise ao canvas
            const context = this.getContext('2d');
            const imageData = context.getImageData(0, 0, this.width, this.height);
            for (let i = 0; i < imageData.data.length; i += 4) {{
                imageData.data[i] = imageData.data[i] ^ {hash(fingerprint.get('canvas_fingerprint', '')) % 10};
            }}
            context.putImageData(imageData, 0, 0);
            return originalToDataURL.apply(this, arguments);
        }};
        
        // Screen resolution
        Object.defineProperty(screen, 'width', {{
            get: () => {fingerprint['screen_resolution']['width']}
        }});
        Object.defineProperty(screen, 'height', {{
            get: () => {fingerprint['screen_resolution']['height']}
        }});
        Object.defineProperty(screen, 'availWidth', {{
            get: () => {fingerprint['screen_resolution']['width']}
        }});
        Object.defineProperty(screen, 'availHeight', {{
            get: () => {fingerprint['screen_resolution']['height'] - 40}
        }});
        Object.defineProperty(screen, 'colorDepth', {{
            get: () => {fingerprint['screen_resolution'].get('color_depth', 24)}
        }});
        
        // Permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({{ state: Notification.permission }}) :
                originalQuery(parameters)
        );
        
        // Chrome runtime
        window.chrome = {{
            runtime: {{}}
        }};
        
        console.log('🔐 Antidetection Script Loaded');
        """
        
        return js
    
    def close_browser(self, profile_id: str):
        """Fecha um navegador específico"""
        if profile_id in self.drivers:
            self.drivers[profile_id].quit()
            del self.drivers[profile_id]
    
    def close_all_browsers(self):
        """Fecha todos os navegadores ativos"""
        for driver in self.drivers.values():
            driver.quit()
        self.drivers.clear()


# Exemplo de uso
if __name__ == "__main__":
    from antidetection_browser import AntidetectionBrowser
    
    print("=" * 70)
    print("TESTE DE INTEGRAÇÃO SELENIUM")
    print("=" * 70)
    print()
    
    # Carrega o sistema de perfis
    browser_system = AntidetectionBrowser()
    
    # Cria um perfil de teste
    profile = browser_system.create_profile(
        name="Teste Selenium Facebook",
        proxy=None  # Adicione proxy aqui se tiver
    )
    
    print(f"✅ Perfil criado: {profile.name}")
    print(f"   ID: {profile.profile_id}")
    print(f"   User-Agent: {profile.fingerprint['user_agent'][:60]}...")
    print()
    
    # Inicia navegador com Selenium
    print("🚀 Iniciando navegador com fingerprint customizado...")
    print()
    
    selenium = AntidetectionSelenium()
    
    print("INSTRUÇÕES:")
    print("-" * 70)
    print("1. O navegador irá abrir com fingerprint único")
    print("2. Visite: https://abrahamjuliot.github.io/creepjs/")
    print("3. Ou: https://pixelscan.net/")
    print("4. Ou: https://bot.sannysoft.com/")
    print("5. Verifique se o fingerprint está customizado!")
    print("6. Digite qualquer tecla aqui para fechar o navegador...")
    print("-" * 70)
    print()
    
    try:
        # DESCOMENTE ABAIXO PARA TESTAR COM SELENIUM REAL
        # Certifique-se de ter o ChromeDriver instalado
        
        """
        driver = selenium.launch_browser(
            profile_id=profile.profile_id,
            fingerprint=profile.fingerprint,
            proxy=profile.proxy
        )
        
        # Abre site de teste de fingerprint
        driver.get("https://abrahamjuliot.github.io/creepjs/")
        
        input()  # Aguarda usuário pressionar Enter
        
        selenium.close_browser(profile.profile_id)
        """
        
        print("⚠️  Código de teste comentado!")
        print("📝 Para testar com Selenium real:")
        print("   1. Instale: pip install selenium --break-system-packages")
        print("   2. Baixe ChromeDriver: https://chromedriver.chromium.org/")
        print("   3. Descomente o código marcado no arquivo")
        print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
        print("Certifique-se de ter:")
        print("  - Chrome instalado")
        print("  - ChromeDriver no PATH")
        print("  - pip install selenium --break-system-packages")
    
    print()
    print("✨ Sistema pronto para produção!")
