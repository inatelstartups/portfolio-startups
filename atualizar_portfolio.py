#!/usr/bin/env python3
"""
Script de atualização automática do Portfólio de Startups (Inatel Startups).
Busca as 4 views compartilhadas do Airtable, baixa as logos via endpoint assinado,
aplica recorte inteligente e classificação óptica de fundo, ordena alfabeticamente (A-Z)
e atualiza o index.html.
"""
import html
import json
import os
import re
import subprocess
import unicodedata
import urllib.parse
import urllib.request
from PIL import Image, ImageChops, ImageDraw

VIEWS = {
    "ideation": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shr6lGlyWE9395CtX/tblAEZQFetlB1ThTe"),
    "pre-incubated": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shrQMcUOOgtk19ydG/tblAEZQFetlB1ThTe"),
    "incubated": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shrd6rAzCsgZv2elr/tblAEZQFetlB1ThTe"),
    "graduated": ("app45MMiNeduNXvUx", "https://airtable.com/app45MMiNeduNXvUx/shrHu5Ku1Q5Phv7WP/tblAEZQFetlB1ThTe"),
}

STAGE_TAG_LABEL = {
    "ideation": "Ideação",
    "pre-incubated": "Pré-Incubação",
    "incubated": "Incubadas",
    "graduated": "Graduada",
}

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return f"logo_{text}"

if __name__ == "__main__":
    print("Para atualizar e publicar no GitHub:")
    print("  git add -A && git commit -m 'Atualiza portfólio de startups' && git push origin main")
