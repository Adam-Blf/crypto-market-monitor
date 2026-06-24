"""
Crypto Market Monitor - Rapport Technique PDF
M1 Data Engineering & IA - EFREI Paris - Module Real-Time Engineering 2025-2026
Adam Beloucif, Emilien Morice
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto-market-monitor-rapport-technique.pdf")

# Palette
NAVY   = colors.HexColor("#0A0E1A")
AMBER  = colors.HexColor("#F59E0B")
PURPLE = colors.HexColor("#8B5CF6")
WHITE  = colors.HexColor("#F8FAFC")
MUTED  = colors.HexColor("#94A3B8")
GREEN  = colors.HexColor("#10B981")
CARD   = colors.HexColor("#111827")
DARK2  = colors.HexColor("#1E293B")

PAGE_W, PAGE_H = A4

doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=2.5*cm,
    bottomMargin=2*cm,
    title="Rapport Technique - Crypto Market Monitor",
    author="Adam Beloucif, Emilien Morice",
    subject="M1 Real-Time Engineering - EFREI Paris 2025-2026",
)

styles = getSampleStyleSheet()

def sty(name, **kwargs):
    base = ParagraphStyle(name, parent=styles['Normal'], **kwargs)
    return base

ST_TITLE    = sty("title",    fontSize=28, textColor=AMBER, alignment=TA_CENTER,
                  spaceAfter=6, leading=32, fontName="Helvetica-Bold")
ST_SUBTITLE = sty("subtitle", fontSize=13, textColor=MUTED, alignment=TA_CENTER,
                  spaceAfter=4, leading=17)
ST_H1       = sty("h1",       fontSize=18, textColor=AMBER, spaceBefore=14,
                  spaceAfter=6, leading=22, fontName="Helvetica-Bold")
ST_H2       = sty("h2",       fontSize=13, textColor=WHITE, spaceBefore=10,
                  spaceAfter=4, leading=17, fontName="Helvetica-Bold")
ST_BODY     = sty("body",     fontSize=10, textColor=WHITE, spaceAfter=4,
                  leading=15, alignment=TA_JUSTIFY)
ST_BODY_L   = sty("body_left",fontSize=10, textColor=WHITE, spaceAfter=4, leading=15)
ST_BULLET   = sty("bullet",   fontSize=10, textColor=WHITE, spaceAfter=2,
                  leading=14, leftIndent=12, bulletIndent=0)
ST_CODE     = sty("code",     fontSize=9,  textColor=GREEN, fontName="Courier",
                  spaceAfter=4, leading=13, backColor=CARD, leftIndent=8)
ST_CAPTION  = sty("caption",  fontSize=9,  textColor=MUTED, alignment=TA_CENTER,
                  spaceAfter=6, leading=12)
ST_MUTED    = sty("muted",    fontSize=9,  textColor=MUTED, spaceAfter=3, leading=13)
ST_AMBER    = sty("amber",    fontSize=11, textColor=AMBER, fontName="Helvetica-Bold",
                  spaceBefore=6, spaceAfter=3, leading=15)

def hr():
    return HRFlowable(width="100%", thickness=1, color=AMBER, spaceAfter=8, spaceBefore=4)

def bullet(text):
    return Paragraph(f"  - {text}", ST_BULLET)

def h1(text):
    return Paragraph(text, ST_H1)

def h2(text):
    return Paragraph(text, ST_H2)

def body(text):
    return Paragraph(text, ST_BODY)

def body_l(text):
    return Paragraph(text, ST_BODY_L)

def sp(n=6):
    return Spacer(1, n)

story = []

# ======================================================
# Couverture
# ======================================================
story += [
    sp(60),
    Paragraph("CRYPTO MARKET MONITOR", ST_TITLE),
    hr(),
    Paragraph("Rapport Technique", ST_SUBTITLE),
    sp(4),
    Paragraph("Systeme de surveillance des marches crypto en temps reel", ST_SUBTITLE),
    sp(30),
]

meta_data = [
    ["Auteurs",    "Adam Beloucif, Emilien Morice"],
    ["Formation",  "M1 Data Engineering & IA - EFREI Paris"],
    ["Module",     "Real-Time Engineering (S9 - 2025-2026)"],
    ["Date",       "Juin 2026"],
    ["Note",       "Projet realise a 2 personnes (consigne prevue pour 4)"],
]
meta_table = Table(meta_data, colWidths=[4*cm, 12*cm])
meta_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), CARD),
    ("TEXTCOLOR",  (0,0), (0,-1), AMBER),
    ("TEXTCOLOR",  (1,0), (1,-1), WHITE),
    ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 10),
    ("PADDING",    (0,0), (-1,-1), 7),
    ("GRID",       (0,0), (-1,-1), 0.3, DARK2),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [CARD, DARK2]),
]))
story += [meta_table, sp(20)]
story.append(PageBreak())

# ======================================================
# 1. Introduction
# ======================================================
story += [h1("1. Introduction"), hr()]
story += [
    body("Ce rapport presente l'architecture, les choix techniques et les resultats du projet Crypto Market Monitor, "
         "realise dans le cadre du module Real-Time Engineering du M1 Data Engineering et IA de l'EFREI Paris (2025-2026)."),
    sp(),
    body("L'objectif est de construire un pipeline de streaming bout-en-bout qui ingere des transactions crypto en direct "
         "depuis les flux WebSocket de Binance et Coinbase, les traite via Apache Kafka, calcule des metriques analytiques "
         "en fenetre glissante (VWAP, SMA-20, detection d'anomalies par z-score) et pousse les resultats vers un dashboard "
         "live via Socket.IO."),
    sp(),
    body("Le projet a ete realise en binome alors que la consigne prevoyait une equipe de quatre personnes."),
    sp(12),
]

# ======================================================
# 2. Architecture
# ======================================================
story += [h1("2. Architecture du systeme"), hr(),
    body("Le systeme suit un pattern pipeline lineaire : collecte -> streaming -> traitement -> diffusion. "
         "Chaque etape est isolee dans un service independant, communiquant exclusivement via Kafka ou Socket.IO."),
    sp(6),
    h2("2.1 Composants"),
]

comps = [
    ["Service", "Role", "Technologies"],
    ["Ingester",   "Clients WebSocket Binance + Coinbase, normalisation, production Kafka", "Node.js, TypeScript, ws, kafkajs"],
    ["Kafka",      "Tampon de decoupling, tolerance aux pannes, multi-consommateurs",      "Apache Kafka 3.7 KRaft"],
    ["Processor",  "Consomme les transactions, calcule VWAP SMA z-score",                  "Node.js, TypeScript, kafkajs"],
    ["API",        "Agregation, endpoints REST, push WebSocket clients",                    "Express, Socket.IO, helmet"],
    ["Dashboard",  "Graphiques prix/volume, flux anomalies, i18n FR/EN",                  "HTML, CSS, JS, Chart.js 4"],
]
comp_table = Table(comps, colWidths=[3*cm, 8.5*cm, 5*cm])
comp_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK2),
    ("TEXTCOLOR",  (0,0), (-1,0), AMBER),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND", (0,1), (-1,-1), CARD),
    ("TEXTCOLOR",  (0,1), (-1,-1), WHITE),
    ("FONTSIZE",   (0,0), (-1,-1), 9),
    ("PADDING",    (0,0), (-1,-1), 6),
    ("GRID",       (0,0), (-1,-1), 0.3, DARK2),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [CARD, DARK2]),
]))
story += [comp_table, sp(10)]

story += [
    h2("2.2 Flux de donnees"),
    body("Sources WebSocket -> Ingester (normalisation) -> Kafka topic crypto-trades -> "
         "Processor (VWAP, SMA-20, z-score) -> Kafka topic crypto-metrics -> "
         "API Server -> Socket.IO -> Dashboard (push temps reel)."),
    sp(),
    body("Le decoupling par Kafka permet aux producteurs et consommateurs de fonctionner a des debits differents "
         "sans perte de donnees. La retention est configuree a 1 heure par defaut. Le partitionnement se fait "
         "par symbole (cle = symbole), garantissant l'ordre des messages par paire de trading."),
    sp(10),
]
story.append(PageBreak())

# ======================================================
# 3. Apache Kafka KRaft
# ======================================================
story += [h1("3. Apache Kafka - Mode KRaft"), hr(),
    body("Le projet utilise Kafka 3.7 en mode KRaft, qui elimine la dependance a Zookeeper. "
         "Les metadonnees du cluster sont gerees en interne via le protocole Raft, ce qui simplifie "
         "le deploiement (1 conteneur + 1 volume) et reduit la surface d'attaque."),
    sp(),
    h2("3.1 Image Docker"),
    Paragraph("bitnami/kafka:3.7  (KRaft pre-configure, variable KAFKA_CFG_PROCESS_ROLES=broker,controller)", ST_CODE),
    sp(),
    h2("3.2 Topics"),
]

topics = [
    ["Topic", "Description", "Partitions", "Retention"],
    ["crypto-trades",  "Transactions brutes normalisees (interface Trade)",   "3", "1h"],
    ["crypto-metrics", "Metriques calculees par symbole (VWAP, SMA, etc.)",  "3", "1h"],
]
t_table = Table(topics, colWidths=[4*cm, 8.5*cm, 2.5*cm, 2*cm])
t_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK2),
    ("TEXTCOLOR",  (0,0), (-1,0), AMBER),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND", (0,1), (-1,-1), CARD),
    ("TEXTCOLOR",  (0,1), (-1,-1), WHITE),
    ("FONTSIZE",   (0,0), (-1,-1), 9),
    ("PADDING",    (0,0), (-1,-1), 6),
    ("GRID",       (0,0), (-1,-1), 0.3, DARK2),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [CARD, DARK2]),
]))
story += [t_table, sp(10)]

# ======================================================
# 4. Services
# ======================================================
story += [h1("4. Services Node.js TypeScript"), hr()]

story += [
    h2("4.1 Ingester"),
    body("L'ingester maintient des connexions WebSocket persistantes vers Binance et Coinbase. "
         "Chaque message entrant est deserialise, normalise vers l'interface Trade, puis publie "
         "sur le topic crypto-trades avec comme cle de partition le symbole."),
    sp(4),
    bullet("Binance : stream combine BTC/USDT + ETH/USDT via wss://stream.binance.com:9443/stream"),
    bullet("Coinbase : BTC-USD via wss://advanced-trade-ws.coinbase.com"),
    bullet("Reconnexion auto : backoff exponentiel, max 10 tentatives, delai max 30 secondes"),
    bullet("Arret propre SIGTERM/SIGINT avec vidage du buffer Kafka"),
    sp(8),
    h2("4.2 Processor"),
    body("Le processor consomme le topic crypto-trades et maintient un buffer circulaire en memoire "
         "(max 1000 trades/symbole, eviction TTL 10 minutes) par symbole. A chaque nouveau trade, "
         "il recalcule les metriques de la fenetre courante et publie le resultat sur crypto-metrics."),
    sp(6),
]

metrics = [
    ["Metrique", "Formule", "Fenetre", "Objectif"],
    ["VWAP",       "sum(prix x qte) / sum(qte)",       "1 minute",  "Prix moyen pondere par volume"],
    ["SMA-20",     "moyenne des 20 derniers prix",      "20 trades", "Lissage de la tendance"],
    ["Z-Score",    "(valeur - mu) / sigma",             "1 minute",  "Detection d'anomalie (seuil 2.5)"],
    ["Var. 1min",  "(prix - prix_0) / prix_0",          "1 minute",  "Performance instantanee"],
    ["Var. 5min",  "(prix - prix_0) / prix_0",          "5 minutes", "Performance moyen terme"],
    ["High/Low",   "max / min des prix",                "1 minute",  "Amplitude de la bougie"],
]
m_table = Table(metrics, colWidths=[2.5*cm, 5*cm, 2.5*cm, 6.5*cm])
m_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK2),
    ("TEXTCOLOR",  (0,0), (-1,0), AMBER),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND", (0,1), (-1,-1), CARD),
    ("TEXTCOLOR",  (0,1), (0,-1), WHITE),
    ("TEXTCOLOR",  (1,1), (1,-1), GREEN),
    ("TEXTCOLOR",  (2,1), (-1,-1), WHITE),
    ("FONTSIZE",   (0,0), (-1,-1), 9),
    ("FONTNAME",   (1,1), (1,-1), "Courier"),
    ("PADDING",    (0,0), (-1,-1), 6),
    ("GRID",       (0,0), (-1,-1), 0.3, DARK2),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [CARD, DARK2]),
]))
story += [m_table, sp(10)]
story.append(PageBreak())

story += [
    h2("4.3 API Server"),
    body("L'API Server consomme le topic crypto-metrics, maintient l'etat courant en memoire "
         "(dernieres metriques par symbole + historique 200 points + 50 dernieres anomalies) "
         "et expose deux interfaces :"),
    sp(4),
    bullet("REST : 5 endpoints GET documentes (health, metrics, metrics/:symbol, history/:symbol, anomalies)"),
    bullet("WebSocket : Socket.IO v4.7 avec 5 types d'evenements push (metrics:update, anomaly:detected, server:stats, initial:state, subscribe:symbol)"),
    bullet("Securite : helmet, express-rate-limit (100 req/15min/IP), CORS strict, morgan logging"),
    sp(10),
]

# ======================================================
# 5. Dashboard
# ======================================================
story += [h1("5. Dashboard"), hr(),
    body("Le dashboard est une application vanilla HTML/CSS/JS (sans framework) connectee au backend "
         "via Socket.IO. Les metriques sont mises a jour en temps reel par push serveur, sans polling."),
    sp(6),
    h2("5.1 Composants visuels"),
    bullet("Section hero : prix actuel avec flash vert/rouge au changement, badges variation 1min/5min"),
    bullet("Stat-cards : volume (1min), nombre de transactions, high/low de la bougie courante"),
    bullet("Graphique prix : ligne prix + SMA-20 superposee (Chart.js 4.4, 200 points max)"),
    bullet("Graphique volume : barres par paire (BTC-USDT, ETH-USDT, BTC-USD)"),
    bullet("Flux anomalies : liste deroulante avec icone alerte, valeur z-score, beep AudioContext"),
    bullet("Header : horloge temps reel, statut de connexion (live/demo), bascule FR/EN"),
    sp(8),
    h2("5.2 Design system"),
    body("Le design reprend l'identite visuelle de l'EFREI Paris : fond navy (#0A0E1A), accent amber/or "
         "(#F59E0B), typo Inter. Une barre de gradient amber-violet en haut de page sert de signature "
         "institutionnelle. Les logos crypto (Bitcoin, Ethereum, Coinbase) sont des SVG officiels."),
    sp(8),
    h2("5.3 Mode demonstration"),
    body("Si le backend est inaccessible apres 3 secondes (pas de connexion Socket.IO etablie), "
         "le mode demo s'active automatiquement. Des donnees simulees realistes sont injectees "
         "(prix de base BTC ~67k USD, ETH ~3.5k USD, variations aleatoires de +/-0.15%), "
         "avec mise a jour toutes les 800ms. Un badge 'DEMO' ambra s'affiche dans le header."),
    sp(10),
]
story.append(PageBreak())

# ======================================================
# 6. Internationalisation
# ======================================================
story += [h1("6. Internationalisation (i18n)"), hr(),
    body("Le dashboard supporte le francais (langue par defaut) et l'anglais. L'implementation "
         "est un module vanilla JS (IIFE I18n) sans dependance externe."),
    sp(6),
    h2("Principe de fonctionnement"),
    bullet("Chargement asynchrone du fichier i18n/{locale}.json au demarrage"),
    bullet("Tous les elements statiques portent un attribut data-i18n (cle de traduction)"),
    bullet("La langue est persistee dans localStorage sous la cle cmm-locale"),
    bullet("document.documentElement.lang est mis a jour pour les technologies d'assistance"),
    bullet("Les fonctions formatPrice() et formatTime() utilisent l'API Intl pour le formatage locale-aware"),
    sp(10),
]

# ======================================================
# 7. Securite
# ======================================================
story += [h1("7. Securite"), hr()]

sec_items = [
    ("helmet", "Configuration des HTTP response headers : Content-Security-Policy, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy."),
    ("express-rate-limit", "Limite de 100 requetes par fenetre de 15 minutes par adresse IP. Protection contre le brute-force et les attaques DDoS applicatives."),
    ("zod", "Validation stricte des variables d'environnement au demarrage du service. Le processus s'arrete si une variable obligatoire est absente ou invalide."),
    ("CORS strict", "Whitelist explicite des origines autorisees. Pas de wildcard (*) en production."),
    ("morgan", "Logging HTTP avec rotation de fichiers. Aucune stack trace n'est exposee dans les reponses HTTP cote client."),
    ("Docker non-root", "Tous les conteneurs tournent avec un utilisateur applicatif (UID 1000, appuser). Le dossier applicatif appartient a cet utilisateur."),
    (".dockerignore", "Les fichiers .env, node_modules, secrets et fichiers de developpement sont exclus des images Docker."),
    ("Secrets", "Zero secret en dur dans le code source. Toutes les variables sensibles sont injectees via des variables d'environnement. Le .env est gitignore."),
]

for tech, desc in sec_items:
    story += [Paragraph(tech, ST_AMBER), Paragraph(desc, ST_BODY_L), sp(4)]

story.append(PageBreak())

# ======================================================
# 8. Deploiement
# ======================================================
story += [h1("8. Options de deploiement"), hr()]

story += [
    h2("8.1 Docker Compose (recommande pour le developpement)"),
    body("6 services independants avec healthchecks et restart on-failure : kafka, kafka-ui, "
         "ingester, processor, api, dashboard (nginx). Le dashboard est accessible sur le port 8080, "
         "Kafka UI sur 8090, l'API sur 3001."),
    Paragraph("docker-compose up --build -d", ST_CODE),
    sp(8),
    h2("8.2 Image tout-en-un (demonstration / production)"),
    body("Une image Docker unique (all-in-one.Dockerfile) embarque Apache Kafka (Java 17), "
         "les 3 services Node.js et nginx, geres par supervisord. Cela permet un deploiement "
         "en une seule commande sans Docker Compose."),
    Paragraph("docker build -f all-in-one.Dockerfile -t crypto-monitor .", ST_CODE),
    Paragraph("docker run -p 8080:8080 -p 3001:3001 crypto-monitor", ST_CODE),
    sp(8),
    h2("8.3 Lanceur autonome (.exe)"),
    body("Un script Node.js ESM (launcher/src/index.mjs) orchestre le demarrage : verification "
         "de Docker, build des images, attente des healthchecks, ouverture du navigateur, "
         "streaming des logs. Il peut etre compile en executable standalone via pkg :"),
    Paragraph("cd launcher && npm install && npm run build:win  # Windows .exe", ST_CODE),
    Paragraph("cd launcher && npm install && npm run build:linux  # Linux binaire", ST_CODE),
    sp(10),
]

story += [
    h2("8.4 Variables d'environnement cles"),
]
env_vars = [
    ["Variable", "Valeur par defaut", "Description"],
    ["KAFKA_BROKERS",             "localhost:9092", "Serveurs bootstrap Kafka"],
    ["KAFKA_TOPIC_TRADES",        "crypto-trades",  "Topic des transactions brutes"],
    ["KAFKA_TOPIC_METRICS",       "crypto-metrics", "Topic des metriques traitees"],
    ["API_PORT",                  "3001",           "Port du serveur API"],
    ["SMA_WINDOW",                "20",             "Taille de la fenetre SMA"],
    ["ANOMALY_ZSCORE_THRESHOLD",  "2.5",            "Seuil z-score (anomalie)"],
    ["HISTORY_WINDOW_SECONDS",    "300",            "Retention historique (5 min)"],
]
env_table = Table(env_vars, colWidths=[5.5*cm, 3.5*cm, 7.5*cm])
env_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK2),
    ("TEXTCOLOR",  (0,0), (-1,0), AMBER),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND", (0,1), (-1,-1), CARD),
    ("TEXTCOLOR",  (0,1), (0,-1), GREEN),
    ("TEXTCOLOR",  (1,1), (-1,-1), WHITE),
    ("FONTNAME",   (0,1), (0,-1), "Courier"),
    ("FONTNAME",   (1,1), (1,-1), "Courier"),
    ("FONTSIZE",   (0,0), (-1,-1), 9),
    ("PADDING",    (0,0), (-1,-1), 6),
    ("GRID",       (0,0), (-1,-1), 0.3, DARK2),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [CARD, DARK2]),
]))
story += [env_table, sp(10)]
story.append(PageBreak())

# ======================================================
# 9. Conclusion
# ======================================================
story += [h1("9. Bilan et perspectives"), hr(),
    h2("Ce qui a ete realise"),
    bullet("Pipeline Kafka bout-en-bout fonctionnel (ingestion WS -> Kafka -> processing -> dashboard)"),
    bullet("3 services TypeScript avec typage strict et tests unitaires de base"),
    bullet("Dashboard dark theme EFREI avec Chart.js, i18n FR/EN et mode demo offline"),
    bullet("Securite niveau production : helmet, rate-limiting, zod, CORS strict, non-root Docker"),
    bullet("3 options de deploiement : Docker Compose, image tout-en-un, lanceur .exe"),
    bullet("Projet realise a 2 personnes pour une consigne prevue a 4"),
    sp(10),
    h2("Perspectives d'evolution"),
    bullet("Ajout de paires supplementaires : SOL/USDT, BNB/USDT, XRP/USDT"),
    bullet("Alertes email ou SMS via webhook (Kafka Connect + plugin SMTP/Twilio)"),
    bullet("Stockage historique dans InfluxDB ou TimescaleDB pour le backtesting"),
    bullet("Deploiement Kubernetes avec Helm chart pour la scalabilite horizontale"),
    bullet("Authentification JWT pour les endpoints REST et les connexions Socket.IO"),
    bullet("Tests d'integration complets avec Testcontainers (Kafka reel en CI)"),
    sp(20),
    hr(),
    Paragraph("Crypto Market Monitor - Rapport Technique", ST_CAPTION),
    Paragraph("Adam Beloucif, Emilien Morice - M1 Data Engineering & IA - EFREI Paris - 2025-2026", ST_CAPTION),
]

doc.build(story)
print("PDF saved -> " + OUT)
