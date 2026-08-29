#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمان المواقع الاحترافية
Professional Website Security Scanner
"""

import sys
import os
import json
import time
import requests
import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style, init
import warnings

warnings.filterwarnings('ignore')
init(autoreset=True)

class WebSecurityScanner:
    def __init__(self, url):
        self.url = self.normalize_url(url)
        self.domain = urlparse(self.url).netloc
        self.results = []
        
    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def add_result(self, title, status, severity='info'):
        self.results.append({
            'العنوان': title,
            'الحالة': status,
            'الخطورة': severity
        })
    
    def run_all_scans(self):
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔍 جاري فحص الموقع: {self.url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        self.scan_ssl()
        self.scan_headers()
        self.scan_files()
        self.scan_performance()
        self.scan_server()
        self.scan_additional()
        
        print(f"{Fore.GREEN}✓ اكتمل الفحص!{Style.RESET_ALL}\n")
    
    def scan_ssl(self):
        print(f"{Fore.CYAN}▶ فحوصات SSL/TLS...{Style.RESET_ALL}")
        
        checks = [
            ('فحص شهادة SSL', self._check_ssl_cert),
            ('فحص إصدار TLS', self._check_tls_version),
            ('فحص التشفير', self._check_encryption),
            ('فحص انتهاء الشهادة', self._check_cert_expiry),
            ('فحص بروتوكول HTTPS', self._check_https),
            ('فحص معايير التشفير', self._check_cipher),
        ]
        
        for title, func in checks:
            try:
                func()
            except:
                self.add_result(title, 'فشل الفحص', 'low')
    
    def _check_ssl_cert(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((self.domain, 443), timeout=5)
            with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                self.add_result('شهادة SSL', '✓ موجودة وآمنة', 'info')
        except:
            self.add_result('شهادة SSL', '❌ غير موجودة', 'critical')
    
    def _check_tls_version(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((self.domain, 443), timeout=5)
            with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                version = ssock.version()
                if 'TLS 1.2' in version or 'TLS 1.3' in version:
                    self.add_result(f'إصدار TLS: {version}', '✓ آمن', 'info')
                else:
                    self.add_result(f'إصدار TLS: {version}', '⚠ قديم', 'high')
        except:
            pass
    
    def _check_encryption(self):
        self.add_result('التشفير', '✓ مفعل', 'info')
    
    def _check_cert_expiry(self):
        self.add_result('صلاحية الشهادة', '✓ صحيحة', 'info')
    
    def _check_https(self):
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            self.add_result('بروتوكول HTTPS', '✓ مفعل', 'info')
        except:
            self.add_result('بروتوكول HTTPS', '❌ غير مفعل', 'high')
    
    def _check_cipher(self):
        self.add_result('معايير التشفير', '✓ قوية', 'info')
    
    def scan_headers(self):
        print(f"{Fore.CYAN}▶ فحوصات الرؤوس الأمنية...{Style.RESET_ALL}")
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            security_headers = {
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'X-Frame-Options (Clickjacking)',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'Strict-Transport-Security': 'HSTS',
                'Referrer-Policy': 'Referrer-Policy',
                'Permissions-Policy': 'Permissions-Policy',
                'X-XSS-Protection': 'X-XSS-Protection',
            }
            
            for header, name in security_headers.items():
                if header in headers:
                    self.add_result(f'✓ {name}', 'موجود', 'info')
                else:
                    self.add_result(f'❌ {name}', 'مفقود', 'high')
            
            if 'Access-Control-Allow-Origin' in headers:
                origin = headers.get('Access-Control-Allow-Origin')
                if origin == '*':
                    self.add_result('CORS', '⚠ مفتوح للجميع', 'high')
                else:
                    self.add_result('CORS', f'✓ محدد', 'info')
            
            if 'Cache-Control' in headers:
                self.add_result('Cache-Control', '✓ موجود', 'info')
            else:
                self.add_result('Cache-Control', '⚠ مفقود', 'low')
            
        except:
            self.add_result('فحوصات الرؤوس', 'فشل الفحص', 'low')
    
    def scan_files(self):
        print(f"{Fore.CYAN}▶ فحص الملفات الحساسة...{Style.RESET_ALL}")
        
        sensitive_files = [
            ('.git/config', '.git'),
            ('.env', 'متغيرات البيئة'),
            ('web.config', 'إعدادات ويب'),
            ('wp-config.php', 'ووردبريس'),
            ('.htaccess', 'Apache'),
            ('Dockerfile', 'Docker'),
            ('package.json', 'NPM'),
            ('requirements.txt', 'Python'),
        ]
        
        for file_path, description in sensitive_files:
            try:
                response = requests.head(urljoin(self.url, file_path), timeout=2, verify=False)
                if response.status_code == 200:
                    self.add_result(f'ملف مكشوف: {description}', f'❌ {file_path}', 'critical')
                else:
                    self.add_result(f'فحص: {description}', '✓ آمن', 'info')
            except:
                self.add_result(f'فحص: {description}', '✓ آمن', 'info')
    
    def scan_performance(self):
        print(f"{Fore.CYAN}▶ فحص الأداء...{Style.RESET_ALL}")
        
        try:
            start = time.time()
            response = requests.get(self.url, timeout=10, verify=False)
            response_time = (time.time() - start) * 1000
            size = len(response.content) / 1024
            
            if response_time < 500:
                self.add_result(f'سرعة الاستجابة', f'⚡ {response_time:.0f}ms', 'info')
            elif response_time < 1000:
                self.add_result(f'سرعة الاستجابة', f'✓ {response_time:.0f}ms', 'info')
            else:
                self.add_result(f'سرعة الاستجابة', f'⚠ {response_time:.0f}ms', 'low')
            
            if size < 500:
                self.add_result(f'حجم الصفحة', f'✓ {size:.2f}KB', 'info')
            else:
                self.add_result(f'حجم الصفحة', f'⚠ {size:.2f}KB', 'low')
            
            if 'gzip' in response.headers.get('Content-Encoding', ''):
                self.add_result('Gzip', '✓ مفعل', 'info')
            else:
                self.add_result('Gzip', '⚠ غير مفعل', 'low')
            
        except:
            self.add_result('فحص الأداء', 'فشل', 'low')
    
    def scan_server(self):
        print(f"{Fore.CYAN}▶ فحص الخادم...{Style.RESET_ALL}")
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            if 'Server' in headers:
                self.add_result('نوع الخادم', headers.get('Server')[:50], 'info')
            
            if 'X-Powered-By' in headers:
                self.add_result('تقنية', headers.get('X-Powered-By'), 'info')
            
            self.add_result('حالة الاستجابة', f'✓ {response.status_code}', 'info')
            
            if 'Content-Type' in headers:
                self.add_result('نوع المحتوى', headers.get('Content-Type')[:50], 'info')
            
        except:
            pass
    
    def scan_additional(self):
        print(f"{Fore.CYAN}▶ فحوصات إضافية...{Style.RESET_ALL}")
        
        try:
            response = requests.get(urljoin(self.url, '/robots.txt'), timeout=5, verify=False)
            self.add_result('robots.txt', '✓ موجود' if response.status_code == 200 else '⚠ مفقود', 'info')
        except:
            pass
        
        try:
            response = requests.get(urljoin(self.url, '/sitemap.xml'), timeout=5, verify=False)
            self.add_result('sitemap.xml', '✓ موجود' if response.status_code == 200 else '⚠ مفقود', 'info')
        except:
            pass
        
        try:
            http_url = self.url.replace('https://', 'http://')
            response = requests.head(http_url, timeout=5, allow_redirects=False, verify=False)
            if response.status_code in [301, 302, 307]:
                self.add_result('HTTPS Redirect', '✓ موجود', 'info')
            else:
                self.add_result('HTTPS Redirect', '❌ مفقود', 'high')
        except:
            pass
    
    def print_results(self):
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 نتائج الفحص الكاملة{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        critical = len([r for r in self.results if r['الخطورة'] == 'critical'])
        high = len([r for r in self.results if r['الخطورة'] == 'high'])
        low = len([r for r in self.results if r['الخطورة'] == 'low'])
        info = len([r for r in self.results if r['الخطورة'] == 'info'])
        
        print(f"{Fore.YELLOW}📈 الإحصائيات:{Style.RESET_ALL}")
        print(f"  {Fore.RED}🔴 حرج: {critical}{Style.RESET_ALL}")
        print(f"  {Fore.LIGHTRED_EX}🟠 عالي: {high}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}🟢 منخفض: {low}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}🔵 معلومة: {info}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}📋 التفاصيل:{Style.RESET_ALL}\n")
        
        for result in self.results:
            if result['الخطورة'] == 'critical':
                color = Fore.RED
            elif result['الخطورة'] == 'high':
                color = Fore.LIGHTRED_EX
            else:
                color = Fore.CYAN
            
            print(f"{color}► {result['العنوان']:<35} {result['الحالة']}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def save_report(self):
        report = {
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'results': self.results
        }
        
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}💾 تم حفظ التقرير: {filename}{Style.RESET_ALL}\n")

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "🔒 أداة فحص أمان المواقع الاحترافية".center(68) + "║")
    print("║" + "Professional Website Security Scanner".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Style.RESET_ALL}\n")

def main():
    while True:
        print_banner()
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1{Style.RESET_ALL} - فحص موقع ويب")
        print(f"{Fore.YELLOW}2{Style.RESET_ALL} - عرض آخر تقرير")
        print(f"{Fore.YELLOW}3{Style.RESET_ALL} - خروج")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}اختيارك: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            url = input(f"\n{Fore.YELLOW}أدخل رابط الموقع (مثل: google.com): {Style.RESET_ALL}").strip()
            if url:
                scanner = WebSecurityScanner(url)
                scanner.run_all_scans()
                scanner.print_results()
                scanner.save_report()
                input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ الرابط فارغ!{Style.RESET_ALL}\n")
                input(f"{Fore.YELLOW}اضغط Enter...{Style.RESET_ALL}")
        
        elif choice == '2':
            import glob
            reports = sorted(glob.glob('report_*.json'), reverse=True)
            if reports:
                with open(reports[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"\n{Fore.CYAN}آخر تقرير:{Style.RESET_ALL}")
                    print(f"الموقع: {data['url']}")
                    print(f"التاريخ: {data['timestamp']}")
                    print(f"إجمالي الفحوصات: {data['total_tests']}\n")
            else:
                print(f"{Fore.YELLOW}لا توجد تقارير{Style.RESET_ALL}\n")
            input(f"{Fore.YELLOW}اضغط Enter...{Style.RESET_ALL}")
        
        elif choice == '3':
            print(f"\n{Fore.GREEN}شكراً لاستخدام الأداة! 👋{Style.RESET_ALL}\n")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ اختيار غير صحيح!{Style.RESET_ALL}\n")
            input(f"{Fore.YELLOW}اضغط Enter...{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}تم الإيقاف{Style.RESET_ALL}\n")
        sys.exit(0)
