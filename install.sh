#!/bin/bash

# سكريبت التثبيت لأداة فحص أمان المواقع
# Installation script for Website Security Scanner

echo "======================================"
echo "أداة فحص أمان المواقع الشاملة"
echo "Website Security Scanner Installer"
echo "======================================"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    echo "على Kali Linux, استخدم:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✓ Python 3 موجود"
python3 --version
echo ""

# تثبيت المتطلبات
echo "جاري تثبيت المتطلبات..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ تم التثبيت بنجاح!"
    echo ""
    echo "الاستخدام:"
    echo "  python3 scanner.py <URL>"
    echo ""
    echo "الأمثلة:"
    echo "  python3 scanner.py google.com"
    echo "  python3 scanner.py https://example.com"
    echo ""
else
    echo "❌ فشل التثبيت"
    exit 1
fi
