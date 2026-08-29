#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مساعد الأمن السيبراني الذكي - نسخة متقدمة
Advanced AI Cybersecurity Assistant
"""

import sys
import os
import json
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

# قاعدة البيانات الضخمة
AI_DATABASE = {
    'الثغرات': {
        'SQL Injection': {
            'الخطورة': '🔴 حرجة جداً',
            'الوصف': 'حقن كود SQL في حقول الإدخال لسرقة البيانات',
            'الأعراض': ['رسائل خطأ من قاعدة البيانات', 'قاعدة بيانات مكشوفة', 'عمليات غير متوقعة'],
            'الحلول': [
                '✓ استخدم Prepared Statements والـ Parameterized Queries',
                '✓ تحقق من الإدخال من جانب الخادم (Server-side validation)',
                '✓ استخدم ORM frameworks (Hibernate, Sequelize)',
                '✓ قيّد صلاحيات قاعدة البيانات (Principle of least privilege)',
                '✓ استخدم WAF (Web Application Firewall)',
                '✓ قم بـ Input sanitization و filtering'
            ],
            'الأدوات': 'SQLMap, Burp Suite, OWASP ZAP, Acunetix',
            'الكود_الآمن': 'استخدم: statement = db.prepare("SELECT * FROM users WHERE id = ?"); statement.setInt(1, userId);',
            'المعايير': 'CWE-89, OWASP A03:2021'
        },
        
        'XSS (Cross-Site Scripting)': {
            'الخطورة': '🟠 عالية جداً',
            'الوصف': 'حقن كود JavaScript في الصفحة لسرقة بيانات المستخدمين',
            'الأعراض': ['سرقة الـ Cookies', 'إعادة توجيه خطيرة', 'تسجيل الضغطات'],
            'الحلول': [
                '✓ استخدم Content Security Policy (CSP)',
                '✓ قم بـ HTML encoding للمدخلات',
                '✓ استخدم attribute encoding',
                '✓ استخدم JavaScript encoding',
                '✓ فعّل HttpOnly و Secure flags على الـ Cookies',
                '✓ تحديث المكتبات والـ frameworks بانتظام'
            ],
            'الأدوات': 'Burp Suite, OWASP ZAP, BeEF',
            'الكود_الآمن': 'استخدم: textContent بدلاً من innerHTML',
            'المعايير': 'CWE-79, OWASP A07:2021'
        },
        
        'CSRF': {
            'الخطورة': '🟠 عالية',
            'الوصف': 'إجبار المستخدم على تنفيذ طلب غير مرغوب',
            'الأعراض': ['عمليات مالية غير مرغوبة', 'تغيير كلمة المرور', 'حذف البيانات'],
            'الحلول': [
                '✓ استخدم CSRF tokens في كل نموذج',
                '✓ تحقق من Referrer header',
                '✓ استخدم SameSite cookie attribute',
                '✓ اطلب تأكيد للعمليات الحساسة',
                '✓ استخدم POST/PUT/DELETE بدلاً من GET',
                '✓ استخدم HTTP headers للتحقق'
            ],
            'الأدوات': 'Burp Suite, OWASP ZAP',
            'الكود_الآمن': 'أضف token في HTML: <input type="hidden" name="csrf_token" value="...">',
            'المعايير': 'CWE-352, OWASP A01:2021'
        },
        
        'Broken Authentication': {
            'الخطورة': '🔴 حرجة جداً',
            'الوصف': 'ضعف في نظام المصادقة والتحقق من الهوية',
            'الأعراض': ['سرقة الحسابات', 'تسجيل دخول بدون كلمة مرور', 'جلسات ضعيفة'],
            'الحلول': [
                '✓ استخدم Multi-Factor Authentication (MFA/2FA)',
                '✓ استخدم password hashing قوي (bcrypt, Argon2)',
                '✓ حدّد محاولات الدخول (Rate limiting)',
                '✓ استخدم session management آمن',
                '✓ استخدم HTTPS فقط',
                '✓ استخدم secure session cookies'
            ],
            'الأدوات': 'Hashcat, John the Ripper, Burp Suite',
            'الكود_الآمن': 'const hashedPassword = await bcrypt.hash(password, 10);',
            'المعايير': 'CWE-287, OWASP A07:2021'
        },
        
        'Sensitive Data Exposure': {
            'الخطورة': '🔴 حرجة جداً',
            'الوصف': 'تعريض البيانات الحساسة مثل الأرقام والكلمات المرورية',
            'الأعراض': ['بيانات شخصية مكشوفة', 'أرقام بطاقات ائتمان', 'كلمات مرور مرئية'],
            'الحلول': [
                '✓ استخدم HTTPS/TLS 1.2 أو أعلى دائماً',
                '✓ قم بتشفير البيانات في الراحة (Encryption at rest)',
                '✓ قم بتشفير البيانات أثناء النقل (Encryption in transit)',
                '✓ قيّم صلاحيات الوصول بشكل صارم',
                '✓ احذف البيانات القديمة والمؤقتة',
                '✓ استخدم مفاتيح التشفير القوية'
            ],
            'الأدوات': 'OpenSSL, Wireshark, Burp Suite',
            'الكود_الآمن': 'استخدم AES-256 للتشفير: from cryptography.fernet import Fernet',
            'المعايير': 'CWE-327, OWASP A02:2021'
        },
        
        'XXE (XML External Entity)': {
            'الخطورة': '🔴 حرجة جداً',
            'الوصف': 'استخدام كيانات XML خارجية لسرقة البيانات',
            'الأعراض': ['تسريب ملفات النظام', 'هجمات SSRF', 'حرمان الخدمة'],
            'الحلول': [
                '✓ عطّل DTD (Document Type Definition)',
                '✓ عطّل المعالجات الخارجية في مكتبات XML',
                '✓ تحقق من XML المُدخل بعناية',
                '✓ استخدم مكتبات XML آمنة',
                '✓ استخدم JSON بدلاً من XML عند الإمكان',
                '✓ قم بالتحقق من حجم الملفات'
            ],
            'الأدوات': 'XXEinjector, Burp Suite',
            'الكود_الآمن': 'عطّل XXE: parser.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)',
            'المعايير': 'CWE-611, OWASP A05:2021'
        },
        
        'Security Misconfiguration': {
            'الخطورة': '🟠 عالية',
            'الوصف': 'إعدادات أمان ضعيفة وافتراضية خطيرة',
            'الأعراض': ['ملفات إعدادات مكشوفة', 'خدمات غير ضرورية مفعّلة', 'صلاحيات افتراضية'],
            'الحلول': [
                '✓ ثبّت التصحيحات الأمنية بانتظام (Patch management)',
                '✓ أغلق المنافذ والخدمات غير الضرورية',
                '✓ احذف الحسابات والكلمات المرورية الافتراضية',
                '✓ استخدم HTTPS فقط',
                '✓ قيّم التكوينات الأمنية بشكل دوري',
                '✓ استخدم security headers'
            ],
            'الأدوات': 'Nessus, OpenVAS, Qualys',
            'الكود_الآمن': 'أضف headers: X-Frame-Options, X-Content-Type-Options, CSP',
            'المعايير': 'CWE-16, OWASP A05:2021'
        },
    },
    
    'الهجمات_الشهيرة': {
        'DDoS Attack': {
            'النوع': '⚔️ هجوم إنكار الخدمة',
            'الخطورة': '🟠 عالية جداً',
            'الوصف': 'هجوم لشل الخدمة بإرسال طلبات كثيرة من عدة مصادر',
            'الأنواع': [
                '1. Volumetric - استهلاك النطاق الترددي',
                '2. Protocol - استهلاك الموارد',
                '3. Application - استهداف التطبيق نفسه'
            ],
            'الحماية': [
                '✓ استخدم DDoS mitigation services (CloudFlare, AWS Shield)',
                '✓ قلّل حجم الاستجابات',
                '✓ استخدم rate limiting',
                '✓ قيّد عرض النطاق الترددي',
                '✓ استخدم Web Application Firewall (WAF)',
                '✓ قم بتوزيع الحمل (Load balancing)'
            ],
            'الأدوات': 'CloudFlare, AWS Shield, Akamai, Imperva'
        },
        
        'Man-in-the-Middle (MitM)': {
            'النوع': '⚔️ اعتراض الاتصالات',
            'الخطورة': '🔴 حرجة جداً',
            'الوصف': 'اعتراض الاتصالات بين طرفين لسرقة البيانات',
            'الأنواع': [
                '1. ARP Spoofing - خداع بروتوكول ARP',
                '2. DNS Spoofing - خداع نظام الأسماء',
                '3. SSL Stripping - إزالة التشفير'
            ],
            'الحماية': [
                '✓ استخدم HTTPS/TLS دائماً',
                '✓ تحقق من شهادات SSL',
                '✓ استخدم VPN',
                '✓ استخدم Certificate Pinning',
                '✓ فعّل HSTS',
                '✓ استخدم مفاتيح SSH قوية'
            ],
            'الأدوات': 'Wireshark, Mitmproxy, Burp Suite, Ettercap'
        },
        
        'Phishing': {
            'النوع': '⚔️ خداع اجتماعي',
            'الخطورة': '🟠 عالية جداً',
            'الوصف': 'خداع المستخدمين للحصول على بيانات شخصية',
            'الأنواع': [
                '1. Email Phishing - رسائل بريد مزيفة',
                '2. Spear Phishing - استهداف محدد',
                '3. Clone Phishing - نسخ مواقع حقيقية'
            ],
            'الحماية': [
                '✓ درّب الموظفين على التعرف على الرسائل المريبة',
                '✓ استخدم email filters والـ SPAM detection',
                '✓ تحقق من sender domains (DKIM, SPF)',
                '✓ استخدم MFA على الحسابات',
                '✓ فعّل DMARC policy',
                '✓ استخدم email authentication'
            ],
            'الأدوات': 'Gophish, SpamTitan, Proofpoint'
        },
        
        'Brute Force': {
            'النوع': '⚔️ هجوم القوة الغاشمة',
            'الخطورة': '🟠 عالية',
            'الوصف': 'محاولات متكررة لتخمين كلمات المرور',
            'الأنواع': [
                '1. Dictionary Attack - قائمة كلمات معروفة',
                '2. Rainbow Table - جداول بيانات مسبقة',
                '3. Hybrid Attack - مزيج من الطرق'
            ],
            'الحماية': [
                '✓ استخدم كلمات مرور قوية (12+ حرف)',
                '✓ حدّد محاولات الدخول (Rate limiting)',
                '✓ استخدم MFA',
                '✓ استخدم CAPTCHAs',
                '✓ استخدم account lockout',
                '✓ استخدم password hashing قوي'
            ],
            'الأدوات': 'Hashcat, John the Ripper, Hydra'
        },
    },
    
    'الأدوات': {
        'Burp Suite': {
            'النوع': '🛠️ Web Security Testing',
            'الاستخدام': 'اختبار تطبيقات الويب للثغرات',
            'المميزات': ['Proxy', 'Scanner', 'Repeater', 'Intruder', 'Decoder'],
            'الإصدار': 'Community (مجاني), Professional, Enterprise',
            'الرابط': 'https://portswigger.net/burp'
        },
        
        'OWASP ZAP': {
            'النوع': '🛠️ Web Security Scanner',
            'الاستخدام': 'فحص تطبيقات الويب تلقائياً',
            'المميزات': ['Passive Scan', 'Active Scan', 'Fuzzing', 'API Scanning'],
            'الإصدار': 'مفتوح المصدر (مجاني)',
            'الرابط': 'https://www.zaproxy.org/'
        },
        
        'Metasploit': {
            'النوع': '🛠️ Penetration Testing Framework',
            'الاستخدام': 'اختبار واستغلال الثغرات',
            'المميزات': ['Exploits', 'Payloads', 'Post-Exploitation', 'Reporting'],
            'الإصدار': 'Community (مجاني), Pro',
            'الرابط': 'https://www.metasploit.com/'
        },
        
        'Nmap': {
            'النوع': '🛠️ Network Scanning',
            'الاستخدام': 'مسح المنافذ والخدمات والأجهزة',
            'المميزات': ['Port Scanning', 'Service Detection', 'OS Fingerprinting'],
            'الإصدار': 'مفتوح المصدر (مجاني)',
            'الرابط': 'https://nmap.org/'
        },
        
        'Wireshark': {
            'النوع': '🛠️ Network Analysis',
            'الاستخدام': 'تحليل حركة الشبكة والبروتوكولات',
            'المميزات': ['Packet Capture', 'Protocol Analysis', 'Filtering'],
            'الإصدار': 'مفتوح المصدر (مجاني)',
            'الرابط': 'https://www.wireshark.org/'
        },
        
        'SQLMap': {
            'النوع': '🛠️ SQL Injection Testing',
            'الاستخدام': 'اختبار ثغرات SQL Injection تلقائياً',
            'المميزات': ['Automatic Detection', 'Data Extraction', 'Database Fingerprint'],
            'الإصدار': 'مفتوح المصدر (مجاني)',
            'الرابط': 'http://sqlmap.org/'
        },
    },
    
    'المعايير': {
        'OWASP Top 10': {
            'النوع': '📋 معايير الأمان',
            'الإصدار': '2021',
            'الوصف': 'أخطر 10 ثغرات في تطبيقات الويب',
            'القائمة': [
                '1. A01:2021 – Broken Access Control',
                '2. A02:2021 – Cryptographic Failures',
                '3. A03:2021 – Injection',
                '4. A04:2021 – Insecure Design',
                '5. A05:2021 – Security Misconfiguration',
                '6. A06:2021 – Vulnerable Components',
                '7. A07:2021 – Authentication Failures',
                '8. A08:2021 – Software Integrity Failures',
                '9. A09:2021 – Logging Failures',
                '10. A10:2021 – SSRF'
            ]
        },
        
        'NIST Framework': {
            'النوع': '📋 إطار عمل الأمان',
            'الإصدار': '1.1',
            'الوصف': 'إطار عمل الأمن السيبراني الأمريكي',
            'المحاور': [
                '1. IDENTIFY - تحديد الأصول والمخاطر',
                '2. PROTECT - حماية البيانات والأنظمة',
                '3. DETECT - كشف الحوادث الأمنية',
                '4. RESPOND - الاستجابة للحوادث',
                '5. RECOVER - استعادة النظام'
            ]
        },
        
        'ISO 27001': {
            'النوع': '📋 معيار إدارة الأمان',
            'الإصدار': '2022',
            'الوصف': 'معيار عالمي لإدارة أمان المعلومات',
            'المكونات': [
                '✓ إدارة المخاطر',
                '✓ السياسات والإجراءات',
                '✓ الامتثال القانوني',
                '✓ التدقيق والمراقبة',
                '✓ إدارة الحوادث'
            ]
        },
    },
    
    'نصائح_ذهبية': [
        '🔒 استخدم كلمات مرور قوية: 12+ حرف + أحرف كبيرة + أرقام + رموز',
        '🔐 فعّل MFA على جميع الحسابات المهمة',
        '🌐 استخدم HTTPS فقط، تجنب HTTP',
        '🛡️ حدّث أنظمة التشغيل والبرامج بانتظام',
        '📧 تحقق من رسائل البريد المريبة وتجنب الروابط الغريبة',
        '🔑 استخدم مدير كلمات مرور موثوق',
        '🚀 استخدم VPN على الشبكات العامة',
        '📱 لا تترك أجهزتك بدون حماية',
        '🔔 راقب حسابك بحثاً عن نشاط غريب',
        '🧹 احذف البيانات القديمة التي لا تحتاجها'
    ],
    
    'دورات_التعلم': [
        '🎓 HackTheBox - اختبر مهاراتك العملية',
        '🎓 TryHackMe - دورات تفاعلية مجانية',
        '🎓 Coursera - شهادات جامعية معترف بها',
        '🎓 edX - دورات من جامعات عريقة',
        '🎓 Cybrary - دورات أمان مجانية',
        '🎓 Udemy - دورات بأسعار منخفضة',
        '🎓 Security Blue Team - معايير البطاقة الزرقاء'
    ]
}

class SmartAIAssistant:
    def __init__(self):
        self.db = AI_DATABASE
        self.current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def print_header(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}{Back.BLUE}")
        print("╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "🤖 مساعد الأمن السيبراني الذكي - نسخة متقدمة".center(78) + "║")
        print("║" + "AI Cybersecurity Assistant - Advanced Edition".center(78) + "║")
        print("║" + " "*78 + "║")
        print("║" + f"التاريخ والوقت: {self.current_date}".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        print(f"{Style.RESET_ALL}\n")
    
    def show_main_menu(self):
        self.print_header()
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}القائمة الرئيسية - اختر ما تريد:{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} 📚 الثغرات الأمنية والحلول")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} ⚔️ الهجمات الشهيرة والحماية")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} 🛠️ أدوات الأمن السيبراني")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} 📋 المعايير والمعايير الدولية")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} 💡 نصائح ذهبية للأمان")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} 🎓 دورات وموارد التعلم")
        print(f"{Fore.CYAN}[7]{Style.RESET_ALL} 🔍 بحث حر عن أي موضوع")
        print(f"{Fore.CYAN}[8]{Style.RESET_ALL} ❌ الخروج من المساعد")
        
        print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}\n")
    
    def show_vulnerabilities(self):
        print(f"\n{Fore.YELLOW}الثغرات الأمنية المتاحة:{Style.RESET_ALL}\n")
        vulns = list(self.db['الثغرات'].keys())
        
        for i, vuln in enumerate(vulns, 1):
            print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL} {vuln}")
        
        print(f"\n  {Fore.CYAN}[0]{Style.RESET_ALL} العودة للقائمة الرئيسية\n")
        
        try:
            choice = input(f"{Fore.YELLOW}اختر رقم الثغرة: {Style.RESET_ALL}").strip()
            if choice == '0':
                return
            if 1 <= int(choice) <= len(vulns):
                self.show_vuln_details(vulns[int(choice)-1])
            else:
                print(f"{Fore.RED}❌ اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}❌ خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_vuln_details(self, vuln_name):
        vuln = self.db['الثغرات'][vuln_name]
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📌 {vuln_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.RED}الخطورة:{Style.RESET_ALL} {vuln['الخطورة']}")
        print(f"{Fore.GREEN}الوصف:{Style.RESET_ALL} {vuln['الوصف']}\n")
        
        print(f"{Fore.YELLOW}الأعراض:{Style.RESET_ALL}")
        for symptom in vuln['الأعراض']:
            print(f"  • {symptom}")
        
        print(f"\n{Fore.GREEN}الحلول:{Style.RESET_ALL}")
        for solution in vuln['الحلول']:
            print(f"  {solution}")
        
        print(f"\n{Fore.CYAN}الأدوات:{Style.RESET_ALL} {vuln['الأدوات']}")
        print(f"{Fore.CYAN}الكود الآمن:{Style.RESET_ALL} {vuln['الكود_الآمن']}")
        print(f"{Fore.CYAN}المعايير:{Style.RESET_ALL} {vuln['المعايير']}")
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def show_attacks(self):
        print(f"\n{Fore.YELLOW}الهجمات الشهيرة:{Style.RESET_ALL}\n")
        attacks = list(self.db['الهجمات_الشهيرة'].keys())
        
        for i, attack in enumerate(attacks, 1):
            print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL} {attack}")
        
        print(f"\n  {Fore.CYAN}[0]{Style.RESET_ALL} العودة للقائمة الرئيسية\n")
        
        try:
            choice = input(f"{Fore.YELLOW}اختر رقم الهجوم: {Style.RESET_ALL}").strip()
            if choice == '0':
                return
            if 1 <= int(choice) <= len(attacks):
                self.show_attack_details(attacks[int(choice)-1])
            else:
                print(f"{Fore.RED}❌ اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}❌ خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_attack_details(self, attack_name):
        attack = self.db['الهجمات_الشهيرة'][attack_name]
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚔️ {attack_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}النوع:{Style.RESET_ALL} {attack['النوع']}")
        print(f"{Fore.RED}الخطورة:{Style.RESET_ALL} {attack['الخطورة']}")
        print(f"{Fore.CYAN}الوصف:{Style.RESET_ALL} {attack['الوصف']}\n")
        
        print(f"{Fore.YELLOW}الأنواع:{Style.RESET_ALL}")
        for atype in attack['الأنواع']:
            print(f"  {atype}")
        
        print(f"\n{Fore.GREEN}الحماية:{Style.RESET_ALL}")
        for protection in attack['الحماية']:
            print(f"  {protection}")
        
        print(f"\n{Fore.CYAN}الأدوات:{Style.RESET_ALL} {attack['الأدوات']}")
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def show_tools(self):
        print(f"\n{Fore.YELLOW}أدوات الأمن السيبراني:{Style.RESET_ALL}\n")
        tools = list(self.db['الأدوات'].keys())
        
        for i, tool in enumerate(tools, 1):
            print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL} {tool}")
        
        print(f"\n  {Fore.CYAN}[0]{Style.RESET_ALL} العودة للقائمة الرئيسية\n")
        
        try:
            choice = input(f"{Fore.YELLOW}اختر رقم الأداة: {Style.RESET_ALL}").strip()
            if choice == '0':
                return
            if 1 <= int(choice) <= len(tools):
                self.show_tool_details(tools[int(choice)-1])
            else:
                print(f"{Fore.RED}❌ اختيار غير صحيح{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}❌ خطأ في الإدخال{Style.RESET_ALL}")
    
    def show_tool_details(self, tool_name):
        tool = self.db['الأدوات'][tool_name]
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🛠️ {tool_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        for key, value in tool.items():
            if key == 'المميزات':
                print(f"{Fore.GREEN}{key}:{Style.RESET_ALL}")
                for feature in value:
                    print(f"  • {feature}")
            else:
                print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def show_tips(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 النصائح الذهبية للأمان{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        for i, tip in enumerate(self.db['نصائح_ذهبية'], 1):
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {tip}\n")
        
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def show_courses(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎓 دورات وموارد التعلم{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        for course in self.db['دورات_التعلم']:
            print(f"  {course}\n")
        
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def run(self):
        while True:
            self.show_main_menu()
            choice = input(f"{Fore.CYAN}اختيارك: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.show_vulnerabilities()
            elif choice == '2':
                self.show_attacks()
            elif choice == '3':
                self.show_tools()
            elif choice == '4':
                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📋 المعايير والمعايير الدولية{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
                
                for framework_name, framework in self.db['المعايير'].items():
                    print(f"{Fore.GREEN}{framework_name}:{Style.RESET_ALL}")
                    print(f"  النوع: {framework['النوع']}")
                    print(f"  الإصدار: {framework['الإصدار']}")
                    print(f"  الوصف: {framework['الوصف']}\n")
                    
                    for item in list(framework.values())[3]:
                        print(f"    {item}")
                    print()
                
                print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
            elif choice == '5':
                self.show_tips()
            elif choice == '6':
                self.show_courses()
            elif choice == '7':
                query = input(f"\n{Fore.YELLOW}ابحث عن موضوع (مثل: SQL): {Style.RESET_ALL}").strip().lower()
                results = []
                
                for vuln in self.db['الثغرات']:
                    if query in vuln.lower():
                        results.append(('ثغرة', vuln))
                
                for attack in self.db['الهجمات_الشهيرة']:
                    if query in attack.lower():
                        results.append(('هجوم', attack))
                
                if results:
                    print(f"\n{Fore.GREEN}وجدنا {len(results)} نتيجة:{Style.RESET_ALL}\n")
                    for i, (ttype, item) in enumerate(results, 1):
                        print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL} {item} ({ttype})")
                else:
                    print(f"{Fore.RED}لم نجد نتائج{Style.RESET_ALL}\n")
            elif choice == '8':
                print(f"\n{Fore.GREEN}شكراً لاستخدام المساعد! 👋{Style.RESET_ALL}\n")
                return
            else:
                print(f"{Fore.RED}❌ اختيار غير صحيح{Style.RESET_ALL}\n")
            
            input(f"{Fore.YELLOW}اضغط Enter للمتابعة...{Style.RESET_ALL}")
