#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمان المواقع الشاملة - القائمة التفاعلية
Website Security Scanner - Interactive Menu
"""

import sys
import os
import subprocess
from colorama import Fore, Back, Style, init

init(autoreset=True)

def print_banner():
    """طباعة البانر الرئيسي"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  أداة فحص أمان المواقع الشاملة".center(58) + "║")
    print("║" + "  Website Security Scanner v1.0".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print(f"{Style.RESET_ALL}\n")

def print_menu():
    """طباعة القائمة الرئيسية"""
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}اختر ما تريد:{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}1{Style.RESET_ALL} - فحص موقع ويب")
    print(f"{Fore.CYAN}2{Style.RESET_ALL} - عرض التقارير السابقة")
    print(f"{Fore.CYAN}3{Style.RESET_ALL} - حذف التقارير القديمة")
    print(f"{Fore.CYAN}4{Style.RESET_ALL} - الخروج")
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")

def get_url_input():
    """الحصول على رابط من المستخدم"""
    print(f"{Fore.YELLOW}أدخل رابط الموقع (مثال: google.com):${Style.RESET_ALL} ", end='')
    url = input().strip()
    
    if not url:
        print(f"{Fore.RED}❌ الرابط فارغ! الرجاء المحاولة مرة أخرى.{Style.RESET_ALL}\n")
        return None
    
    return url

def run_scan(url):
    """تشغيل الفحص"""
    print(f"\n{Fore.CYAN}جاري فحص الموقع: {url}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}الرجاء الانتظار...{Style.RESET_ALL}\n")
    
    try:
        subprocess.run(['python3', 'scanner.py', url], check=True)
        print(f"\n{Fore.GREEN}✓ اكتمل الفحص بنجاح!{Style.RESET_ALL}\n")
    except subprocess.CalledProcessError:
        print(f"\n{Fore.RED}❌ حدث خطأ أثناء الفحص{Style.RESET_ALL}\n")
    except FileNotFoundError:
        print(f"{Fore.RED}❌ لم يتم العثور على scanner.py{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}اضغط Enter للعودة للقائمة...{Style.RESET_ALL}")

def list_reports():
    """عرض التقارير المتاحة"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}التقارير المتاحة:{Style.RESET_ALL}\n")
    
    import glob
    reports = glob.glob('report_*.json')
    
    if not reports:
        print(f"{Fore.YELLOW}لا توجد تقارير{Style.RESET_ALL}\n")
    else:
        for i, report in enumerate(reports, 1):
            size = os.path.getsize(report) / 1024
            print(f"{Fore.GREEN}{i}{Style.RESET_ALL} - {report} ({size:.2f} KB)")
        print()
    
    input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")

def delete_reports():
    """حذف التقارير"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}حذف التقارير:{Style.RESET_ALL}\n")
    
    import glob
    reports = glob.glob('report_*.json')
    
    if not reports:
        print(f"{Fore.YELLOW}لا توجد تقارير للحذف{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}سيتم حذف {len(reports)} تقرير{Style.RESET_ALL}\n")
        confirm = input(f"{Fore.YELLOW}هل أنت متأكد؟ (نعم/لا): {Style.RESET_ALL}").strip().lower()
        
        if confirm in ['نعم', 'yes', 'y']:
            for report in reports:
                try:
                    os.remove(report)
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL} تم حذف {report}")
                except Exception as e:
                    print(f"{Fore.RED}❌{Style.RESET_ALL} فشل حذف {report}: {e}")
            print()
        else:
            print(f"{Fore.YELLOW}تم الإلغاء{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}اضغط Enter للعودة...{Style.RESET_ALL}")

def main():
    """البرنامج الرئيسي"""
    while True:
        print_banner()
        print_menu()
        
        choice = input(f"{Fore.CYAN}اختيارك: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            url = get_url_input()
            if url:
                run_scan(url)
        elif choice == '2':
            list_reports()
        elif choice == '3':
            delete_reports()
        elif choice == '4':
            print(f"\n{Fore.GREEN}شكراً لاستخدامك الأداة! 👋{Style.RESET_ALL}\n")
            sys.exit(0)
        else:
            print(f"{Fore.RED}❌ اختيار غير صحيح!{Style.RESET_ALL}\n")
            input(f"{Fore.YELLOW}اضغط Enter للمحاولة مرة أخرى...{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}تم الإيقاف من قبل المستخدم{Style.RESET_ALL}\n")
        sys.exit(0)
