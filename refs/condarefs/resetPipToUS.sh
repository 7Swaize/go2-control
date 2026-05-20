#!/bin/bash
# reset_pip_us.sh
# One-shot script to reset pip from Chinese mirror to US/global PyPI

echo "[1/3] Checking current pip configuration..."
pip config list

echo "[2/3] Unsetting any existing mirror..."
pip config unset global.index-url 2>/dev/null
pip config unset install.index-url 2>/dev/null

echo "[3/3] Setting pip to official US PyPI..."
pip config set global.index-url https://pypi.org/simple

echo "Done. Current pip config is now:"
pip config list

echo "Testing with pip self-upgrade..."
pip install --upgrade pip -i https://pypi.org/simple

# pip config unset global.index-url 2>/dev/null && pip config unset install.index-url 2>/dev/null && pip config set global.index-url https://pypi.org/simple && pip install --upgrade pip -i https://pypi.org/simple

