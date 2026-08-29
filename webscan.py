#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمان المواقع - نسخة مبسطة
Website Security Scanner - Simple Version
"""

import sys
import os
import json
import time
import requests
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

class SimpleScanner:
    def __init__(self, url):
        self.url = self.normalize_url(url)
        self.domain = urlparse(self.url).netloc
        self.issues = []
        
    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def check_ssl(self):
        """فحص SSL"""
        try:
            response = requests.get(self.url, timeout=5, verify=True)
            self.issues.append({'نوع': 'SSL', 'الحالة': 'آمن ✓'})
        except requests.exceptions.SSLError:
            self.issues.append({'نوع': 'SSL', 'الحالة': 'غير آمن ❌'})
        except:
            pass
    
    def check_headers(self):
        """فحص الرؤوس الأمنية"""
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            checks = {
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'X-Frame',
                'X-Content-Type-Options': 'X-Content-Type',
                'Strict-Transport-Security': 'HSTS'
            }
            
            for header, name in checks.items():
                if header in headers:
                    self.issues.append({'نوع': name, 'الحالة': 'موجود ✓'})
                else:
                    self.issues.append({'نوع': name, 'الحالة': 'مفقود ❌'})
        except:
            pass
    
    def check_performance(self):
        """فحص الأداء"""
        try:
            start = time.time()
            response = requests.get(self.url, timeout=10, verify=False)
            response_time = (time.time() - start) * 1000
            
            if response_time < 1000:
                status = f'سريع ✓ ({response_time:.0f}ms)'
            elif response_time < 3000:
                status = f'متوسط ({response_time:.0f}ms)'
            else:
                status = f'بطيء ❌ ({response_time:.0f}ms)'
            
            self.issues.append({'نوع': 'الأداء', 'الحالة': status})
        except:
            pass
    
    def run_scan(self):
        """تشغيل الفحص"""
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}جاري فحص: {self.url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        tests = [
            ('فحص SSL', self.check_ssl),
            ('فحص الرؤوس', self.check_headers),
            ('فحص الأداء', self.check_performance)
        ]
        
        for name, func in tests:
            print(f"{Fore.GREEN}► {name}...{Style.RESET_ALL}")
            func()
            time.sleep(0.5)
        
        self.print_results()
    
    def print_results(self):
        """عرض النتائج"""
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}النتائج:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        for issue in self.issues:
            print(f"{Fore.CYAN}{issue['نوع']:<20}{Style.RESET_ALL} : {issue['الحالة']}")
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        # حفظ التقرير
        report = {
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'results': self.issues
        }
        
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}✓ تم حفظ التقرير: {filename}{Style.RESET_ALL}\n")

def print_banner():
    """البانر الرئيسي"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*48 + "╗")
    print("║" + " "*48 + "║")
    print("║" + "أداة فحص أمان المواقع".center(48) + "║")
    print("║" + "Website Security Scanner".center(48) + "║")
    print("║" + " "*48 + "║")
    print("╚" + "═"*48 + "╝")
    print(f"{Style.RESET_ALL}\n")

def main_menu():
    """القائمة الرئيسية"""
    while True:
        print_banner()
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1{Style.RESET_ALL} - فحص موقع")
        print(f"{Fore.YELLOW}2{Style.RESET_ALL} - عرض آخر تقرير")
        print(f"{Fore.YELLOW}3{Style.RESET_ALL} - خروج")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}اختيارك: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            url = input(f"\n{Fore.YELLOW}أدخل الرابط (مثل: google.com): {Style.RESET_ALL}").strip()
            if url:
                scanner = SimpleScanner(url)
                scanner.run_scan()
                input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ الرابط فارغ!{Style.RESET_ALL}\n")
                input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")
        
        elif choice == '2':
            import glob
            reports = sorted(glob.glob('report_*.json'), reverse=True)
            if reports:
                with open(reports[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"\n{Fore.CYAN}آخر تقرير: {data['timestamp']}{Style.RESET_ALL}\n")
                    for item in data['results']:
                        print(f"{item['نوع']:<20} : {item['الحالة']}")
                    print()
            else:
                print(f"{Fore.YELLOW}لا توجد تقارير بعد{Style.RESET_ALL}\n")
            input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")
        
        elif choice == '3':
            print(f"\n{Fore.GREEN}شكراً لاستخدامك الأداة! 👋{Style.RESET_ALL}\n")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ اختيار غير صحيح!{Style.RESET_ALL}\n")
            input(f"{Fore.YELLOW}اضغط Enter للمحاولة...{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}تم الإيقاف{Style.RESET_ALL}\n")
        sys.exit(0)
