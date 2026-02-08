"""
Sistema Antidetecção do Zero
Navegador com isolamento de perfis, fingerprints customizados e gestão de proxies
"""

import json
import os
import random
import string
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import time

class FingerprintGenerator:
    """Gera fingerprints únicos e realistas para cada perfil"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    ]
    
    SCREEN_RESOLUTIONS = [
        (1920, 1080), (1366, 768), (1440, 900), (1536, 864), (1600, 900),
        (2560, 1440), (1280, 720), (1680, 1050), (1280, 1024), (1920, 1200)
    ]
    
    TIMEZONES = [
        "America/Sao_Paulo", "America/New_York", "Europe/London", 
        "Europe/Paris", "Asia/Tokyo", "Australia/Sydney",
        "America/Los_Angeles", "America/Chicago", "Europe/Berlin"
    ]
    
    LANGUAGES = [
        "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "en-US,en;q=0.9",
        "es-ES,es;q=0.9,en;q=0.8",
        "fr-FR,fr;q=0.9,en;q=0.8",
        "de-DE,de;q=0.9,en;q=0.8"
    ]
    
    PLATFORMS = ["Win32", "MacIntel", "Linux x86_64"]
    
    @staticmethod
    def generate() -> Dict:
        """Gera um fingerprint completo e único"""
        
        width, height = random.choice(FingerprintGenerator.SCREEN_RESOLUTIONS)
        
        fingerprint = {
            "user_agent": random.choice(FingerprintGenerator.USER_AGENTS),
            "screen_resolution": {
                "width": width,
                "height": height,
                "color_depth": 24,
                "pixel_ratio": random.choice([1, 1.25, 1.5, 2])
            },
            "timezone": random.choice(FingerprintGenerator.TIMEZONES),
            "language": random.choice(FingerprintGenerator.LANGUAGES),
            "platform": random.choice(FingerprintGenerator.PLATFORMS),
            "hardware_concurrency": random.choice([2, 4, 6, 8, 12, 16]),
            "device_memory": random.choice([2, 4, 8, 16, 32]),
            "webgl_vendor": random.choice([
                "Google Inc. (NVIDIA)",
                "Google Inc. (Intel)",
                "Google Inc. (AMD)",
                "Apple Inc."
            ]),
            "webgl_renderer": random.choice([
                "ANGLE (NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)",
                "ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
                "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
                "Apple M1"
            ]),
            "canvas_fingerprint": hashlib.md5(str(random.random()).encode()).hexdigest(),
            "webrtc": {
                "enabled": random.choice([True, False]),
                "public_ip": FingerprintGenerator._generate_fake_ip()
            },
            "fonts": FingerprintGenerator._generate_font_list(),
            "plugins": FingerprintGenerator._generate_plugin_list(),
            "do_not_track": random.choice([None, "1"]),
            "cookies_enabled": True,
            "created_at": int(time.time())
        }
        
        return fingerprint
    
    @staticmethod
    def _generate_fake_ip() -> str:
        """Gera um IP fake realista"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    @staticmethod
    def _generate_font_list() -> List[str]:
        """Gera lista realista de fontes"""
        base_fonts = [
            "Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana",
            "Georgia", "Comic Sans MS", "Trebuchet MS", "Arial Black", "Impact"
        ]
        extra_fonts = [
            "Calibri", "Cambria", "Consolas", "Lucida Console", "Tahoma",
            "Segoe UI", "Palatino", "Garamond", "Bookman", "Courier"
        ]
        
        num_fonts = random.randint(30, 80)
        return random.sample(base_fonts + extra_fonts * 5, min(num_fonts, len(base_fonts + extra_fonts * 5)))
    
    @staticmethod
    def _generate_plugin_list() -> List[Dict]:
        """Gera lista de plugins do navegador"""
        plugins = []
        
        if random.random() > 0.5:
            plugins.append({
                "name": "Chrome PDF Plugin",
                "description": "Portable Document Format",
                "filename": "internal-pdf-viewer"
            })
        
        if random.random() > 0.5:
            plugins.append({
                "name": "Chrome PDF Viewer",
                "description": "Portable Document Format",
                "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai"
            })
            
        if random.random() > 0.7:
            plugins.append({
                "name": "Native Client",
                "description": "Native Client Executable",
                "filename": "internal-nacl-plugin"
            })
        
        return plugins


class BrowserProfile:
    """Representa um perfil de navegador isolado"""
    
    def __init__(self, profile_id: str, name: str, fingerprint: Dict, proxy: Optional[Dict] = None):
        self.profile_id = profile_id
        self.name = name
        self.fingerprint = fingerprint
        self.proxy = proxy
        self.cookies = []
        self.local_storage = {}
        self.session_storage = {}
        self.created_at = int(time.time())
        self.last_used = None
        self.notes = ""
        
    def to_dict(self) -> Dict:
        """Converte o perfil para dicionário"""
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "fingerprint": self.fingerprint,
            "proxy": self.proxy,
            "cookies": self.cookies,
            "local_storage": self.local_storage,
            "session_storage": self.session_storage,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "notes": self.notes
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'BrowserProfile':
        """Cria um perfil a partir de dicionário"""
        profile = BrowserProfile(
            profile_id=data["profile_id"],
            name=data["name"],
            fingerprint=data["fingerprint"],
            proxy=data.get("proxy")
        )
        profile.cookies = data.get("cookies", [])
        profile.local_storage = data.get("local_storage", {})
        profile.session_storage = data.get("session_storage", {})
        profile.created_at = data.get("created_at", int(time.time()))
        profile.last_used = data.get("last_used")
        profile.notes = data.get("notes", "")
        return profile


class AntidetectionBrowser:
    """Sistema principal de gerenciamento de navegadores antidetecção"""
    
    def __init__(self, data_dir: str = "./browser_profiles"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.profiles: Dict[str, BrowserProfile] = {}
        self._load_profiles()
    
    def create_profile(self, name: str, proxy: Optional[Dict] = None) -> BrowserProfile:
        """Cria um novo perfil com fingerprint único"""
        
        profile_id = self._generate_profile_id()
        fingerprint = FingerprintGenerator.generate()
        
        profile = BrowserProfile(
            profile_id=profile_id,
            name=name,
            fingerprint=fingerprint,
            proxy=proxy
        )
        
        self.profiles[profile_id] = profile
        self._save_profile(profile)
        
        return profile
    
    def get_profile(self, profile_id: str) -> Optional[BrowserProfile]:
        """Obtém um perfil pelo ID"""
        return self.profiles.get(profile_id)
    
    def list_profiles(self) -> List[BrowserProfile]:
        """Lista todos os perfis"""
        return list(self.profiles.values())
    
    def delete_profile(self, profile_id: str) -> bool:
        """Deleta um perfil"""
        if profile_id in self.profiles:
            profile_file = self.data_dir / f"{profile_id}.json"
            profile_file.unlink(missing_ok=True)
            del self.profiles[profile_id]
            return True
        return False
    
    def update_profile(self, profile_id: str, **kwargs) -> bool:
        """Atualiza dados de um perfil"""
        profile = self.profiles.get(profile_id)
        if not profile:
            return False
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        self._save_profile(profile)
        return True
    
    def regenerate_fingerprint(self, profile_id: str) -> bool:
        """Regenera o fingerprint de um perfil"""
        profile = self.profiles.get(profile_id)
        if not profile:
            return False
        
        profile.fingerprint = FingerprintGenerator.generate()
        self._save_profile(profile)
        return True
    
    def export_profile(self, profile_id: str, export_path: str) -> bool:
        """Exporta um perfil para arquivo"""
        profile = self.profiles.get(profile_id)
        if not profile:
            return False
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def import_profile(self, import_path: str) -> Optional[BrowserProfile]:
        """Importa um perfil de arquivo"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profile = BrowserProfile.from_dict(data)
            self.profiles[profile.profile_id] = profile
            self._save_profile(profile)
            
            return profile
        except Exception as e:
            print(f"Erro ao importar perfil: {e}")
            return None
    
    def _generate_profile_id(self) -> str:
        """Gera um ID único para o perfil"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    
    def _save_profile(self, profile: BrowserProfile):
        """Salva um perfil em disco"""
        profile_file = self.data_dir / f"{profile.profile_id}.json"
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)
    
    def _load_profiles(self):
        """Carrega todos os perfis do disco"""
        for profile_file in self.data_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                profile = BrowserProfile.from_dict(data)
                self.profiles[profile.profile_id] = profile
            except Exception as e:
                print(f"Erro ao carregar perfil {profile_file}: {e}")


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o sistema
    browser_system = AntidetectionBrowser()
    
    print("=" * 60)
    print("SISTEMA ANTIDETECÇÃO - NAVEGADOR PRÓPRIO")
    print("=" * 60)
    print()
    
    # Cria 5 perfis de exemplo
    print("📋 Criando 5 perfis de exemplo...")
    print()
    
    profiles_created = []
    for i in range(1, 6):
        profile = browser_system.create_profile(
            name=f"Perfil Facebook {i}",
            proxy={
                "host": f"proxy{i}.example.com",
                "port": 8080 + i,
                "username": f"user{i}",
                "password": f"pass{i}"
            }
        )
        profiles_created.append(profile)
        
        print(f"✅ Perfil {i} criado:")
        print(f"   ID: {profile.profile_id}")
        print(f"   Nome: {profile.name}")
        print(f"   User-Agent: {profile.fingerprint['user_agent'][:60]}...")
        print(f"   Resolução: {profile.fingerprint['screen_resolution']['width']}x{profile.fingerprint['screen_resolution']['height']}")
        print(f"   Timezone: {profile.fingerprint['timezone']}")
        print(f"   Idioma: {profile.fingerprint['language'][:20]}...")
        print(f"   Canvas ID: {profile.fingerprint['canvas_fingerprint'][:16]}...")
        print()
    
    # Lista todos os perfis
    print("=" * 60)
    print(f"📊 Total de perfis: {len(browser_system.list_profiles())}")
    print("=" * 60)
    print()
    
    # Exporta um perfil
    if profiles_created:
        export_file = "/home/claude/perfil_exemplo.json"
        browser_system.export_profile(profiles_created[0].profile_id, export_file)
        print(f"💾 Perfil exportado para: {export_file}")
        print()
    
    print("✨ Sistema pronto para uso!")
    print()
    print("Próximos passos:")
    print("1. Integrar com Selenium/Puppeteer")
    print("2. Criar interface web de gerenciamento")
    print("3. Adicionar rotação automática de proxies")
    print("4. Implementar sincronização de cookies")
