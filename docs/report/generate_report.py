"""
Crypto Market Monitor - Rapport Technique PDF v2
EFREI branding officiel : navy #163767, rose #ff43b8, bleu #3653a0, Gilroy -> Helvetica
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto-market-monitor-rapport-technique.pdf")

# EFREI palette
BG      = colors.HexColor("#0B1B34")
NAVY    = colors.HexColor("#163767")
ROSE    = colors.HexColor("#FF43B8")
BLUE    = colors.HexColor("#3653A0")
BLUE2   = colors.HexColor("#337AB6")
PURPLE  = colors.HexColor("#95569E")
WHITE   = colors.HexColor("#FFFFFF")
MUTED   = colors.HexColor("#94A3B8")
GREEN   = colors.HexColor("#10B981")
CARD    = colors.HexColor("#163767")
CARD2   = colors.HexColor("#1E2E4A")
DARK    = colors.HexColor("#0D1F3C")
RED_LT  = colors.HexColor("#F87171")

PAGE_W, PAGE_H = A4

doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2.2*cm, bottomMargin=1.8*cm,
    title="Rapport Technique - Crypto Market Monitor",
    author="Adam Beloucif, Emilien Morice",
    subject="M1 Real-Time Engineering - EFREI Paris 2025-2026",
)

styles = getSampleStyleSheet()

def sty(name, **kwargs):
    return ParagraphStyle(name, parent=styles["Normal"], **kwargs)

ST_COVER_TITLE = sty("ct", fontSize=32, textColor=WHITE, alignment=TA_LEFT,
                     spaceAfter=4, leading=38, fontName="Helvetica-Bold")
ST_COVER_SUB   = sty("cs", fontSize=14, textColor=MUTED, alignment=TA_LEFT,
                     spaceAfter=6, leading=20)
ST_H1   = sty("h1", fontSize=20, textColor=WHITE, spaceBefore=16, spaceAfter=4,
              leading=26, fontName="Helvetica-Bold")
ST_SECTION_LABEL = sty("sl", fontSize=9, textColor=ROSE, spaceBefore=2, spaceAfter=2,
                        leading=12, fontName="Helvetica-Bold")
ST_H2   = sty("h2", fontSize=13, textColor=WHITE, spaceBefore=10, spaceAfter=3,
              leading=17, fontName="Helvetica-Bold")
ST_BODY = sty("body", fontSize=10, textColor=MUTED, spaceAfter=4,
              leading=15, alignment=TA_JUSTIFY)
ST_BODY_L = sty("bodyl", fontSize=10, textColor=MUTED, spaceAfter=4, leading=15)
ST_BULLET = sty("bul", fontSize=10, textColor=WHITE, spaceAfter=2,
                leading=14, leftIndent=10)
ST_CODE = sty("code", fontSize=9, textColor=GREEN, fontName="Courier",
              spaceAfter=3, leading=13, backColor=DARK, leftIndent=8)
ST_CAPTION = sty("cap", fontSize=9, textColor=MUTED, alignment=TA_CENTER,
                 spaceAfter=6, leading=12)
ST_ROSE = sty("rose", fontSize=11, textColor=ROSE, fontName="Helvetica-Bold",
              spaceBefore=6, spaceAfter=2, leading=15)
ST_NUM  = sty("num", fontSize=28, textColor=ROSE, fontName="Helvetica-Bold",
              alignment=TA_CENTER, spaceAfter=2, leading=32)

def hr(color=ROSE):
    return HRFlowable(width="100%", thickness=1.5, color=color, spaceAfter=8, spaceBefore=4)

def sp(n=6): return Spacer(1, n)
def h1(text): return Paragraph(text, ST_H1)
def h2(text): return Paragraph(text, ST_H2)
def body(text): return Paragraph(text, ST_BODY)
def bul(text): return Paragraph(f"  - {text}", ST_BULLET)
def code(text): return Paragraph(text, ST_CODE)
def rose_label(text): return Paragraph(text.upper(), ST_SECTION_LABEL)

def table(data, col_widths, header_color=ROSE):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), header_color),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("PADDING",    (0,0), (-1,-1), 6),
        ("GRID",       (0,0), (-1,-1), 0.3, CARD2),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [DARK, CARD]),
        ("TEXTCOLOR",  (0,1), (-1,-1), WHITE),
        ("LEADING",    (0,0), (-1,-1), 13),
    ]))
    return t

story = []

# ══════════════════════════════════════════════════════
# PAGE DE COUVERTURE
# ══════════════════════════════════════════════════════
story += [sp(40)]

# Rose accent line (simulate via table)
cov_top = Table([[""]],colWidths=[17*cm], rowHeights=[0.12*cm])
cov_top.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ROSE),("LINEBELOW",(0,0),(-1,-1),0,ROSE)]))
story.append(cov_top)
story += [sp(20)]

story.append(Paragraph("CRYPTO MARKET MONITOR", ST_COVER_TITLE))
story.append(Paragraph("Rapport Technique", ST_COVER_SUB))
story += [sp(8)]
cov_div = Table([[""]],colWidths=[5*cm], rowHeights=[0.1*cm])
cov_div.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ROSE)]))
story.append(cov_div)
story += [sp(8)]
story.append(Paragraph("Pipeline Kafka  -  Analytics temps reel  -  Dashboard live", ST_COVER_SUB))
story += [sp(40)]

meta = [
    ["AUTEURS",   "Adam Beloucif, Emilien Morice"],
    ["FORMATION", "M1 Data Engineering & IA - EFREI Paris"],
    ["MODULE",    "Real-Time Engineering  -  S9 2025-2026"],
    ["DATE",      "Juin 2026"],
    ["CONTEXTE",  "Projet realise a 2 personnes (consigne prevue pour 4)"],
]
mt = Table(meta, colWidths=[3.5*cm, 13*cm])
mt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TEXTCOLOR", (0,0),(0,-1),ROSE),
    ("TEXTCOLOR", (1,0),(1,-1),WHITE),
    ("FONTNAME",  (0,0),(0,-1),"Helvetica-Bold"),
    ("FONTSIZE",  (0,0),(-1,-1),9),
    ("PADDING",   (0,0),(-1,-1),7),
    ("GRID",      (0,0),(-1,-1),0.3,CARD2),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[DARK,CARD]),
]))
story.append(mt)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# 1. INTRODUCTION
# ══════════════════════════════════════════════════════
story += [rose_label("introduction"), h1("1. Introduction"), hr()]
story += [
    body("Ce rapport presente l'architecture, les choix techniques et les resultats du projet "
         "Crypto Market Monitor, realise dans le cadre du module Real-Time Engineering du M1 Data "
         "Engineering et IA de l'EFREI Paris (2025-2026)."),
    sp(),
    body("L'objectif : construire un pipeline de streaming bout-en-bout qui ingere des transactions "
         "crypto en direct depuis Binance et Coinbase, les traite via Apache Kafka, calcule des "
         "metriques analytiques en fenetre glissante (VWAP, SMA-20, z-score) et pousse les resultats "
         "vers un dashboard live via Socket.IO."),
    sp(12),
]

# KPIs
kpi_data = [
    ["100M+\ntransactions/jour\n(Binance)", "< 1s\nlatence cible\ndetection anomalie", "3\nsources\nBinance + Coinbase", "4\nservices\nindependants"],
]
kpi_t = Table(kpi_data, colWidths=[4*cm]*4)
kpi_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TEXTCOLOR", (0,0),(-1,-1),WHITE),
    ("FONTNAME",  (0,0),(-1,-1),"Helvetica-Bold"),
    ("FONTSIZE",  (0,0),(-1,-1),10),
    ("ALIGN",     (0,0),(-1,-1),"CENTER"),
    ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ("PADDING",   (0,0),(-1,-1),10),
    ("LINEABOVE", (0,0),(-1,0),2,ROSE),
    ("GRID",      (0,0),(-1,-1),0.3,CARD2),
]))
story += [kpi_t, sp(12), PageBreak()]

# ══════════════════════════════════════════════════════
# 2. ARCHITECTURE
# ══════════════════════════════════════════════════════
story += [rose_label("architecture"), h1("2. Architecture du systeme"), hr()]
story += [
    body("Le systeme suit un pipeline lineaire : collecte WebSocket -> Kafka -> traitement "
         "analytique -> API REST/WebSocket -> dashboard. Chaque service est isole dans un "
         "conteneur Docker independant."),
    sp(8),
]

comp_data = [
    ["Service", "Role", "Technologies"],
    ["Ingester",   "Clients WS Binance + Coinbase, normalisation, production Kafka", "Node.js, TypeScript, ws, kafkajs"],
    ["Kafka",      "Tampon decoupling, tolerance pannes, multi-consommateurs",        "Apache Kafka 3.7 KRaft"],
    ["Processor",  "Consomme trades, calcule VWAP SMA-20 z-score variance",          "Node.js, TypeScript, kafkajs"],
    ["API",        "Agregation, endpoints REST, push WebSocket live",                 "Express, Socket.IO, helmet"],
    ["Dashboard",  "Graphiques Chart.js, flux anomalies, i18n FR/EN",                "HTML, CSS, JS, Chart.js 4"],
]
story += [table(comp_data, [3*cm, 8.5*cm, 5*cm]), sp(10)]

story += [
    h2("Flux de donnees"),
    code("WS Sources -> Ingester -> Kafka [crypto-trades] -> Processor -> Kafka [crypto-metrics] -> API -> Socket.IO -> Dashboard"),
    sp(4),
    body("Le partitionnement par symbole (cle = BTC-USDT, ETH-USDT, BTC-USD) garantit l'ordre "
         "des messages par paire. La retention est de 1 heure. En cas de crash du processor, "
         "il relira le topic depuis son dernier offset consomme."),
    sp(12), PageBreak(),
]

# ══════════════════════════════════════════════════════
# 3. KAFKA
# ══════════════════════════════════════════════════════
story += [rose_label("apache kafka"), h1("3. Apache Kafka - Mode KRaft"), hr()]
story += [
    body("Kafka 3.7 en mode KRaft elimine Zookeeper. Les metadonnees du cluster sont gerees "
         "via Raft interne, ce qui simplifie le deploiement (1 conteneur + 1 volume) et "
         "reduit la surface d'attaque operationnelle."),
    sp(6),
]

topic_data = [
    ["Topic", "Description", "Partitions", "Retention"],
    ["crypto-trades",  "Transactions brutes normalisees (interface Trade)",   "3", "1h"],
    ["crypto-metrics", "Metriques calculees par symbole (VWAP, SMA, etc.)",  "3", "1h"],
]
story += [table(topic_data, [4.5*cm, 8*cm, 2.5*cm, 1.5*cm]), sp(6)]
story += [
    bul("Image Docker : bitnami/kafka:3.7 (KRaft pre-configure)"),
    bul("Partition key = symbole -> ordre des messages garanti par paire"),
    bul("Reconnexion Kafka client : backoff exponentiel, max 10 tentatives"),
    sp(12), PageBreak(),
]

# ══════════════════════════════════════════════════════
# 4. SERVICES
# ══════════════════════════════════════════════════════
story += [rose_label("services node.js"), h1("4. Services Node.js TypeScript"), hr()]

story += [h2("4.1 Ingester"), sp(3)]
story += [
    body("L'ingester maintient des connexions WebSocket persistantes et normalise chaque "
         "message vers une interface Trade commune avant de le produire sur Kafka."),
    bul("Binance : stream combine BTC/USDT + ETH/USDT"),
    bul("Coinbase : BTC-USD via Advanced Trade WebSocket"),
    bul("Reconnexion auto : backoff exponentiel, max 10 tentatives, delai max 30s"),
    bul("Arret propre SIGTERM/SIGINT avec vidage du buffer Kafka"),
    sp(8),
]

story += [h2("4.2 Processor - Analytique"), sp(3)]

metrics_data = [
    ["Metrique", "Formule", "Fenetre", "Objectif"],
    ["VWAP",       "sum(prix * qte) / sum(qte)",       "1 min",    "Prix moyen pondere par volume"],
    ["SMA-20",     "moyenne des 20 derniers prix",      "20 trades","Lissage de la tendance"],
    ["Z-Score",    "(valeur - mu) / sigma",             "1 min",    "Anomalie si > 2.5 sigma"],
    ["Var. 1min",  "(prix - prix0) / prix0",            "1 min",    "Performance instantanee"],
    ["Var. 5min",  "(prix - prix0) / prix0",            "5 min",    "Performance moyen terme"],
    ["High/Low",   "max / min des prix",                "1 min",    "Amplitude de la bougie"],
]
story += [table(metrics_data, [2.5*cm, 5.5*cm, 2*cm, 6.5*cm], ROSE), sp(4)]
story += [
    code("Buffer circulaire : max 1000 trades / symbole, eviction TTL 10 minutes"),
    sp(8),
]

story += [h2("4.3 API Server"), sp(3)]
story += [
    body("L'API expose 5 endpoints REST et 5 types d'evenements Socket.IO. Elle maintient "
         "l'etat courant en memoire : dernieres metriques + historique 200 points + 50 anomalies."),
]
api_data = [
    ["Endpoint / Evenement", "Type", "Description"],
    ["GET /api/health",           "REST",      "Sante du service"],
    ["GET /api/metrics",          "REST",      "Toutes les metriques"],
    ["GET /api/metrics/:symbol",  "REST",      "Metriques par paire"],
    ["GET /api/history/:symbol",  "REST",      "Historique 200 points"],
    ["GET /api/anomalies",        "REST",      "50 dernieres anomalies"],
    ["metrics:update",            "Socket.IO", "Push nouvelles metriques"],
    ["anomaly:detected",          "Socket.IO", "Push alerte z-score"],
    ["server:stats",              "Socket.IO", "Stats connexions / msg/s"],
]
story += [table(api_data, [5.5*cm, 2.5*cm, 8.5*cm], BLUE), sp(8), PageBreak()]

# ══════════════════════════════════════════════════════
# 5. DASHBOARD
# ══════════════════════════════════════════════════════
story += [rose_label("dashboard"), h1("5. Dashboard"), hr()]
story += [
    body("Application vanilla HTML/CSS/JS connectee via Socket.IO. Aucun framework front-end "
         "pour minimiser les dependances et maximiser la performance de chargement."),
    sp(6), h2("5.1 Composants"),
    bul("Section hero : prix avec flash vert/rouge, badges variation 1min/5min"),
    bul("4 stat-cards : volume (1min), transactions, high, low"),
    bul("Graphique prix + SMA-20 superposee (Chart.js 4.4, 200 points)"),
    bul("Barres de volume par paire"),
    bul("Flux anomalies en temps reel avec beep AudioContext"),
    bul("Horloge + statut connexion live"),
    sp(8), h2("5.2 Design EFREI"),
    body("Palette brand EFREI officielle : fond navy #163767, accent rose #ff43b8, "
         "bleu #3653a0. Barre gradient EFREI en haut de page. Logos SVG officiels "
         "Bitcoin, Ethereum, Coinbase. Typo Inter (Google Fonts)."),
    sp(6), h2("5.3 Mode demonstration"),
    body("Si le backend est inaccessible apres 3 secondes, le mode demo s'active. "
         "Donnees simulees realistes (BTC ~67k, ETH ~3.5k), mise a jour 800ms. "
         "Badge DEMO rose dans le header."),
    sp(10), PageBreak(),
]

# ══════════════════════════════════════════════════════
# 6. i18n
# ══════════════════════════════════════════════════════
story += [rose_label("internationalisation"), h1("6. Multilinguisme i18n"), hr()]
story += [
    body("Module vanilla JS IIFE (I18n) sans dependance externe. Charge les JSON "
         "depuis i18n/{locale}.json, persiste le choix en localStorage, applique "
         "les traductions via attributs data-i18n."),
    sp(6),
    bul("Francais par defaut, Anglais en option"),
    bul("Attributs data-i18n sur tous les elements statiques"),
    bul("Intl.NumberFormat / Intl.DateTimeFormat pour formatage locale-aware"),
    bul("document.documentElement.lang mis a jour pour accessibilite"),
    bul("aria-pressed sur les boutons FR | EN"),
    sp(10), PageBreak(),
]

# ══════════════════════════════════════════════════════
# 7. SECURITE
# ══════════════════════════════════════════════════════
story += [rose_label("securite"), h1("7. Securite - Production-ready"), hr()]

sec_data = [
    ["Composant", "Protection"],
    ["helmet",             "HTTP headers : CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy"],
    ["express-rate-limit", "100 req / 15min / IP - protection brute-force et DDoS applicatif"],
    ["zod",                "Validation stricte des variables d'environnement - arret si manquante/invalide"],
    ["CORS strict",        "Whitelist explicite des origines - pas de wildcard (*)"],
    ["morgan",             "Logging HTTP avec rotation - aucune stack trace exposee cote client"],
    ["Docker non-root",    "Tous les conteneurs tournent en utilisateur appuser (UID 1000)"],
    [".dockerignore",      "Exclusion des .env, node_modules, secrets des images Docker"],
    ["Secrets env vars",   "Zero secret en dur - .env gitignore, patterns dans .gitignore"],
]
story += [table(sec_data, [3.5*cm, 13*cm], RED_LT), sp(10), PageBreak()]

# ══════════════════════════════════════════════════════
# 8. DEPLOIEMENT
# ══════════════════════════════════════════════════════
story += [rose_label("deploiement"), h1("8. Options de deploiement"), hr()]

deploy_data = [
    ["Option", "Commande", "Usage"],
    ["Lanceur .exe",   "node launcher/src/index.mjs\n(compile : npm run build:win)", "Demo, machines sans Docker Compose"],
    ["Image tout-en-un", "docker run -p 8080:8080 crypto-monitor", "Demo standalone, 1 seul conteneur"],
    ["Docker Compose", "docker-compose up --build -d",              "Developpement, debug, Kafka UI :8090"],
]
story += [table(deploy_data, [3.5*cm, 6.5*cm, 6.5*cm], BLUE), sp(8)]

story += [h2("Variables d'environnement cles")]
env_data = [
    ["Variable", "Defaut", "Description"],
    ["KAFKA_BROKERS",            "localhost:9092", "Bootstrap servers Kafka"],
    ["KAFKA_TOPIC_TRADES",       "crypto-trades",  "Topic transactions brutes"],
    ["KAFKA_TOPIC_METRICS",      "crypto-metrics", "Topic metriques calculees"],
    ["API_PORT",                 "3001",           "Port du serveur API"],
    ["SMA_WINDOW",               "20",             "Fenetre SMA (nombre de trades)"],
    ["ANOMALY_ZSCORE_THRESHOLD", "2.5",            "Seuil z-score alerte"],
    ["HISTORY_WINDOW_SECONDS",   "300",            "Retention historique (5 min)"],
]
story += [table(env_data, [5*cm, 3.5*cm, 8*cm]), sp(10), PageBreak()]

# ══════════════════════════════════════════════════════
# 9. BILAN
# ══════════════════════════════════════════════════════
story += [rose_label("bilan"), h1("9. Bilan et perspectives"), hr()]
story += [
    h2("Realise"), sp(3),
    bul("Pipeline Kafka bout-en-bout fonctionnel (WebSocket -> Kafka -> analytics -> push)"),
    bul("3 services TypeScript avec typage strict"),
    bul("Dashboard EFREI-branded avec Chart.js, i18n FR/EN, mode demo offline"),
    bul("Securite production : helmet, rate-limit, zod, CORS strict, non-root Docker"),
    bul("3 options deploiement : Docker Compose, image tout-en-un, lanceur .exe"),
    bul("Projet realise a 2 personnes pour une consigne prevue a 4"),
    sp(10), h2("Perspectives"), sp(3),
    bul("Ajout de paires : SOL/USDT, BNB/USDT, XRP/USDT"),
    bul("Alertes email/SMS via Kafka Connect (plugin SMTP / Twilio)"),
    bul("Stockage historique : InfluxDB ou TimescaleDB pour le backtesting"),
    bul("Kubernetes + Helm chart pour la scalabilite horizontale"),
    bul("Authentification JWT sur les endpoints REST et Socket.IO"),
    bul("Tests d'integration Testcontainers (Kafka reel en CI/CD)"),
    sp(20), hr(NAVY),
    Paragraph("Crypto Market Monitor - Rapport Technique", ST_CAPTION),
    Paragraph("Adam Beloucif, Emilien Morice - M1 Data Engineering & IA - EFREI Paris - 2025-2026", ST_CAPTION),
]

doc.build(story)
print("PDF v2 saved -> " + OUT)
