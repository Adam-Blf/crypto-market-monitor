"""
Crypto Market Monitor - Presentation PPTX
M1 Data Engineering & IA - EFREI Paris - Module Real-Time Engineering 2025-2026
Adam Beloucif, Emilien Morice
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto-market-monitor.pptx")

NAVY   = RGBColor(0x0A, 0x0E, 0x1A)
AMBER  = RGBColor(0xF5, 0x9E, 0x0B)
PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
WHITE  = RGBColor(0xF8, 0xFA, 0xFC)
MUTED  = RGBColor(0x94, 0xA3, 0xB8)
GREEN  = RGBColor(0x10, 0xB9, 0x81)
CARD   = RGBColor(0x11, 0x18, 0x27)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)


def set_bg(slide, color=NAVY):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, text, left, top, width, height,
             size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return tb


def add_rect(slide, left, top, width, height, color=CARD):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_title(slide, title):
    add_text(slide, title, 0.5, 0.2, 12.5, 0.85, size=28, bold=True, color=AMBER)


def add_footer(slide, num, total=12):
    add_text(slide, "M1 EFREI - Real-Time Engineering  |  Adam Beloucif, Emilien Morice  |  " + str(num) + "/" + str(total),
             0.4, 7.15, 12.5, 0.3, size=9, color=MUTED)
    line = slide.shapes.add_shape(1, Inches(0), Inches(7.46), Inches(13.33), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = AMBER
    line.line.fill.background()


def new_slide():
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)
    set_bg(slide)
    return slide


def bullet_list(slide, items, left, top, width, size=13):
    for i, item in enumerate(items):
        add_text(slide, "  " + item, left, top + i * 0.42, width, 0.4, size=size, color=WHITE)


# Slide 1 - Title
s1 = new_slide()
bar = s1.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(0.07))
bar.fill.solid(); bar.fill.fore_color.rgb = AMBER; bar.line.fill.background()
add_text(s1, "CRYPTO MARKET MONITOR", 1.0, 1.1, 11.3, 1.1,
         size=42, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
add_text(s1, "Systeme de surveillance des marches crypto en temps reel", 1.0, 2.4, 11.3, 0.6,
         size=18, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s1, "Pipeline Kafka  -  Analytics en fenetre glissante  -  Dashboard live Socket.IO",
         1.0, 3.05, 11.3, 0.5, size=14, color=MUTED, italic=True, align=PP_ALIGN.CENTER)
add_rect(s1, 3.7, 4.0, 5.9, 1.65, CARD)
add_text(s1, "Adam Beloucif  &  Emilien Morice", 3.7, 4.15, 5.9, 0.5,
         size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s1, "M1 Data Engineering & IA - EFREI Paris", 3.7, 4.65, 5.9, 0.4,
         size=12, color=AMBER, align=PP_ALIGN.CENTER)
add_text(s1, "Module Real-Time Engineering  -  2025-2026", 3.7, 5.05, 5.9, 0.35,
         size=11, color=MUTED, align=PP_ALIGN.CENTER)
add_text(s1, "Projet realise a 2 personnes (consigne prevue pour 4)", 1.0, 6.25, 11.3, 0.4,
         size=11, color=PURPLE, italic=True, align=PP_ALIGN.CENTER)

# Slide 2 - Contexte
s2 = new_slide()
add_title(s2, "Contexte et problematique")
add_footer(s2, 2)
add_rect(s2, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s2, "Contexte", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s2, [
    "Marches crypto : 100M+ transactions/jour sur Binance",
    "Volatilite extreme, besoin de reaction < 1 seconde",
    "Plusieurs sources heterogenes (Binance + Coinbase)",
    "Detecter les mouvements anormaux en continu",
    "Afficher les metriques live sans polling HTTP",
], 0.6, 1.82, 5.5)
add_rect(s2, 6.9, 1.15, 6.0, 5.5, CARD)
add_text(s2, "Problematique technique", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s2, [
    "Ingerer des flux WebSocket haute frequence",
    "Decoupler ingestion / traitement / affichage",
    "Calculer VWAP, SMA, z-score en temps reel",
    "Pousser les mises a jour vers N clients simultanement",
    "Resilience : reconnexion auto, tolerance aux pannes",
], 7.1, 1.82, 5.6)

# Slide 3 - Architecture
s3 = new_slide()
add_title(s3, "Architecture globale - Pipeline Kafka")
add_footer(s3, 3)
boxes = [
    (0.25, 2.9, 2.1, "Sources WS\nBinance + Coinbase", PURPLE),
    (2.7,  2.9, 2.1, "Ingester\nNode.js + TS",         AMBER),
    (5.15, 2.9, 2.2, "Apache Kafka\nKRaft 3.7",         RGBColor(0x23, 0x1F, 0x20)),
    (7.7,  2.9, 2.1, "Processor\nVWAP SMA Z-score",    AMBER),
    (10.15,2.9, 2.8, "API + Dashboard\nExpress / Socket.IO", AMBER),
]
for lft, top, wid, lbl, col in boxes:
    shape = s3.shapes.add_shape(1, Inches(lft), Inches(top), Inches(wid), Inches(1.4))
    shape.fill.solid(); shape.fill.fore_color.rgb = col
    shape.line.color.rgb = WHITE
    tf = shape.text_frame; tf.text = lbl
    for para in tf.paragraphs:
        para.alignment = PP_ALIGN.CENTER
        for run in para.runs:
            run.font.size = Pt(11); run.font.bold = True
            run.font.color.rgb = NAVY if col == AMBER else WHITE
add_rect(s3, 0.4, 5.3, 12.5, 1.5, CARD)
add_text(s3, "Kafka decouples les producteurs des consommateurs : debits independants sans perte de donnees.\nRetention configurable (1h par defaut). Partitionnement par symbole (BTC-USDT, ETH-USDT, BTC-USD).",
         0.6, 5.4, 12.1, 1.2, size=11, color=WHITE)

# Slide 4 - Kafka
s4 = new_slide()
add_title(s4, "Apache Kafka - Mode KRaft (sans Zookeeper)")
add_footer(s4, 4)
add_rect(s4, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s4, "Pourquoi Kafka ?", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s4, [
    "Tampon tolerant aux pannes entre ingestion et traitement",
    "Les producteurs ecrivent a la vitesse du marche",
    "Les consommateurs lisent a leur propre rythme",
    "Multi-consommateurs independants sur le meme topic",
    "Retention configurable : relecture en cas de crash",
    "Image bitnami/kafka:3.7 (KRaft pre-configure)",
], 0.6, 1.82, 5.5)
add_rect(s4, 6.9, 1.15, 6.0, 2.6, CARD)
add_text(s4, "KRaft vs Zookeeper", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
add_text(s4, "Kafka 3.7+ gere ses metadonnees via Raft interne.\nSupprime la dependance Zookeeper.\nDeploiement : 1 conteneur + 1 volume.",
         7.1, 1.82, 5.6, 1.6, size=12, color=WHITE)
add_rect(s4, 6.9, 4.0, 6.0, 2.65, CARD)
add_text(s4, "Topics du projet", 7.1, 4.15, 5.6, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s4, [
    "crypto-trades  ->  transactions brutes normalisees",
    "crypto-metrics  ->  metriques calculees par symbole",
], 7.1, 4.65, 5.6)
add_text(s4, "Cle de partition = symbole (ordre des messages garanti par paire)",
         7.1, 5.6, 5.6, 0.45, size=11, color=MUTED)

# Slide 5 - Ingester
s5 = new_slide()
add_title(s5, "Service Ingester - Collecte des flux WebSocket")
add_footer(s5, 5)
add_rect(s5, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s5, "Sources de donnees", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s5, [
    "Binance : BTC/USDT, ETH/USDT (stream combine)",
    "Coinbase Advanced Trade : BTC-USD",
    "wss://stream.binance.com:9443/stream",
    "wss://advanced-trade-ws.coinbase.com",
], 0.6, 1.82, 5.5)
add_text(s5, "Interface Trade normalisee :", 0.6, 3.65, 5.5, 0.4, size=12, bold=True, color=AMBER)
add_text(s5, "{ exchange, symbol, price, quantity,\n  timestamp, tradeId, side, value }",
         0.6, 4.1, 5.5, 0.9, size=11, color=GREEN)
add_rect(s5, 6.9, 1.15, 6.0, 5.5, CARD)
add_text(s5, "Resilience", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s5, [
    "Reconnexion auto avec backoff exponentiel",
    "Max 10 tentatives par connexion WebSocket",
    "Delai initial 1s, max 30s entre tentatives",
    "Heartbeat Coinbase gere (channel heartbeats)",
    "Arret propre SIGTERM/SIGINT (vidage buffer Kafka)",
    "Partitionnement par cle symbole",
], 7.1, 1.82, 5.6)

# Slide 6 - Processor
s6 = new_slide()
add_title(s6, "Service Processor - Moteur Analytique Temps Reel")
add_footer(s6, 6)
rows = [
    ("VWAP",      "sum(prix * qte) / sum(qte)", "1 minute", "Prix moyen pondere par volume"),
    ("SMA-20",    "moyenne des 20 derniers prix","20 trades","Tendance de court terme"),
    ("Z-Score",   "(valeur - mu) / sigma",       "1 minute", "Alerte si > seuil 2.5"),
    ("Var. 1min", "(prix - prix_0) / prix_0",   "1 minute", "Performance instantanee"),
    ("Var. 5min", "(prix - prix_0) / prix_0",   "5 minutes","Performance moyen terme"),
    ("High/Low",  "max/min des prix",            "1 minute", "Amplitude de la bougie"),
]
add_rect(s6, 0.4, 1.15, 12.6, 0.5, RGBColor(0x1E, 0x29, 0x3B))
for col_x, lbl in [(0.55, "Metrique"), (3.2, "Formule"), (7.1, "Fenetre"), (9.2, "Objectif")]:
    add_text(s6, lbl, col_x, 1.22, 2.5, 0.35, size=11, bold=True, color=AMBER)
for i, (name, formula, window, desc) in enumerate(rows):
    y = 1.72 + i * 0.58
    bg = CARD if i % 2 == 0 else RGBColor(0x16, 0x1F, 0x30)
    add_rect(s6, 0.4, y, 12.6, 0.55, bg)
    add_text(s6, name,    0.55, y+0.09, 2.4,  0.38, size=12, bold=True, color=WHITE)
    add_text(s6, formula, 3.2,  y+0.09, 3.7,  0.38, size=10, color=GREEN)
    add_text(s6, window,  7.1,  y+0.09, 1.9,  0.38, size=11, color=AMBER)
    add_text(s6, desc,    9.2,  y+0.09, 3.6,  0.38, size=10, color=MUTED)
add_text(s6, "Buffer circulaire en memoire : max 1000 trades/symbole, eviction TTL 10 minutes",
         0.5, 7.05, 12.4, 0.35, size=10, color=PURPLE, italic=True)

# Slide 7 - API
s7 = new_slide()
add_title(s7, "Service API - Express + Socket.IO")
add_footer(s7, 7)
add_rect(s7, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s7, "Endpoints REST", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
for i, ep in enumerate([
    "GET /api/health            sante du service",
    "GET /api/metrics           toutes les metriques",
    "GET /api/metrics/:symbol   par paire",
    "GET /api/history/:symbol   historique (max 200)",
    "GET /api/anomalies         50 dernieres alertes",
]):
    add_text(s7, ep, 0.6, 1.85 + i*0.6, 5.5, 0.5, size=11, color=WHITE)
add_rect(s7, 6.9, 1.15, 6.0, 5.5, CARD)
add_text(s7, "Evenements Socket.IO (push serveur)", 7.1, 1.3, 5.6, 0.45, size=13, bold=True, color=AMBER)
for i, (ev, desc) in enumerate([
    ("metrics:update",   "Nouvelles metriques calculees"),
    ("anomaly:detected", "Alerte z-score > seuil"),
    ("server:stats",     "Stats serveur (connexions, msg/s)"),
    ("initial:state",    "Etat complet a la connexion"),
    ("subscribe:symbol", "Choix de la paire par le client"),
]):
    y = 1.85 + i * 0.6
    add_text(s7, ev,   7.1, y, 2.8, 0.4, size=11, bold=True, color=GREEN)
    add_text(s7, desc, 10.0, y, 2.8, 0.4, size=11, color=MUTED)

# Slide 8 - Dashboard
s8 = new_slide()
add_title(s8, "Dashboard - Interface Temps Reel")
add_footer(s8, 8)
add_rect(s8, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s8, "Composants visuels", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s8, [
    "Prix hero avec flash vert/rouge au changement",
    "Badges variation 1min et 5min",
    "4 stat-cards : Volume, Trades, High, Low",
    "Graphique prix + SMA-20 (Chart.js line)",
    "Barres de volume par paire (Chart.js bar)",
    "Flux anomalies avec beep AudioContext",
    "Horloge + statut connexion temps reel",
], 0.6, 1.82, 5.5)
add_rect(s8, 6.9, 1.15, 6.0, 5.5, CARD)
add_text(s8, "Qualite UX", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s8, [
    "Dark theme EFREI : navy #0A0E1A + amber #F59E0B",
    "Logos SVG officiels Bitcoin, Ethereum, Coinbase",
    "Barre accent EFREI amber-purple en haut de page",
    "i18n FR/EN avec bascule instantanee (localStorage)",
    "Mode demo : donnees simulees si backend absent",
    "Inter + JetBrains Mono (Google Fonts)",
    "Animations CSS 150ms, prefers-reduced-motion",
], 7.1, 1.82, 5.6)

# Slide 9 - Securite
s9 = new_slide()
add_title(s9, "Securite - Niveau Production")
add_footer(s9, 9)
sec_rows = [
    ("helmet",             "HTTP headers (CSP, HSTS, X-Frame-Options, nosniff...)"),
    ("express-rate-limit", "100 req / 15min par IP - protection brute-force"),
    ("zod",                "Validation stricte des variables d'environnement au demarrage"),
    ("morgan",             "Logging HTTP avec rotation - zero stack trace cote client"),
    ("CORS strict",        "Whitelist explicite des origines autorisees"),
    ("Non-root Docker",    "Tous les conteneurs tournent en utilisateur appuser (UID 1000)"),
    (".dockerignore",      "Exclusion des .env, node_modules, secrets des images"),
    ("Secrets env vars",   "Zero secret en dur - .env gitignored"),
]
for i, (tech, desc) in enumerate(sec_rows):
    y = 1.2 + i * 0.6
    bg = CARD if i % 2 == 0 else RGBColor(0x16, 0x1F, 0x30)
    add_rect(s9, 0.4, y, 12.6, 0.56, bg)
    add_text(s9, tech, 0.6,  y+0.1, 3.0, 0.38, size=12, bold=True, color=AMBER)
    add_text(s9, desc, 3.8,  y+0.1, 9.0, 0.38, size=11, color=WHITE)

# Slide 10 - i18n
s10 = new_slide()
add_title(s10, "Multilinguisme - i18n Francais / Anglais")
add_footer(s10, 10)
add_rect(s10, 0.4, 1.15, 5.9, 5.5, CARD)
add_text(s10, "Architecture i18n (vanilla JS)", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s10, [
    "Module IIFE I18n - zero dependance externe",
    "Chargement async des JSON depuis i18n/",
    "Langue persistee dans localStorage (cmm-locale)",
    "Attributs data-i18n sur tous les elements statiques",
    "Fonctions formatPrice/formatTime locale-aware",
    "Boutons FR | EN en header avec aria-pressed",
    "document.documentElement.lang mis a jour",
], 0.6, 1.82, 5.5)
add_rect(s10, 6.9, 1.15, 6.0, 5.5, CARD)
add_text(s10, "Exemple (fr.json)", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
add_text(s10, '{\n  "title": "CRYPTO MONITOR",\n  "live": "EN DIRECT",\n  "connected": "Connecte",\n  "anomalies": {\n    "title": "Alertes anomalies",\n    "zscore": "Score Z"\n  },\n  "footer": {\n    "module": "Ingenierie Temps Reel"\n  }\n}',
         7.1, 1.82, 5.6, 3.5, size=10, color=GREEN)

# Slide 11 - Deploiement
s11 = new_slide()
add_title(s11, "Deploiement - 3 options Docker")
add_footer(s11, 11)
add_rect(s11, 0.4, 1.15, 4.0, 5.5, CARD)
add_text(s11, "Option 1\nLanceur autonome", 0.6, 1.3, 3.6, 0.75, size=13, bold=True, color=AMBER)
add_text(s11, "node launcher/src/index.mjs\n\nVerifie Docker, build,\nattend les healthchecks\net ouvre le dashboard.\n\nCompile en .exe (pkg) :\nnpm run build:win", 0.6, 2.12, 3.6, 3.5, size=11, color=WHITE)
add_rect(s11, 4.7, 1.15, 4.1, 5.5, CARD)
add_text(s11, "Option 2\nImage tout-en-un", 4.9, 1.3, 3.7, 0.75, size=13, bold=True, color=AMBER)
add_text(s11, "docker build \\\n  -f all-in-one.Dockerfile \\\n  -t crypto-monitor .\n\ndocker run -p 8080:8080 \\\n  crypto-monitor\n\n1 conteneur supervisord :\nKafka + 3 services + nginx", 4.9, 2.12, 3.7, 3.5, size=11, color=WHITE)
add_rect(s11, 9.1, 1.15, 4.2, 5.5, CARD)
add_text(s11, "Option 3\nDocker Compose", 9.3, 1.3, 3.8, 0.75, size=13, bold=True, color=AMBER)
add_text(s11, "cp .env.example .env\ndocker-compose up \\\n  --build -d\n\n6 services :\nkafka, kafka-ui,\ningester, processor,\napi, dashboard (nginx)\n\nDashboard  :8080\nKafka UI   :8090", 9.3, 2.12, 3.8, 3.5, size=11, color=WHITE)

# Slide 12 - Conclusion
s12 = new_slide()
add_title(s12, "Bilan et perspectives")
add_footer(s12, 12)
add_rect(s12, 0.4, 1.15, 5.9, 3.0, CARD)
add_text(s12, "Ce qui a ete realise", 0.6, 1.3, 5.5, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s12, [
    "Pipeline Kafka bout-en-bout fonctionnel",
    "3 services TypeScript + dashboard complet",
    "Analytics : VWAP, SMA-20, z-score, high/low",
    "Securite production (helmet, rate-limit, zod)",
    "i18n FR/EN + mode demo offline",
], 0.6, 1.82, 5.5, size=12)
add_rect(s12, 6.9, 1.15, 6.0, 3.0, CARD)
add_text(s12, "Contexte du projet", 7.1, 1.3, 5.6, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s12, [
    "Realise a 2 (consigne prevue pour 4 personnes)",
    "M1 Real-Time Engineering - EFREI Paris 2025-2026",
    "TypeScript strict, Docker multi-stage",
    "3 options de deploiement",
], 7.1, 1.82, 5.6, size=12)
add_rect(s12, 0.4, 4.35, 12.6, 2.85, CARD)
add_text(s12, "Perspectives d evolution", 0.6, 4.5, 12.2, 0.45, size=14, bold=True, color=AMBER)
bullet_list(s12, [
    "Ajout de paires supplementaires (SOL, BNB, XRP...)",
    "Alertes email/SMS via webhook Kafka Connect",
    "Stockage historique dans InfluxDB ou TimescaleDB",
    "Deploiement Kubernetes (Helm chart) pour la scalabilite",
], 0.6, 5.02, 12.2, size=12)

prs.save(OUT)
print("Presentation saved -> " + OUT)
