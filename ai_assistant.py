#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة الذكاء الاصطناعي للأمن السيبراني
AI Cybersecurity Assistant
"""

import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

# قاعدة البيانات الضخمة للأمن السيبراني
CYBERSECURITY_DATABASE = {
    'الثغرات الشائعة': {
        'SQL Injection': {
            'الوصف': 'حقن كود SQL في حقول الإدخال',
            'الخطورة': 'حرجة جداً',
            'الأعراض': 'رسائل خطأ غريبة، قاعدة بيانات مكشوفة',
            'الحل': [
                '1. استخدم Prepared Statements',
                '2. تحقق من الإدخال من جانب الخادم',
                '3. استخدم ORM frameworks',
                '4. قيّد صلاحيات قاعدة البيانات',
                '5. استخدم WAF (Web Application Firewall)'
            ],
            'الأدوات': 'SQLMap, Burp Suite, OWASP ZAP',
            'المعايير': 'OWASP Top 10, CWE-89'
        },
        
        'XSS (Cross-Site Scripting)': {
            'الوصف': 'حقن كود JavaScript في الصفحة',
            'الخطورة': 'عالية جداً',
            'الأعراض': 'سرقة كوكيز، إعادة توجيه غير متوقعة',
            'الحل': [
                '1. استخدم Content Security Policy (CSP)',
                '2. قم بتصفية المدخلات',
                '3. استخدم HTML encoding',
                '4. تحديث المكتبات بانتظام',
                '5. استخدم HttpOnly و Secure flags'
            ],
            'الأدوات': 'Burp Suite, OWASP ZAP, Acunetix',
            'المعايير': 'OWASP Top 10, CWE-79'
        },
        
        'CSRF (Cross-Site Request Forgery)': {
            'الوصف': 'إجبار المستخدم على تنفيذ طلب غير مرغوب',
            'الخطورة': 'عالية',
            'الأعراض': 'عمليات غير مرغوبة بدون علم المستخدم',
            'الحل': [
                '1. استخدم CSRF tokens',
                '2. تحقق من Referrer header',
                '3. استخدم SameSite cookie flag',
                '4. اطلب تأكيد للعمليات الحساسة',
                '5. استخدم POST بدلاً من GET'
            ],
            'الأدوات': 'Burp Suite, OWASP ZAP',
            'المعايير': 'OWASP Top 10, CWE-352'
        },
        
        'XXE (XML External Entity)': {
            'الوصف': 'استخدام كيانات XML خارجية خبيثة',
            'الخطورة': 'عالية جداً',
            'الأعراض': 'تسريب البيانات، حرمان الخدمة',
            'الحل': [
                '1. عطّل المعالجات الخارجية',
                '2. تحقق من XML المُدخل',
                '3. استخدم مكتبات آمنة',
                '4. استخدم JSON بدلاً من XML',
                '5. قم بتقييم وتقييد حجم الملفات'
            ],
            'الأدوات': 'Burp Suite, XXEinjector',
            'المعايير': 'OWASP Top 10, CWE-611'
        },
        
        'Broken Authentication': {
            'الوصف': 'ضعف في نظام المصادقة',
            'الخطورة': 'حرجة جداً',
            'الأعراض': 'سرقة حسابات، تخطي المصادقة',
            'الحل': [
                '1. استخدم Multi-Factor Authentication (MFA)',
                '2. استخدم password hashing (bcrypt, Argon2)',
                '3. حدّد محاولات دخول',
                '4. استخدم session management آمن',
                '5. استخدم HTTPS فقط'
            ],
            'الأدوات': 'Burp Suite, Hashcat',
            'المعايير': 'OWASP Top 10, CWE-287'
        },
        
        'Sensitive Data Exposure': {
            'الوصف': 'تعريض البيانات الحساسة',
            'الخطورة': 'حرجة جداً',
            'الأعراض': 'معلومات شخصية مكشوفة، أرقام بطاقات',
            'الحل': [
                '1. استخدم HTTPS دائماً',
                '2. قم بتشفير البيانات في الراحة',
                '3. قيّم صلاحيات الوصول',
                '4. احذف البيانات القديمة',
                '5. استخدم TLS 1.2 أو أعلى'
            ],
            'الأدوات': 'OpenSSL, Wireshark, Burp Suite',
            'المعايير': 'OWASP Top 10, CWE-327'
        },
        
        'Security Misconfiguration': {
            'الوصف': 'إعدادات أمان ضعيفة',
            'الخطورة': 'عالية',
            'الأعراض': 'ملفات إعدادات مكشوفة، خدمات غير آمنة',
            'الحل': [
                '1. ثبّت التصحيحات الأمنية بانتظام',
                '2. أغلق المنافذ غير الضرورية',
                '3. احذف الحسابات الافتراضية',
                '4. استخدم HTTPS فقط',
                '5. قم بتقسيم الشبكات'
            ],
            'الأدوات': 'Nessus, OpenVAS, Qualys',
            'المعايير': 'OWASP Top 10, CWE-16'
        },
        
        'Insecure Deserialization': {
            'الوصف': 'معالجة غير آمنة للبيانات المسلسلة',
            'الخطورة': 'حرجة جداً',
            'الأعراض': 'تنفيذ كود بعيد، تسريب البيانات',
            'الحل': [
                '1. لا تستخدم serialization للبيانات الموثوقة',
                '2. تحقق من البيانات المُدخلة',
                '3. استخدم مكتبات آمنة',
                '4. استخدم JSON بدلاً من binary formats',
                '5. قم بالتوقيع الرقمي للبيانات'
            ],
            'الأدوات': 'ysoserial, Burp Suite',
            'ا��معايير': 'OWASP Top 10, CWE-502'
        },
        
        'Broken Access Control': {
            'الوصف': 'ضعف في التحكم بالوصول',
            'الخطورة': 'حرجة جداً',
            'الأعراض': 'وصول غير مصرح، تجاوز الصلاحيات',
            'الحل': [
                '1. استخدم Role-Based Access Control (RBAC)',
                '2. تحقق من الصلاحيات على جميع الطلبات',
                '3. استخدم Zero Trust model',
                '4. سجّل محاولات الوصول المرفوضة',
                '5. قيّم الصلاحيات بانتظام'
            ],
            'الأدوات': 'Burp Suite, OWASP ZAP',
            'المعايير': 'OWASP Top 10, CWE-284'
        },
    },
    
    'الهجمات الشهيرة': {
        'DDoS (Distributed Denial of Service)': {
            'الوصف': 'هجوم لشل الخدمة من عدة مصادر',
            'الخطورة': 'عالية جداً',
            'الأنواع': 'Volumetric, Protocol, Application layer',
            'الحماية': [
                '1. استخدم DDoS mitigation services',
                '2. قلّل حجم الاستجابة',
                '3. استخدم rate limiting',
                '4. قيّد عرض النطاق الترددي',
                '5. استخدم Web Application Firewall'
            ],
            'الأدوات': 'CloudFlare, AWS Shield, Akamai'
        },
        
        'Man-in-the-Middle (MitM)': {
            'الوصف': 'اعتراض الاتصالات بين طرفين',
            'الخطورة': 'حرجة جداً',
            'الأنواع': 'ARP Spoofing, DNS Spoofing, SSL Stripping',
            'الحماية': [
                '1. استخدم HTTPS/TLS',
                '2. تحقق من شهادات SSL',
                '3. استخدم VPN',
                '4. استخدم Certificate Pinning',
                '5. تفعيل HSTS'
            ],
            'الأدوات': 'Wireshark, Mitmproxy, Burp Suite'
        },
        
        'Brute Force': {
            'الوصف': 'محاولات متكررة للتخمين',
            'الخطورة': 'عالية',
            'الأنواع': 'Password, API key, PIN',
            'الحماية': [
                '1. استخدم strong passwords',
                '2. حدّد محاولات الدخول',
                '3. استخدم MFA',
                '4. استخدم CAPTCHAs',
                '5. استخدم account lockout'
            ],
            'الأدوات': 'Hashcat, John the Ripper'
        },
        
        'Phishing': {
            'الوصف': 'خداع المستخدمين للحصول على بيانات',
            'الخطورة': 'عالية',
            'الأنواع': 'Email, SMS, Social Media',
            'الحماية': [
                '1. درّب الموظفين',
                '2. استخدم email filters',
                '3. تحقق من sender domains',
                '4. استخدم MFA',
                '5. فعّل SPF, DKIM, DMARC'
            ],
            'الأدوات': 'Gophish, SpamTitan'
        },
    },
    
    'أدوات الأمن السيبراني': {
        'Burp Suite': {
            'النوع': 'Web Security Testing',
            'الاستخدام': 'اختبار الثغرات في تطبيقات الويب',
            'الإصدار': 'Community, Professional, Enterprise',
            'الرابط': 'https://portswigger.net/burp'
        },
        
        'OWASP ZAP': {
            'النوع': 'Web Security Scanner',
            'الاستخدام': 'فحص تطبيقات الويب تلقائياً',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'https://www.zaproxy.org/'
        },
        
        'Metasploit': {
            'النوع': 'Penetration Testing',
            'الاستخدام': 'اختبار الثغرات واستغلالها',
            'الإصدار': 'Community, Pro',
            'الرابط': 'https://www.metasploit.com/'
        },
        
        'Nmap': {
            'النوع': 'Network Scanning',
            'الاستخدام': 'مسح المنافذ والخدمات',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'https://nmap.org/'
        },
        
        'Wireshark': {
            'النوع': 'Network Analysis',
            'الاستخدام': 'تحليل حركة الشبكة',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'https://www.wireshark.org/'
        },
        
        'Hashcat': {
            'النوع': 'Password Cracking',
            'الاستخدام': 'كسر كلمات المرور',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'https://hashcat.net/'
        },
        
        'SQLMap': {
            'النوع': 'SQL Injection Testing',
            'الاستخدام': 'اختبار ثغرات SQL Injection',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'http://sqlmap.org/'
        },
        
        'Nikto': {
            'النوع': 'Web Server Scanner',
            'الاستخدام': 'فحص خوادم الويب',
            'الإصدار': 'مفتوح المصدر',
            'الرابط': 'https://cirt.net/Nikto2'
        },
    },
    
    'المعايير والإطارات': {
        'OWASP Top 10': {
            'الوصف': 'أخطر 10 ثغرات في تطبيقات الويب',
            'الإصدار': '2021',
            'المحتوى': [
                '1. Broken Access Control',
                '2. Cryptographic Failures',
                '3. Injection',
                '4. Insecure Design',
                '5. Security Misconfiguration',
                '6. Vulnerable Components',
                '7. Authentication Failures',
                '8. Software and Data Integrity',
                '9. Logging Failures',
                '10. SSRF'
            ]
        },
        
        'NIST Cybersecurity Framework': {
            'الوصف': 'إطار عمل الأمن السيبراني',
            'الإصدار': '1.1',
            'المحاور': [
                '1. Identify (تحديد)',
                '2. Protect (حماية)',
                '3. Detect (كشف)',
                '4. Respond (الاستجابة)',
                '5. Recover (الاستعادة)'
            ]
        },
        
        'ISO 27001': {
            'الوصف': 'معيار إدارة أمان المعلومات',
            'الإصدار': '2022',
            'المميزات': [
                '1. إدارة المخاطر',
                '2. السياسات والإجراءات',
                '3. الامتثال القانوني',
                '4. التدقيق والمراقبة',
                '5. إدارة الحوادث'
            ]
        },
    },
    
    'نصائح الأمان': {
        'كلمات المرور': [
            '✓ استخدم 12+ حرف',
            '✓ اخلط بين أحرف كبيرة وصغيرة',
            '✓ أضف أرقام ورموز',
            '✓ تجنب كلمات قاموسية',
            '✓ لا تستخدم معلومات شخصية',
            '✓ غيّر كلمات المرور بانتظام'
        ],
        
        'الحسابات': [
            '✓ فعّل MFA على جميع الحسابات',
            '✓ استخدم مدير كلمات مرور',
            '✓ راقب نشاط الحساب',
            '✓ احذف الحسابات غير المستخدمة',
            '✓ استخدم recovery options آمنة'
        ],
        
        'الشبكات': [
            '✓ استخدم firewall',
            '✓ حدّث أنظمة التشغيل',
            '✓ استخدم VPN',
            '✓ فعّل HTTPS فقط',
            '✓ نظّف السجلات بانتظام'
        ],
    },
    
    'المورد والدورات': {
        'مواقع التعلم': [
            'HackTheBox - اختبر مهاراتك العملية',
            'TryHackMe - دورات تفاعلية للأمان',
            'Coursera - دورات جامعية',
            'edX - شهادات معترف بها',
            'Cybrary - دورات مجانية'
        ],
        
        'المجتمعات': [
            'OWASP - مجتمع الأمان',
            'Reddit r/cybersecurity',
            'Twitter security community',
            'GitHub security projects',
            'Stack Overflow'
        ],
    }
}

class AISecurityAssistant:
    def __init__(self):
        self.db = CYBERSECURITY_DATABASE
    
    def print_menu(self):
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🤖 مساعد الأمن السيبراني الذكي{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}الفئات المتاحة:{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}1{Style.RESET_ALL} - الثغرات الشائعة والحلول")
        print(f"{Fore.CYAN}2{Style.RESET_ALL} - الهجمات الشهيرة والحماية")
        print(f"{Fore.CYAN}3{Style.RESET_ALL} - أدوات الأمن السيبراني")
        print(f"{Fore.CYAN}4{Style.RESET_ALL} - المعايير والإطارات")
        print(f"{Fore.CYAN}5{Style.RESET_ALL} - نصائح الأمان")
        print(f"{Fore.CYAN}6{Style.RESET_ALL} - المصادر والدورات")
        print(f"{Fore.CYAN}7{Style.RESET_ALL} - البحث الحر")
        print(f"{Fore.CYAN}8{Style.RESET_ALL} - العودة للقائمة الرئيسية")
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    
    def show_vulnerabilities(self):
        print(f"\n{Fore.YELLOW}الثغرات الشائعة:{Style.RESET_ALL}\n")
        for i, vuln in enumerate(self.db['الثغرات الشائعة'].keys(), 1):
            print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {vuln}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}اختر رقم الثغرة: {Style.RESET_ALL}").strip()
            vulns = list(self.db['الثغرات الشائعة'].keys())
            if 1 <= int(choice) <= len(vulns):
                self.show_vulnerability_details(vulns[int(choice)-1])
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_vulnerability_details(self, vuln_name):
        vuln = self.db['الثغرات الشائعة'][vuln_name]
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📌 {vuln_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}الوصف:{Style.RESET_ALL} {vuln['الوصف']}")
        print(f"{Fore.RED}الخطورة:{Style.RESET_ALL} {vuln['الخطورة']}")
        
        if 'الأعراض' in vuln:
            print(f"{Fore.YELLOW}الأعراض:{Style.RESET_ALL} {vuln['الأعراض']}")
        
        if 'الحل' in vuln:
            print(f"\n{Fore.GREEN}الحلول:{Style.RESET_ALL}")
            for solution in vuln['الحل']:
                print(f"  {solution}")
        
        if 'الأدوات' in vuln:
            print(f"\n{Fore.CYAN}الأدوات:{Style.RESET_ALL} {vuln['الأدوات']}")
        
        if 'المعايير' in vuln:
            print(f"{Fore.CYAN}المعايير:{Style.RESET_ALL} {vuln['المعايير']}")
        
        print()
    
    def show_attacks(self):
        print(f"\n{Fore.YELLOW}الهجمات الشهيرة:{Style.RESET_ALL}\n")
        for i, attack in enumerate(self.db['الهجمات الشهيرة'].keys(), 1):
            print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {attack}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}اختر رقم الهجوم: {Style.RESET_ALL}").strip()
            attacks = list(self.db['الهجمات الشهيرة'].keys())
            if 1 <= int(choice) <= len(attacks):
                self.show_attack_details(attacks[int(choice)-1])
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_attack_details(self, attack_name):
        attack = self.db['الهجمات الشهيرة'][attack_name]
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚔️ {attack_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}الوصف:{Style.RESET_ALL} {attack['الوصف']}")
        print(f"{Fore.RED}الخطورة:{Style.RESET_ALL} {attack['الخطورة']}")
        
        if 'الأنواع' in attack:
            print(f"{Fore.YELLOW}الأنواع:{Style.RESET_ALL} {attack['الأنواع']}")
        
        if 'الحماية' in attack:
            print(f"\n{Fore.GREEN}الحماية:{Style.RESET_ALL}")
            for protection in attack['الحماية']:
                print(f"  {protection}")
        
        if 'الأدوات' in attack:
            print(f"\n{Fore.CYAN}الأدوات:{Style.RESET_ALL} {attack['الأدوات']}")
        
        print()
    
    def show_tools(self):
        print(f"\n{Fore.YELLOW}أدوات الأمن السيبراني:{Style.RESET_ALL}\n")
        for i, tool in enumerate(self.db['أدوات الأمن السيبراني'].keys(), 1):
            print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {tool}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}اختر رقم الأداة: {Style.RESET_ALL}").strip()
            tools = list(self.db['أدوات الأمن السيبراني'].keys())
            if 1 <= int(choice) <= len(tools):
                tool_name = tools[int(choice)-1]
                tool = self.db['أدوات الأمن السيبراني'][tool_name]
                print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}🛠️ {tool_name}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
                
                for key, value in tool.items():
                    print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
                print()
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_frameworks(self):
        print(f"\n{Fore.YELLOW}المعايير والإطارات:{Style.RESET_ALL}\n")
        for i, framework in enumerate(self.db['المعايير والإطارات'].keys(), 1):
            print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {framework}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}اختر رقم الإطار: {Style.RESET_ALL}").strip()
            frameworks = list(self.db['المعايير والإطارات'].keys())
            if 1 <= int(choice) <= len(frameworks):
                framework_name = frameworks[int(choice)-1]
                framework = self.db['المعايير والإطارات'][framework_name]
                print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📋 {framework_name}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
                
                print(f"{Fore.GREEN}الوصف:{Style.RESET_ALL} {framework['الوصف']}")
                print(f"{Fore.YELLOW}الإصدار:{Style.RESET_ALL} {framework['الإصدار']}")
                
                for key, values in framework.items():
                    if key not in ['الوصف', 'الإصدار']:
                        print(f"\n{Fore.GREEN}{key}:{Style.RESET_ALL}")
                        for item in values:
                            print(f"  {item}")
                print()
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_tips(self):
        print(f"\n{Fore.YELLOW}نصائح الأمان:{Style.RESET_ALL}\n")
        for i, category in enumerate(self.db['نصائح الأمان'].keys(), 1):
            print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {category}")
        
        try:
            choice = input(f"\n{Fore.YELLOW}اختر رقم الفئة: {Style.RESET_ALL}").strip()
            categories = list(self.db['نصائح الأمان'].keys())
            if 1 <= int(choice) <= len(categories):
                category_name = categories[int(choice)-1]
                print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 {category_name}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
                
                for tip in self.db['نصائح الأمان'][category_name]:
                    print(f"  {tip}")
                print()
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_resources(self):
        print(f"\n{Fore.YELLOW}المصادر والدورات:{Style.RESET_ALL}\n")
        
        for category, items in self.db['المورد والدورات'].items():
            print(f"\n{Fore.CYAN}{category}:{Style.RESET_ALL}")
            for item in items:
                print(f"  • {item}")
        print()
    
    def free_search(self):
        query = input(f"\n{Fore.YELLOW}ابحث عن موضوع (مثل: SQL Injection): {Style.RESET_ALL}").strip().lower()
        
        results = []
        for category, items in self.db.items():
            if isinstance(items, dict):
                for key, value in items.items():
                    if query in key.lower():
                        results.append((category, key))
        
        if results:
            print(f"\n{Fore.GREEN}وجدنا {len(results)} نتيجة:{Style.RESET_ALL}\n")
            for i, (category, item) in enumerate(results, 1):
                print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {item} (من {category})")
            
            try:
                choice = input(f"\n{Fore.YELLOW}اختر رقم النتيجة: {Style.RESET_ALL}").strip()
                if 1 <= int(choice) <= len(results):
                    category, item = results[int(choice)-1]
                    if category == 'الثغرات الشائعة':
                        self.show_vulnerability_details(item)
                    elif category == 'الهجمات الشهيرة':
                        self.show_attack_details(item)
                else:
                    print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}خطأ في الإدخال{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}لم نجد نتائج تطابق البحث{Style.RESET_ALL}\n")
    
    def run(self):
        while True:
            self.print_menu()
            choice = input(f"{Fore.CYAN}اختيارك: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.show_vulnerabilities()
            elif choice == '2':
                self.show_attacks()
            elif choice == '3':
                self.show_tools()
            elif choice == '4':
                self.show_frameworks()
            elif choice == '5':
                self.show_tips()
            elif choice == '6':
                self.show_resources()
            elif choice == '7':
                self.free_search()
            elif choice == '8':
                return
            else:
                print(f"{Fore.RED}اختيار غير صحيح{Style.RESET_ALL}\n")
            
            input(f"{Fore.YELLOW}اضغط Enter للمتابعة...{Style.RESET_ALL}")
