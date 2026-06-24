"""
Crypto Market Monitor - PDF Technical Report Generator
Authors: Adam Beloucif, Emilien Morice
M1 Data Engineering & IA, EFREI Paris
Module: Real-Time Engineering 2025-2026
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
import io


# ── Color palette ─────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#0F172A')
AMBER  = colors.HexColor('#F59E0B')
PURPLE = colors.HexColor('#8B5CF6')
WHITE  = colors.HexColor('#F8FAFC')
LIGHT  = colors.HexColor('#E2E8F0')
MUTED  = colors.HexColor('#64748B')
GREEN  = colors.HexColor('#10B981')
RED    = colors.HexColor('#EF4444')
DARK_BG = colors.HexColor('#1E293B')
CARD   = colors.HexColor('#F1F5F9')
CODE_BG = colors.HexColor('#F8FAFC')
BORDER = colors.HexColor('#CBD5E1')
TEXT   = colors.HexColor('#1E293B')
HEADING_LINE = colors.HexColor('#E2E8F0')

PAGE_W, PAGE_H = A4


# ── Styles ────────────────────────────────────────────────────────────────
def build_styles():
    styles = getSampleStyleSheet()

    cover_title = ParagraphStyle('CoverTitle',
        fontSize=32, textColor=AMBER, alignment=TA_CENTER,
        fontName='Helvetica-Bold', spaceAfter=8, leading=38)

    cover_sub = ParagraphStyle('CoverSub',
        fontSize=16, textColor=WHITE, alignment=TA_CENTER,
        fontName='Helvetica', spaceAfter=6, leading=22)

    cover_meta = ParagraphStyle('CoverMeta',
        fontSize=11, textColor=colors.HexColor('#94A3B8'), alignment=TA_CENTER,
        fontName='Helvetica', spaceAfter=4, leading=16)

    h1 = ParagraphStyle('H1',
        fontSize=18, textColor=AMBER, spaceBefore=22, spaceAfter=8,
        fontName='Helvetica-Bold', leading=24, borderPad=4)

    h2 = ParagraphStyle('H2',
        fontSize=13, textColor=PURPLE, spaceBefore=16, spaceAfter=6,
        fontName='Helvetica-Bold', leading=18)

    h3 = ParagraphStyle('H3',
        fontSize=11, textColor=TEXT, spaceBefore=10, spaceAfter=4,
        fontName='Helvetica-Bold', leading=15)

    body = ParagraphStyle('Body',
        fontSize=10, textColor=TEXT, leading=16, alignment=TA_JUSTIFY,
        fontName='Helvetica', spaceAfter=6)

    body_left = ParagraphStyle('BodyLeft',
        fontSize=10, textColor=TEXT, leading=16, alignment=TA_LEFT,
        fontName='Helvetica', spaceAfter=4)

    bullet = ParagraphStyle('Bullet',
        fontSize=10, textColor=TEXT, leading=15, alignment=TA_LEFT,
        fontName='Helvetica', leftIndent=16, spaceAfter=3,
        bulletIndent=4)

    code = ParagraphStyle('Code',
        fontSize=8.5, fontName='Courier', backColor=CODE_BG,
        leftIndent=16, rightIndent=16, spaceBefore=4, spaceAfter=4,
        leading=13, textColor=colors.HexColor('#0F172A'),
        borderColor=BORDER, borderWidth=0.5, borderPad=8)

    code_inline = ParagraphStyle('CodeInline',
        fontSize=9, fontName='Courier', textColor=colors.HexColor('#0F172A'),
        backColor=CARD)

    caption = ParagraphStyle('Caption',
        fontSize=8, textColor=MUTED, alignment=TA_CENTER,
        fontName='Helvetica-Oblique', spaceAfter=8)

    toc_entry = ParagraphStyle('TOCEntry',
        fontSize=10, textColor=TEXT, leading=18, fontName='Helvetica',
        leftIndent=0, spaceAfter=2)

    toc_h2 = ParagraphStyle('TOCH2',
        fontSize=9.5, textColor=MUTED, leading=16, fontName='Helvetica',
        leftIndent=16, spaceAfter=1)

    return {
        'cover_title': cover_title,
        'cover_sub': cover_sub,
        'cover_meta': cover_meta,
        'h1': h1, 'h2': h2, 'h3': h3,
        'body': body, 'body_left': body_left,
        'bullet': bullet, 'code': code,
        'code_inline': code_inline,
        'caption': caption,
        'toc_entry': toc_entry,
        'toc_h2': toc_h2,
    }


S = build_styles()


# ── Helpers ───────────────────────────────────────────────────────────────

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=HEADING_LINE,
                      spaceAfter=8, spaceBefore=4)


def sp(h=0.3):
    return Spacer(1, h * cm)


def h1(text):
    return Paragraph(text, S['h1'])


def h2(text):
    return Paragraph(text, S['h2'])


def h3(text):
    return Paragraph(text, S['h3'])


def p(text):
    return Paragraph(text, S['body'])


def pl(text):
    return Paragraph(text, S['body_left'])


def bullet(text, indent=0):
    style = ParagraphStyle('BulletDyn',
        parent=S['bullet'], leftIndent=16 + indent * 12)
    return Paragraph(f"- {text}", style)


def code_block(text):
    lines = text.strip().split('\n')
    safe = '<br/>'.join(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for line in lines)
    return Paragraph(safe, S['code'])


def make_table(data, col_widths, header_bg=AMBER, stripe_color=CARD):
    """Build a styled table."""
    t = Table(data, colWidths=col_widths)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE if header_bg == NAVY else NAVY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ROWBACKGROUND', (0, 1), (-1, -1), [WHITE, CARD]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUND', (0, 1), (-1, -1), [WHITE, colors.HexColor('#F8FAFC')]),
    ]
    t.setStyle(TableStyle(style))
    return t


def amber_badge(text):
    """Small amber inline badge."""
    style = ParagraphStyle('Badge',
        fontSize=8, fontName='Helvetica-Bold',
        backColor=colors.HexColor('#FEF3C7'),
        textColor=colors.HexColor('#92400E'),
        borderColor=AMBER, borderWidth=0.5, borderPad=3)
    return Paragraph(text, style)


# ── Page template ─────────────────────────────────────────────────────────

class ReportCanvas(pdfcanvas.Canvas):
    """Custom canvas for header/footer on content pages."""

    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self._page_number = 0

    def showPage(self):
        self._page_number += 1
        self.draw_page_decoration()
        super().showPage()

    def save(self):
        self.draw_page_decoration()
        super().save()

    def draw_page_decoration(self):
        pn = self._page_number
        if pn == 1:
            return  # Cover page - no header/footer
        w, h = A4
        # Header bar
        self.setFillColor(NAVY)
        self.rect(0, h - 1.2 * cm, w, 1.2 * cm, fill=1, stroke=0)
        # Header amber accent
        self.setFillColor(AMBER)
        self.rect(0, h - 0.15 * cm, w, 0.15 * cm, fill=1, stroke=0)
        # Header text
        self.setFillColor(colors.HexColor('#94A3B8'))
        self.setFont('Helvetica', 8)
        self.drawString(2 * cm, h - 0.85 * cm, 'Crypto Market Monitor - Rapport Technique')
        self.setFillColor(AMBER)
        self.drawRightString(w - 2 * cm, h - 0.85 * cm,
                             'M1 Data Engineering & IA - EFREI Paris 2025-2026')
        # Footer line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.3)
        self.line(2 * cm, 1.5 * cm, w - 2 * cm, 1.5 * cm)
        # Footer text
        self.setFillColor(MUTED)
        self.setFont('Helvetica', 8)
        self.drawString(2 * cm, 0.9 * cm, 'Adam Beloucif, Emilien Morice')
        self.drawCentredString(w / 2, 0.9 * cm, 'Confidentiel - Usage pedagogique uniquement')
        self.drawRightString(w - 2 * cm, 0.9 * cm, f'Page {pn - 1}')


# ── Content sections ──────────────────────────────────────────────────────

def cover_page(story):
    """Page de couverture."""
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("CRYPTO MARKET MONITOR", S['cover_title']))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Rapport Technique", ParagraphStyle('ST',
        fontSize=20, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica',
        spaceAfter=6)))
    story.append(Spacer(1, 0.6 * cm))

    # Separator
    story.append(HRFlowable(width='60%', thickness=1.5, color=AMBER,
                             spaceAfter=16, spaceBefore=8))

    story.append(Paragraph(
        "Systeme de surveillance de marches crypto en temps reel",
        ParagraphStyle('Tagline', fontSize=14, textColor=colors.HexColor('#CBD5E1'),
                       alignment=TA_CENTER, fontName='Helvetica-Oblique',
                       spaceAfter=4)))
    story.append(Spacer(1, 1.5 * cm))

    # Info box
    info_data = [
        ['Auteurs', 'Adam Beloucif, Emilien Morice'],
        ['Formation', 'M1 Data Engineering & IA'],
        ['Etablissement', 'EFREI Paris - Universite Paris-Pantheon-Assas'],
        ['Module', 'Real-Time Engineering'],
        ['Annee academique', '2025-2026'],
        ['Date de rendu', 'Juin 2026'],
    ]
    info_table = Table(info_data, colWidths=[5 * cm, 10 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), DARK_BG),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (0, -1), AMBER),
        ('TEXTCOLOR', (1, 0), (1, -1), TEXT),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1.5 * cm))
    story.append(HRFlowable(width='60%', thickness=0.5, color=MUTED,
                             spaceAfter=12, spaceBefore=8))
    story.append(Paragraph(
        "Note: Projet realise par 2 personnes alors que le cahier des charges prevoyait une equipe de 4.",
        ParagraphStyle('Note', fontSize=9, textColor=MUTED, alignment=TA_CENTER,
                       fontName='Helvetica-Oblique')))
    story.append(PageBreak())


def toc_page(story):
    """Table des matieres."""
    story.append(h1("Table des matieres"))
    story.append(hr())
    story.append(sp(0.3))

    toc_entries = [
        ("1.", "Introduction", None),
        ("", "1.1 Contexte et objectifs", None),
        ("", "1.2 Contraintes du projet", None),
        ("2.", "Architecture globale", None),
        ("", "2.1 Vue d'ensemble", None),
        ("", "2.2 Flux de donnees", None),
        ("", "2.3 Choix techniques", None),
        ("3.", "Apache Kafka - Mode KRaft", None),
        ("", "3.1 Architecture KRaft", None),
        ("", "3.2 Topics et partitionnement", None),
        ("4.", "Service Ingester", None),
        ("", "4.1 Sources WebSocket", None),
        ("", "4.2 Normalisation des donnees", None),
        ("", "4.3 Strategie de reconnexion", None),
        ("5.", "Service Processor - Analytique", None),
        ("", "5.1 VWAP", None),
        ("", "5.2 SMA-20", None),
        ("", "5.3 Detection d'anomalies Z-Score", None),
        ("6.", "Service API", None),
        ("", "6.1 Endpoints REST", None),
        ("", "6.2 Evenements Socket.IO", None),
        ("7.", "Dashboard", None),
        ("", "7.1 Stack frontend", None),
        ("", "7.2 Graphiques Chart.js", None),
        ("8.", "Securite", None),
        ("9.", "Multilinguisme - Module i18n", None),
        ("10.", "Deploiement Docker Compose", None),
        ("11.", "Tests et validation", None),
        ("12.", "Bilan et perspectives", None),
        ("13.", "Conclusion", None),
    ]

    for num, title, page in toc_entries:
        if num:
            style = ParagraphStyle('TOCMain', fontSize=10, textColor=TEXT,
                                   leading=20, fontName='Helvetica-Bold',
                                   leftIndent=0, spaceAfter=2)
            story.append(Paragraph(f"{num}  {title}", style))
        else:
            style = ParagraphStyle('TOCSub', fontSize=9.5, textColor=MUTED,
                                   leading=17, fontName='Helvetica',
                                   leftIndent=20, spaceAfter=1)
            story.append(Paragraph(title, style))

    story.append(PageBreak())


def section_introduction(story):
    story.append(h1("1. Introduction"))
    story.append(hr())

    story.append(h2("1.1 Contexte et objectifs"))
    story.append(p(
        "Les marches des cryptomonnaies sont caracterises par une volatilite extreme et des volumes "
        "de transactions considerables, generes 24h/24 par des milliers d'acteurs repartis dans le monde. "
        "Cette realite rend indispensable la mise en place d'outils de surveillance capables de traiter "
        "les donnees en temps reel, de calculer des indicateurs financiers pertinents et de detecter "
        "automatiquement les comportements anormaux du marche."
    ))
    story.append(p(
        "Le projet Crypto Market Monitor repond a ce besoin en implementant un pipeline de traitement "
        "de donnees en temps reel complet, depuis la collecte des flux WebSocket jusqu'a la visualisation "
        "sur un dashboard interactif. L'objectif pedagogique est de mettre en pratique les concepts "
        "fondamentaux du Real-Time Engineering: ingestion de flux, bus de messages, traitement en "
        "continu et interface utilisateur reactive."
    ))

    story.append(h2("1.2 Contraintes du projet"))
    story.append(p(
        "Ce projet a ete realise dans le cadre du module Real-Time Engineering de la formation "
        "M1 Data Engineering & IA a l'EFREI Paris. La contrainte principale a ete de mener "
        "a bien un projet prevu pour une equipe de 4 personnes avec seulement 2 etudiants: "
        "Adam Beloucif et Emilien Morice. Cette contrainte a necessite des choix architecturaux "
        "pragmatiques tout en maintenant un niveau de qualite professionnel."
    ))
    story.append(sp(0.2))
    for item in [
        "Equipe reduite: 2 personnes sur un projet calibre pour 4",
        "Stack imposee: Apache Kafka obligatoire comme bus de messages",
        "TypeScript: tout le code Node.js en TypeScript strict",
        "Deploiement Docker: chaque service dockerise avec healthchecks",
        "Temps reel: latence end-to-end inferieure a 500 ms",
    ]:
        story.append(bullet(item))
    story.append(PageBreak())


def section_architecture(story):
    story.append(h1("2. Architecture globale"))
    story.append(hr())

    story.append(h2("2.1 Vue d'ensemble"))
    story.append(p(
        "L'architecture suit un pattern pipeline en etoile, avec Kafka comme backbone central "
        "qui decouple les producteurs (ingester) des consommateurs (processor, API). "
        "Chaque service est independant, deployable separement et communique exclusivement "
        "via les topics Kafka ou les interfaces HTTP/WebSocket exposees."
    ))

    arch_diagram = [
        "    +------------------+     +------------+     +----------+",
        "    |   Binance WS     | --> |            |     |          |",
        "    | BTC/USDT ETH/USDT|     |  INGESTER  | --> |  KAFKA   |",
        "    +------------------+     |            |     | (KRaft)  |",
        "                             | TypeScript |     |          |",
        "    +------------------+     |  Node.js   |     | topics:  |",
        "    |   Coinbase WS    | --> |            |     | -trades  |",
        "    |    BTC-USD       |     +------------+     | -metrics |",
        "    +------------------+                        |          |",
        "                                                +----+-----+",
        "                                                     |",
        "                                          +----------v---------+",
        "                                          |    PROCESSOR       |",
        "                                          |  VWAP, SMA, Z-Score|",
        "                                          +----------+---------+",
        "                                                     |",
        "                                          +----------v---------+",
        "                                          |   API Express      |",
        "                                          | REST + Socket.IO   |",
        "                                          +----------+---------+",
        "                                                     |",
        "                                          +----------v---------+",
        "                                          |   DASHBOARD        |",
        "                                          | HTML/CSS/JS vanille|",
        "                                          | Chart.js + i18n    |",
        "                                          +--------------------+",
    ]
    story.append(code_block('\n'.join(arch_diagram)))
    story.append(Paragraph("Figure 1 - Architecture pipeline Crypto Market Monitor", S['caption']))

    story.append(h2("2.2 Flux de donnees"))
    steps = [
        ("Collecte", "Les exchanges Binance (BTC/USDT, ETH/USDT) et Coinbase (BTC-USD) publient "
         "des trades en continu via WebSocket. Chaque message contient le prix, la quantite "
         "echangee et l'horodatage."),
        ("Normalisation", "Le service Ingester traduit les formats proprietaires de chaque exchange "
         "vers une interface Trade unifiee (symbol, price, qty, ts, exchange) avant de publier "
         "dans le topic Kafka crypto-trades."),
        ("Calcul analytique", "Le Processor consomme crypto-trades, maintient des buffers circulaires "
         "par symbole et calcule en continu VWAP, SMA-20, z-score et variations de prix. "
         "Les resultats sont publies dans crypto-metrics."),
        ("Distribution", "L'API Express consomme crypto-metrics, maintient un ring buffer de 500 "
         "entrees par symbole en memoire et pousse les mises a jour via Socket.IO a tous les clients "
         "connectes qui ont souscrit au symbole correspondant."),
        ("Visualisation", "Le Dashboard HTML/CSS/JS reçoit les donnees en temps reel, met a jour "
         "les graphiques Chart.js et declenche des alertes visuelles et sonores en cas d'anomalie."),
    ]
    for i, (step, desc) in enumerate(steps):
        story.append(Paragraph(
            f"<b>Etape {i+1} - {step}:</b> {desc}",
            ParagraphStyle('Step', parent=S['body'], leftIndent=0, spaceAfter=5)
        ))

    story.append(h2("2.3 Choix techniques"))
    choices_data = [
        ['Composant', 'Technologie choisie', 'Justification'],
        ['Bus de messages', 'Apache Kafka KRaft', 'Impose par le cahier des charges, robustesse, decoupling'],
        ['Runtime', 'Node.js 20 + TypeScript', 'Typage fort, ecosysteme riche, I/O async natif'],
        ['WebSocket client', 'ws (npm)', 'Legere, fiable, reconnexion maitrisable'],
        ['Kafka client', 'kafkajs', 'Mature, TypeScript-first, retry config fine'],
        ['API', 'Express 4 + Socket.IO 4', 'Standard industrie, push facile via Socket.IO'],
        ['Frontend', 'HTML/CSS/JS vanilla', 'Zero build step, bundle minimal, maintenable'],
        ['Graphiques', 'Chart.js 4', 'Performant, declaratif, mise a jour incrementale'],
        ['Conteneurisation', 'Docker Compose', 'Reproductibilite, isolation, healthchecks'],
    ]
    story.append(make_table(choices_data,
                            [4.5*cm, 4.5*cm, 8.5*cm], header_bg=NAVY))
    story.append(Paragraph("Tableau 1 - Choix technologiques", S['caption']))
    story.append(PageBreak())


def section_kafka(story):
    story.append(h1("3. Apache Kafka - Mode KRaft"))
    story.append(hr())

    story.append(h2("3.1 Architecture KRaft"))
    story.append(p(
        "Kafka 3.x introduit le mode KRaft (Kafka Raft Metadata Mode), qui integre la gestion "
        "des metadonnees directement dans le broker Kafka, eliminant ainsi la dependance historique "
        "a Apache Zookeeper. Dans ce projet, Kafka est configure en mode KRaft single-node, "
        "ce qui simplifie considerablement le deploiement Docker tout en conservant toutes les "
        "fonctionnalites necessaires pour un environnement de developpement."
    ))
    story.append(p(
        "Le broker joue simultanement les roles de controller et de broker, ce qui est acceptable "
        "en contexte de developpement ou de charge moderee. En production, une configuration "
        "multi-broker avec quorum Raft dedie serait recommandee."
    ))

    story.append(h2("3.2 Topics et partitionnement"))
    topics_data = [
        ['Topic', 'Partitions', 'Retention', 'Replication', 'Usage'],
        ['crypto-trades', '3', '7 jours', '1', 'Trades bruts normalises depuis l\'ingester'],
        ['crypto-metrics', '3', '1 jour', '1', 'Metriques calculees par le processor'],
    ]
    story.append(make_table(topics_data,
                            [3.5*cm, 2.2*cm, 2.2*cm, 2.5*cm, 7.1*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 2 - Configuration des topics Kafka", S['caption']))

    story.append(h3("Partitionnement par symbole"))
    story.append(p(
        "Les messages sont partitionnes par cle (symbol). Cette strategie garantit que tous les "
        "trades d'un meme symbole (ex: BTC/USDT) sont traites sequentiellement par le meme "
        "processor, preservant ainsi l'ordre necessaire aux calculs de series temporelles "
        "(VWAP, SMA)."
    ))

    story.append(h3("Configuration Docker"))
    story.append(code_block(
        "# Variables d'environnement Kafka (docker-compose.yml)\n"
        "KAFKA_NODE_ID: 1\n"
        "KAFKA_PROCESS_ROLES: broker,controller\n"
        "KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093\n"
        "KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093\n"
        "KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092\n"
        "KAFKA_AUTO_CREATE_TOPICS_ENABLE: true\n"
        "KAFKA_LOG_RETENTION_HOURS: 168\n"
        "KAFKA_NUM_PARTITIONS: 3"
    ))
    story.append(PageBreak())


def section_ingester(story):
    story.append(h1("4. Service Ingester"))
    story.append(hr())

    story.append(h2("4.1 Sources WebSocket"))
    story.append(p(
        "Le service Ingester maintient simultanement trois connexions WebSocket persistantes "
        "vers les exchanges Binance et Coinbase. Chaque exchange a ses propres specificites "
        "de protocole, notamment le format des messages et la methode de souscription aux streams."
    ))
    sources_data = [
        ['Exchange', 'URL WebSocket', 'Symboles', 'Format'],
        ['Binance', 'wss://stream.binance.com:9443/ws', 'btcusdt@trade, ethusdt@trade', 'JSON aggtrade'],
        ['Coinbase', 'wss://advanced-trade-ws.coinbase.com', 'BTC-USD', 'JSON match'],
    ]
    story.append(make_table(sources_data,
                            [2.5*cm, 6*cm, 4.5*cm, 4.5*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 3 - Sources de donnees WebSocket", S['caption']))

    story.append(h2("4.2 Normalisation des donnees"))
    story.append(p(
        "Chaque exchange publie ses trades dans un format JSON propre. Le service Ingester "
        "normalise ces messages heterogenes vers une interface Trade unifiee avant toute "
        "publication vers Kafka:"
    ))
    story.append(code_block(
        "interface Trade {\n"
        "  symbol:   string   // ex: BTC/USDT\n"
        "  price:    number   // prix en USD\n"
        "  qty:      number   // quantite echangee\n"
        "  ts:       number   // timestamp en ms (Unix epoch)\n"
        "  exchange: string   // 'binance' | 'coinbase'\n"
        "}"
    ))
    story.append(p(
        "La normalisation inclut: conversion des champs string vers number (parseFloat), "
        "harmonisation des symboles (BTC-USD -> BTC/USDT), et horodatage normalise en millisecondes."
    ))

    story.append(h2("4.3 Strategie de reconnexion"))
    story.append(p(
        "Les connexions WebSocket peuvent etre interrompues pour diverses raisons: problemes "
        "reseau transitoires, maintenance des exchanges, timeouts. Une strategie de reconnexion "
        "robuste est indispensable pour un pipeline de production. Le service Ingester "
        "implementee un backoff exponentiel avec jitter:"
    ))
    story.append(code_block(
        "// Formule de backoff exponentiel avec jitter\n"
        "const delay = Math.min(\n"
        "  BASE_DELAY * Math.pow(2, attempt),\n"
        "  MAX_DELAY\n"
        ") + Math.random() * JITTER\n"
        "\n"
        "// Parametres\n"
        "const BASE_DELAY = 1000   // 1 seconde\n"
        "const MAX_DELAY  = 30000  // 30 secondes\n"
        "const JITTER     = 1000   // +/- 1 seconde aleatoire"
    ))
    story.append(p(
        "L'ajout du jitter (variation aleatoire) est crucial pour eviter le \"thundering herd\" "
        "problem: si plusieurs connexions tombent simultanement (ex: redemarrage du serveur), "
        "le jitter etale les tentatives de reconnexion dans le temps, evitant une surcharge soudaine."
    ))
    story.append(PageBreak())


def section_processor(story):
    story.append(h1("5. Service Processor - Analytique Temps Reel"))
    story.append(hr())

    story.append(p(
        "Le service Processor est le coeur analytique du pipeline. Il consomme les trades bruts "
        "depuis le topic Kafka crypto-trades, maintient des structures de donnees en memoire "
        "(buffers circulaires) par symbole, et calcule en continu trois categories d'indicateurs: "
        "indicateurs de prix, indicateurs de volume, et detection d'anomalies."
    ))

    story.append(h2("5.1 VWAP - Volume Weighted Average Price"))
    story.append(p(
        "Le VWAP est un indicateur fondamental en trading haute frequence. Il represente le prix "
        "moyen pondere par le volume, offrant une mesure plus representative que la simple moyenne "
        "arithmetique des prix."
    ))
    story.append(code_block(
        "// Formule VWAP sur les N derniers trades\n"
        "VWAP = SUM(price_i * qty_i, i=1..N) / SUM(qty_i, i=1..N)\n"
        "\n"
        "// Implementation avec buffer circulaire (N = 100)\n"
        "let sumPV = 0  // somme price * volume\n"
        "let sumV  = 0  // somme volume\n"
        "buffer.getAll().forEach(t => {\n"
        "  sumPV += t.price * t.qty\n"
        "  sumV  += t.qty\n"
        "})\n"
        "const vwap = sumV > 0 ? sumPV / sumV : 0"
    ))
    story.append(p(
        "La fenetre glissante de 100 trades offre un bon compromis entre reactivite et stabilite. "
        "Le recalcul a chaque nouveau trade est O(N) avec le buffer circulaire, ce qui reste "
        "acceptable pour N=100 et les frequences de trades observees."
    ))

    story.append(h2("5.2 SMA-20 - Moyenne Mobile Simple"))
    story.append(p(
        "La moyenne mobile simple sur 20 periodes lisse les fluctuations de court terme "
        "et permet de visualiser la tendance directionnelle du prix."
    ))
    story.append(code_block(
        "// Formule SMA sur N periodes\n"
        "SMA_N = (1/N) * SUM(price_i, i=t-N+1 .. t)\n"
        "\n"
        "// Implementation\n"
        "const prices = buffer.getAll().slice(-20).map(t => t.price)\n"
        "const sma20  = prices.reduce((a, b) => a + b, 0) / prices.length"
    ))

    story.append(h2("5.3 Detection d'anomalies - Z-Score"))
    story.append(p(
        "Le z-score (score standardise) mesure l'ecart d'une valeur par rapport a la moyenne "
        "en unites d'ecart-type. Un z-score eleve en valeur absolue indique un mouvement "
        "statistiquement anormal du prix."
    ))
    story.append(code_block(
        "// Formule Z-Score\n"
        "z = (x - mean) / std\n"
        "\n"
        "// Avec:\n"
        "//   x    = prix actuel\n"
        "//   mean = moyenne des 50 derniers prix\n"
        "//   std  = ecart-type des 50 derniers prix\n"
        "\n"
        "// Seuil d'anomalie: |z| > 2.5\n"
        "const isAnomaly = Math.abs(zScore) > ANOMALY_THRESHOLD  // 2.5\n"
        "\n"
        "// Calcul de std\n"
        "const mean = prices.reduce((a, b) => a + b) / prices.length\n"
        "const variance = prices.reduce((s, p) => s + (p - mean)**2, 0) / prices.length\n"
        "const std = Math.sqrt(variance)"
    ))
    story.append(p(
        "Un seuil de 2.5 sigma signifie qu'environ 1.24% des variations de prix "
        "seront flaggees comme anomalies dans une distribution normale. Ce niveau est "
        "suffisamment sensible pour detecter les mouvements significatifs sans generer "
        "trop de faux positifs sur les marches crypto inheremment volatils."
    ))
    story.append(PageBreak())


def section_api(story):
    story.append(h1("6. Service API"))
    story.append(hr())

    story.append(p(
        "Le service API est le point d'entree du frontend. Il encapsule la logique "
        "de consommation Kafka, maintient les ring buffers en memoire et gere les "
        "connexions Socket.IO entrantes des clients dashboard."
    ))

    story.append(h2("6.1 Endpoints REST"))
    endpoints_data = [
        ['Methode', 'Route', 'Description', 'Response'],
        ['GET', '/api/health', 'Healthcheck', '{ status: "ok", ts }'],
        ['GET', '/api/symbols', 'Liste des symboles actifs', '{ symbols: string[] }'],
        ['GET', '/api/metrics/:symbol', 'Dernieres metriques', 'Metrics object'],
        ['GET', '/api/history/:symbol', 'Historique ring buffer', 'Metrics[]  (500 max)'],
        ['GET', '/api/anomalies', 'Alertes recentes', 'Anomaly[]'],
    ]
    story.append(make_table(endpoints_data,
                            [2*cm, 4.5*cm, 5*cm, 6*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 4 - Endpoints REST de l'API", S['caption']))

    story.append(h2("6.2 Evenements Socket.IO"))
    events_data = [
        ['Evenement', 'Direction', 'Payload', 'Description'],
        ['subscribe', 'Client -> Serveur', '{ symbol: string }', 'Abonnement a un symbole'],
        ['unsubscribe', 'Client -> Serveur', '{ symbol: string }', 'Desabonnement'],
        ['metrics', 'Serveur -> Client', 'Metrics object', 'Mise a jour temps reel'],
        ['anomaly', 'Serveur -> Client', 'Anomaly object', 'Alerte anomalie detectee'],
        ['error', 'Serveur -> Client', '{ message: string }', 'Erreur de traitement'],
    ]
    story.append(make_table(events_data,
                            [2.5*cm, 3.5*cm, 4.5*cm, 7*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 5 - Evenements Socket.IO", S['caption']))

    story.append(h2("6.3 Ring Buffer en memoire"))
    story.append(p(
        "Pour servir l'historique des metriques sans persistance base de donnees, chaque "
        "symbole dispose d'un buffer circulaire de 500 entrees maintenu en memoire vive. "
        "Cette approche offre des lectures O(1) et une empreinte memoire constante."
    ))
    story.append(code_block(
        "// Ring buffer par symbole\n"
        "const ringBuffers = new Map<string, CircularBuffer<Metrics>>()\n"
        "\n"
        "// A chaque message Kafka\n"
        "consumer.on('metrics', (metrics: Metrics) => {\n"
        "  if (!ringBuffers.has(metrics.symbol)) {\n"
        "    ringBuffers.set(metrics.symbol, new CircularBuffer(500))\n"
        "  }\n"
        "  ringBuffers.get(metrics.symbol)!.push(metrics)\n"
        "  io.to(metrics.symbol).emit('metrics', metrics)\n"
        "})"
    ))
    story.append(PageBreak())


def section_dashboard(story):
    story.append(h1("7. Dashboard"))
    story.append(hr())

    story.append(h2("7.1 Stack frontend"))
    story.append(p(
        "Le dashboard est volontairement developpe en HTML/CSS/JS vanilla sans framework, "
        "conformement aux contraintes du module. Cette approche minimise la complexite du build "
        "et offre un temps de chargement optimal. La communication temps reel est assuree par "
        "Socket.IO Client, et les graphiques par Chart.js."
    ))
    stack_data = [
        ['Technologie', 'Version', 'Usage'],
        ['HTML5/CSS3', 'N/A', 'Structure et styles, CSS Grid/Flex, CSS Variables dark theme'],
        ['JavaScript ES2022', 'vanilla', 'Logique applicative, gestion evenements Socket.IO'],
        ['Chart.js', '4.x', 'Graphiques prix (line) et volume (bar), mise a jour live'],
        ['Socket.IO Client', '4.x', 'Reception push des metriques depuis l\'API'],
        ['Web Audio API', 'native', 'Beep sonore sur detection anomalie (AudioContext)'],
        ['nginx', 'alpine', 'Serveur statique Docker pour les fichiers HTML/CSS/JS'],
    ]
    story.append(make_table(stack_data,
                            [4*cm, 2*cm, 11.5*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 6 - Stack frontend dashboard", S['caption']))

    story.append(h2("7.2 Graphiques Chart.js"))
    story.append(p(
        "Le dashboard affiche deux types de graphiques mis a jour en temps reel:"
    ))
    for item in [
        "Graphique de prix (type line): courbe des 100 derniers prix, mise a jour par ajout/suppression du premier point sans re-rendu complet (chart.data.labels.shift() + push())",
        "Graphique de volume (type bar): volume des 20 derniers trades, couleur verte/rouge selon variation",
        "Indicateurs VWAP et SMA-20 superposes sur le graphique de prix comme lignes de reference",
    ]:
        story.append(bullet(item))

    story.append(h2("7.3 Alertes anomalies"))
    story.append(p(
        "Lorsque le Processor detecte un z-score superieur a 2.5, l'evenement anomaly est "
        "emis via Socket.IO. Le dashboard reagit en:"
    ))
    for item in [
        "Ajoutant une entree rouge dans le flux d'alertes avec horodatage, symbole et z-score",
        "Jouant un beep sonore via AudioContext (frequence 880 Hz, duree 200 ms)",
        "Affichant un badge rouge clignotant sur le symbole concerne",
    ]:
        story.append(bullet(item))
    story.append(PageBreak())


def section_securite(story):
    story.append(h1("8. Securite"))
    story.append(hr())

    story.append(p(
        "La securite est integree a tous les niveaux du pipeline. Le service API, en tant "
        "que point d'entree public, concentre la majorite des mesures de protection."
    ))

    security_data = [
        ['Categorie', 'Mesure', 'Implementation'],
        ['HTTP Headers', 'helmet', 'CSP, HSTS, X-Frame-Options, X-Content-Type-Options'],
        ['Rate Limiting', 'express-rate-limit', '100 requetes/min par IP, WindowMs: 60s'],
        ['CORS', 'Configuration stricte', 'Origines whitelist, methodes autorisees explicites'],
        ['Validation', 'Zod schemas', 'Validation des variables d\'env au demarrage (fast-fail)'],
        ['Secrets', '.env + gitignore', 'Aucun secret en dur dans le code source'],
        ['Docker', 'USER non-root', 'Containers executes avec user node:node (UID 1000)'],
        ['Images', 'Alpine/slim', 'Surface d\'attaque minimale, pas d\'outils inutiles'],
        ['Erreurs', 'Masquage', 'Stack traces jamais exposees au client HTTP'],
        ['Socket.IO', 'Namespace validation', 'Validation des symboles a la souscription'],
    ]
    story.append(make_table(security_data,
                            [3*cm, 4*cm, 10.5*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 7 - Mesures de securite implementees", S['caption']))

    story.append(h2("Validation Zod des variables d'environnement"))
    story.append(code_block(
        "import { z } from 'zod'\n"
        "\n"
        "const envSchema = z.object({\n"
        "  KAFKA_BROKERS:  z.string().min(1),\n"
        "  PORT:           z.coerce.number().default(3000),\n"
        "  CORS_ORIGINS:   z.string().default('http://localhost:8000'),\n"
        "  NODE_ENV:       z.enum(['development', 'production']).default('development'),\n"
        "})\n"
        "\n"
        "// Echec immediat si variable manquante ou invalide\n"
        "export const env = envSchema.parse(process.env)"
    ))
    story.append(PageBreak())


def section_i18n(story):
    story.append(h1("9. Multilinguisme - Module i18n"))
    story.append(hr())

    story.append(p(
        "Le dashboard integre un module d'internationalisation (i18n) en JavaScript vanilla "
        "qui permet de basculer entre le francais et l'anglais sans rechargement de page. "
        "La langue choisie est persistee dans localStorage."
    ))

    story.append(h2("Architecture du module"))
    story.append(code_block(
        "// dashboard/js/i18n.js\n"
        "const translations = {\n"
        "  fr: {\n"
        "    title: 'Surveillance Crypto',\n"
        "    price: 'Prix actuel',\n"
        "    anomaly: 'Anomalie detectee',\n"
        "    // ... 30+ cles\n"
        "  },\n"
        "  en: {\n"
        "    title: 'Crypto Monitor',\n"
        "    price: 'Current price',\n"
        "    anomaly: 'Anomaly detected',\n"
        "    // ...\n"
        "  }\n"
        "}\n"
        "\n"
        "function setLanguage(lang) {\n"
        "  document.querySelectorAll('[data-i18n]').forEach(el => {\n"
        "    const key = el.dataset.i18n\n"
        "    el.textContent = translations[lang]?.[key] ?? translations.fr[key]\n"
        "  })\n"
        "  localStorage.setItem('lang', lang)\n"
        "}"
    ))

    story.append(h2("Utilisation dans le HTML"))
    story.append(code_block(
        "<!-- Attribut data-i18n sur les elements a traduire -->\n"
        "<h2 data-i18n=\"price\">Prix actuel</h2>\n"
        "<span data-i18n=\"anomaly\">Anomalie detectee</span>\n"
        "<button onclick=\"setLanguage('en')\" data-i18n=\"lang_toggle\">EN</button>"
    ))

    i18n_data = [
        ['Cle', 'Francais', 'Anglais'],
        ['title', 'Surveillance Crypto', 'Crypto Monitor'],
        ['price', 'Prix actuel', 'Current price'],
        ['volume', 'Volume', 'Volume'],
        ['anomaly', 'Anomalie detectee', 'Anomaly detected'],
        ['vwap', 'VWAP', 'VWAP'],
        ['sma', 'Moyenne mobile 20', 'Moving average 20'],
        ['change1m', 'Variation 1 min', '1 min change'],
        ['change5m', 'Variation 5 min', '5 min change'],
        ['connected', 'Connecte', 'Connected'],
        ['disconnected', 'Deconnecte', 'Disconnected'],
    ]
    story.append(make_table(i18n_data, [4*cm, 6*cm, 7.5*cm], header_bg=NAVY))
    story.append(Paragraph("Tableau 8 - Extrait des cles de traduction", S['caption']))
    story.append(PageBreak())


def section_docker(story):
    story.append(h1("10. Deploiement Docker Compose"))
    story.append(hr())

    story.append(p(
        "Le projet est entierement conteneurise via Docker Compose. Six services cooperent "
        "via un reseau bridge interne, avec des healthchecks pour garantir l'ordre de demarrage "
        "et la disponibilite de chaque composant."
    ))

    story.append(h2("Services Docker Compose"))
    services_data = [
        ['Service', 'Image', 'Port expose', 'Dependances', 'Role'],
        ['kafka', 'confluentinc/cp-kafka:7.6', '9092', 'aucune', 'Broker Kafka KRaft'],
        ['kafka-ui', 'provectus/kafka-ui', '8080', 'kafka', 'Interface monitoring'],
        ['ingester', 'node:20-alpine', 'aucun', 'kafka', 'Collecte WebSocket'],
        ['processor', 'node:20-alpine', 'aucun', 'kafka', 'Calcul analytique'],
        ['api', 'node:20-alpine', '3000', 'kafka', 'API REST + Socket.IO'],
        ['dashboard', 'nginx:alpine', '8000', 'api', 'Serveur statique'],
    ]
    story.append(make_table(services_data,
                            [2.2*cm, 4.5*cm, 2.5*cm, 2.5*cm, 5.8*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 9 - Services Docker Compose", S['caption']))

    story.append(h2("Variables d'environnement"))
    env_data = [
        ['Variable', 'Service', 'Valeur par defaut', 'Description'],
        ['KAFKA_BROKERS', 'ingester, processor, api', 'kafka:9092', 'Adresse du broker Kafka'],
        ['BINANCE_WS_URL', 'ingester', 'wss://stream.binance.com:9443/ws', 'URL WebSocket Binance'],
        ['COINBASE_WS_URL', 'ingester', 'wss://advanced-trade-ws.coinbase.com', 'URL WebSocket Coinbase'],
        ['PORT', 'api', '3000', 'Port d\'ecoute de l\'API'],
        ['CORS_ORIGINS', 'api', 'http://localhost:8000', 'Origines CORS autorisees'],
        ['NODE_ENV', 'tous', 'development', 'Environnement d\'execution'],
    ]
    story.append(make_table(env_data,
                            [3.5*cm, 4*cm, 4.5*cm, 5.5*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 10 - Variables d'environnement", S['caption']))

    story.append(h2("Commandes de gestion"))
    story.append(code_block(
        "# Demarrage de l'ensemble du stack\n"
        "docker compose up -d\n"
        "\n"
        "# Suivi des logs en temps reel\n"
        "docker compose logs -f\n"
        "\n"
        "# Logs d'un service specifique\n"
        "docker compose logs -f ingester\n"
        "\n"
        "# Arret et suppression des volumes\n"
        "docker compose down -v\n"
        "\n"
        "# Acces aux interfaces\n"
        "# Dashboard:  http://localhost:8000\n"
        "# API REST:   http://localhost:3000/api/health\n"
        "# Kafka UI:   http://localhost:8080"
    ))
    story.append(PageBreak())


def section_tests(story):
    story.append(h1("11. Tests et validation"))
    story.append(hr())

    story.append(p(
        "La strategie de tests du projet combine des validations manuelles des flux end-to-end "
        "et des verifications unitaires des formules analytiques. La nature temps reel du systeme "
        "rend les tests d'integration automatises plus complexes mais non impossibles a mettre "
        "en place pour une version future."
    ))

    story.append(h2("Scenarios de test manuels"))
    test_data = [
        ['Scenario', 'Etapes', 'Resultat attendu'],
        ['Demarrage complet',
         'docker compose up -d, attendre 30s, ouvrir localhost:8000',
         'Dashboard affiche prix BTC/USDT, ETH/USDT en temps reel'],
        ['Detection anomalie',
         'Monitorer le flux pendant un mouvement de marche violent',
         'Alerte rouge + son dans le dashboard, event anomaly Socket.IO'],
        ['Reconnexion WebSocket',
         'Couper reseau 10s, retablir',
         'Ingester se reconnecte automatiquement, flux reprend'],
        ['Kafka UI',
         'Ouvrir localhost:8080, inspecter topics',
         'crypto-trades et crypto-metrics visibles avec messages actifs'],
        ['Changement de langue',
         'Cliquer bouton EN sur le dashboard',
         'Labels UI basculent en anglais sans rechargement'],
        ['Rate limiting API',
         'Envoyer > 100 req/min vers /api/health',
         'HTTP 429 Too Many Requests retourne'],
        ['Health endpoints',
         'GET /api/health, GET /api/symbols',
         'Reponses JSON valides avec donnees actuelles'],
    ]
    story.append(make_table(test_data,
                            [3.5*cm, 5.5*cm, 8.5*cm],
                            header_bg=NAVY))
    story.append(Paragraph("Tableau 11 - Scenarios de tests manuels", S['caption']))

    story.append(h2("Validation des formules analytiques"))
    story.append(p(
        "Les formules VWAP, SMA-20 et Z-Score ont ete validees manuellement sur des series "
        "de prix connues:"
    ))
    for item in [
        "VWAP: verifie sur une serie de 5 trades avec volumes variables, resultat compare a calcul Excel",
        "SMA-20: verifie contre les valeurs publiees par TradingView sur BTC/USDT",
        "Z-Score: verifie sur une distribution normale artificielle (seuil 2.5 = 1.24% outliers attendus)",
    ]:
        story.append(bullet(item))
    story.append(PageBreak())


def section_bilan(story):
    story.append(h1("12. Bilan et perspectives"))
    story.append(hr())

    story.append(h2("Ce qui a ete realise"))
    done = [
        "Pipeline temps reel complet et fonctionnel: WebSocket -> Kafka -> Analytics -> Dashboard",
        "Kafka KRaft sans Zookeeper: simplification du deploiement Docker",
        "3 feeds WebSocket: Binance (BTC/USDT, ETH/USDT) et Coinbase (BTC-USD)",
        "3 indicateurs analytiques: VWAP, SMA-20, Z-Score avec detection d'anomalies",
        "Dashboard live avec Chart.js, alertes visuelles et sonores",
        "Module i18n FR/EN en JavaScript vanilla, persistance localStorage",
        "Securite: helmet, rate-limit, Zod validation, CORS, containers non-root",
        "Deploiement Docker Compose 6 services avec healthchecks et volumes nommes",
        "Projet realise par 2 personnes (prevu pour 4) avec qualite professionnelle",
    ]
    for item in done:
        story.append(bullet(item))

    story.append(sp(0.3))
    story.append(h2("Perspectives d'evolution"))
    future = [
        "Persistance long terme: TimescaleDB ou InfluxDB pour historique sur plusieurs jours",
        "Alertes push: notifications Telegram ou email sur detection d'anomalie critique",
        "Machine Learning: prediction de tendance avec modele LSTM ou Prophet",
        "Exchanges supplementaires: Kraken, OKX pour diversifier les sources de prix",
        "Authentification: JWT + gestion de portefeuilles personnalises",
        "Backtest: capacite de replay des donnees historiques sur le pipeline analytique",
        "CI/CD: GitHub Actions avec tests automatises E2E (Playwright) et lint TypeScript",
        "Observabilite: Prometheus + Grafana pour metriques infra (latence, throughput, consumer lag)",
        "Clustering Kafka: passage a 3 brokers pour haute disponibilite",
    ]
    for item in future:
        story.append(bullet(item))

    story.append(sp(0.3))
    story.append(h2("Retour d'experience"))
    story.append(p(
        "Ce projet a permis d'acquérir une experience pratique significative sur plusieurs "
        "technologies de l'ecosysteme Real-Time Engineering:"
    ))
    skills_data = [
        ['Domaine', 'Competences acquises'],
        ['Apache Kafka', 'Configuration KRaft, topics, partitionnement, consumer groups, kafkajs'],
        ['WebSocket', 'Gestion de connexions persistantes, protocoles Binance/Coinbase, backoff'],
        ['Analytique temps reel', 'VWAP, SMA, Z-score, buffers circulaires, algorithmes O(1)'],
        ['TypeScript', 'Typage strict, interfaces, generics, enums, schema Zod'],
        ['Socket.IO', 'Rooms/namespaces, push server-side, reconnexion client'],
        ['Docker', 'Compose multi-service, healthchecks, volumes, reseau bridge, non-root'],
        ['Securite API', 'Helmet, rate-limiting, CORS, validation env, secrets management'],
    ]
    story.append(make_table(skills_data, [4*cm, 13.5*cm], header_bg=NAVY))
    story.append(Paragraph("Tableau 12 - Competences acquises", S['caption']))
    story.append(PageBreak())


def section_conclusion(story):
    story.append(h1("13. Conclusion"))
    story.append(hr())

    story.append(p(
        "Le projet Crypto Market Monitor constitue une demonstration concrete et fonctionnelle "
        "des concepts fondamentaux du Real-Time Engineering appliques au domaine financier. "
        "Le pipeline complet - de la collecte WebSocket a la visualisation sur dashboard - "
        "illustre comment Apache Kafka peut servir de backbone scalable pour des architectures "
        "evenementielles en temps reel."
    ))
    story.append(p(
        "La realisation de ce projet par une equipe de deux personnes, pour un cahier des charges "
        "prevu pour quatre, demontre la capacite a prioriser les fonctionnalites essentielles, "
        "a faire des choix architecturaux pragmatiques et a maintenir une qualite de code "
        "professionnelle sous contrainte de ressources."
    ))
    story.append(p(
        "Sur le plan technique, les principaux apports sont: la maitrise de Kafka KRaft "
        "comme bus de messages decoupled, l'implementation d'indicateurs financiers temps reel "
        "(VWAP, SMA, Z-score) avec des structures de donnees adaptees (buffers circulaires), "
        "et l'integration d'un stack full TypeScript Node.js containerise avec Docker Compose."
    ))
    story.append(p(
        "Les perspectives d'evolution sont nombreuses: persistance long terme avec TimescaleDB, "
        "alertes push multi-canal, modeles de prediction ML, et passage a une architecture "
        "Kafka multi-broker pour la haute disponibilite. Ces evolutions permettraient de "
        "transformer ce proof of concept en plateforme de surveillance professionnelle."
    ))
    story.append(sp(0.5))
    story.append(HRFlowable(width='40%', thickness=1, color=AMBER,
                             spaceAfter=16, spaceBefore=8))
    story.append(Paragraph(
        "Adam Beloucif  -  Emilien Morice<br/>"
        "M1 Data Engineering & IA - EFREI Paris<br/>"
        "Module Real-Time Engineering - 2025-2026",
        ParagraphStyle('FinalAuthor', fontSize=10, textColor=MUTED,
                       alignment=TA_CENTER, fontName='Helvetica',
                       leading=16)
    ))


# ── Cover page canvas ─────────────────────────────────────────────────────

class CoverPageCanvas(pdfcanvas.Canvas):
    """Canvas that draws a dark cover on page 1."""

    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self._page_number = 0

    def showPage(self):
        self._page_number += 1
        if self._page_number == 1:
            self._draw_cover_bg()
        else:
            self._draw_content_header()
        super().showPage()

    def save(self):
        self._page_number += 1
        if self._page_number == 1:
            self._draw_cover_bg()
        else:
            self._draw_content_header()
        super().save()

    def _draw_cover_bg(self):
        w, h = A4
        self.setFillColor(NAVY)
        self.rect(0, 0, w, h, fill=1, stroke=0)
        # Top amber bar
        self.setFillColor(AMBER)
        self.rect(0, h - 0.3 * cm, w, 0.3 * cm, fill=1, stroke=0)
        # Bottom amber bar
        self.rect(0, 0, w, 0.3 * cm, fill=1, stroke=0)
        # Left purple accent
        self.setFillColor(PURPLE)
        self.rect(0, 0.3 * cm, 0.3 * cm, h - 0.6 * cm, fill=1, stroke=0)

    def _draw_content_header(self):
        pn = self._page_number
        w, h = A4
        self.setFillColor(NAVY)
        self.rect(0, h - 1.2 * cm, w, 1.2 * cm, fill=1, stroke=0)
        self.setFillColor(AMBER)
        self.rect(0, h - 0.15 * cm, w, 0.15 * cm, fill=1, stroke=0)
        self.setFillColor(colors.HexColor('#94A3B8'))
        self.setFont('Helvetica', 8)
        self.drawString(2 * cm, h - 0.85 * cm, 'Crypto Market Monitor - Rapport Technique')
        self.setFillColor(AMBER)
        self.drawRightString(w - 2 * cm, h - 0.85 * cm,
                             'M1 Data Engineering & IA - EFREI Paris 2025-2026')
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.3)
        self.line(2 * cm, 1.5 * cm, w - 2 * cm, 1.5 * cm)
        self.setFillColor(MUTED)
        self.setFont('Helvetica', 8)
        self.drawString(2 * cm, 0.9 * cm, 'Adam Beloucif, Emilien Morice')
        self.drawCentredString(w / 2, 0.9 * cm, 'Confidentiel - Usage pedagogique uniquement')
        self.drawRightString(w - 2 * cm, 0.9 * cm, f'Page {pn - 1}')


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, 'crypto-market-monitor-rapport-technique.pdf')

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title='Crypto Market Monitor - Rapport Technique',
        author='Adam Beloucif, Emilien Morice',
        subject='Real-Time Engineering - M1 EFREI Paris 2025-2026',
    )

    story = []

    cover_page(story)
    toc_page(story)
    section_introduction(story)
    section_architecture(story)
    section_kafka(story)
    section_ingester(story)
    section_processor(story)
    section_api(story)
    section_dashboard(story)
    section_securite(story)
    section_i18n(story)
    section_docker(story)
    section_tests(story)
    section_bilan(story)
    section_conclusion(story)

    doc.build(story, canvasmaker=CoverPageCanvas)

    size = os.path.getsize(out_path)
    print(f"PDF saved: {out_path}")
    print(f"File size: {size:,} bytes ({size / 1024:.1f} KB)")


if __name__ == '__main__':
    main()
