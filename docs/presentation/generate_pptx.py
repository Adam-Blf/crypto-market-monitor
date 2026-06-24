"""
Crypto Market Monitor - PPTX Presentation Generator
Authors: Adam Beloucif, Emilien Morice
M1 Data Engineering & IA, EFREI Paris
Module: Real-Time Engineering 2025-2026
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree


# ── Color palette ──────────────────────────────────────────────────────────
C_NAVY   = RGBColor(0x0F, 0x17, 0x2A)
C_AMBER  = RGBColor(0xF5, 0x9E, 0x0B)
C_PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
C_WHITE  = RGBColor(0xF8, 0xFA, 0xFC)
C_MUTED  = RGBColor(0x94, 0xA3, 0xB8)
C_GREEN  = RGBColor(0x10, 0xB9, 0x81)
C_RED    = RGBColor(0xEF, 0x44, 0x44)
C_CARD   = RGBColor(0x1E, 0x29, 0x3B)
C_DARK   = RGBColor(0x0D, 0x14, 0x22)

TOTAL_SLIDES = 12


# ── Helpers ─────────────────────────────────────────────────────────────────

def set_slide_bg(slide, rgb: RGBColor):
    """Set solid background color on a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = rgb


def add_textbox(slide, text, left, top, width, height,
                font_size=18, bold=False, color=None,
                align=PP_ALIGN.LEFT, italic=False, font_name="Calibri"):
    if color is None:
        color = C_WHITE
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox


def add_multiline_textbox(slide, lines, left, top, width, height,
                          font_size=14, color=None, line_spacing_pt=6,
                          font_name="Calibri"):
    """Add a textbox with multiple paragraphs."""
    if color is None:
        color = C_WHITE
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.name = font_name
    return txBox


def add_slide_title(slide, title):
    add_textbox(slide, title, 0.5, 0.15, 12.3, 0.9,
                font_size=28, bold=True, color=C_AMBER, align=PP_ALIGN.LEFT)


def add_footer(slide, slide_num):
    line_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(7.15), Inches(12.33), Inches(0.1)
    )
    fill = line_box.fill
    fill.solid()
    fill.fore_color.rgb = C_AMBER

    add_textbox(slide,
                f"M1 EFREI - Real-Time Engineering 2025-2026  |  Adam Beloucif, Emilien Morice  |  {slide_num}/{TOTAL_SLIDES}",
                0.5, 7.25, 12.33, 0.22, font_size=8, color=C_MUTED, align=PP_ALIGN.CENTER)


def add_card(slide, left, top, width, height, bg: RGBColor = None):
    """Add a rounded-corner card rectangle."""
    if bg is None:
        bg = C_CARD
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.color.rgb = RGBColor(0x2D, 0x3D, 0x55)
    shape.line.width = Pt(0.75)
    return shape


def add_highlight_bar(slide, left, top, width, height, color: RGBColor = None):
    """Thin accent bar."""
    if color is None:
        color = C_AMBER
    shape = slide.shapes.add_shape(
        1,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


# ── Slide factories ──────────────────────────────────────────────────────────

def slide_01_title(prs):
    """Slide 1: Title."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_slide_bg(slide, C_DARK)

    # Amber gradient bar top
    add_highlight_bar(slide, 0, 0, 13.33, 0.08, C_AMBER)

    # Purple accent left bar
    add_highlight_bar(slide, 0, 0.08, 0.08, 7.42, C_PURPLE)

    # Main title
    add_textbox(slide, "Crypto Market Monitor",
                0.5, 1.0, 12.33, 1.5,
                font_size=40, bold=True, color=C_AMBER, align=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide, "Systeme de surveillance de marches crypto en temps reel",
                0.5, 2.5, 12.33, 0.8,
                font_size=20, bold=False, color=C_WHITE, align=PP_ALIGN.CENTER, italic=True)

    # Separator line
    add_highlight_bar(slide, 3.5, 3.45, 6.33, 0.04, C_PURPLE)

    # Authors
    add_textbox(slide, "Adam Beloucif  -  Emilien Morice",
                0.5, 3.65, 12.33, 0.55,
                font_size=16, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    # Info block
    add_textbox(slide, "M1 Data Engineering & IA  -  EFREI Paris",
                0.5, 4.3, 12.33, 0.45,
                font_size=14, color=C_MUTED, align=PP_ALIGN.CENTER)

    add_textbox(slide, "Module: Real-Time Engineering  -  Annee 2025-2026",
                0.5, 4.75, 12.33, 0.45,
                font_size=14, color=C_MUTED, align=PP_ALIGN.CENTER)

    # Tech tags row
    tags = ["Kafka KRaft", "TypeScript", "Node.js", "WebSocket", "Docker"]
    tag_w = 1.8
    tag_x_start = (13.33 - len(tags) * tag_w - (len(tags) - 1) * 0.15) / 2
    for i, tag in enumerate(tags):
        x = tag_x_start + i * (tag_w + 0.15)
        add_card(slide, x, 5.7, tag_w, 0.5, bg=RGBColor(0x1E, 0x29, 0x3B))
        add_textbox(slide, tag, x, 5.7, tag_w, 0.5,
                    font_size=11, bold=True, color=C_AMBER, align=PP_ALIGN.CENTER)

    # Bottom bar
    add_highlight_bar(slide, 0.08, 7.42, 13.25, 0.08, C_AMBER)


def slide_02_contexte(prs):
    """Slide 2: Contexte et problematique."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Contexte et Problematique")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    context_points = [
        ("Marches crypto volatils", "Les cryptomonnaies connaissent des variations de prix extremes en quelques secondes. Un pipeline temps reel est indispensable pour capturer ces mouvements."),
        ("Donnees en temps reel", "Binance et Coinbase exposent des flux WebSocket publics avec des trades a haute frequence. Chaque message contient prix, volume, horodatage."),
        ("Besoin de surveillance", "Les traders et analystes ont besoin d'indicateurs calcules en continu: VWAP, moyennes mobiles, alertes d'anomalies statistiques."),
        ("Detection d'anomalies", "Le z-score permet d'identifier les mouvements de prix hors norme (seuil 2.5 sigma), declenchant des alertes visuelles et sonores."),
    ]

    for i, (title, body) in enumerate(context_points):
        y = 1.3 + i * 1.3
        add_card(slide, 0.5, y, 12.33, 1.1)
        add_highlight_bar(slide, 0.5, y, 0.06, 1.1, C_AMBER)
        add_textbox(slide, title, 0.75, y + 0.05, 11.5, 0.38,
                    font_size=13, bold=True, color=C_AMBER)
        add_textbox(slide, body, 0.75, y + 0.42, 11.5, 0.62,
                    font_size=11, color=C_WHITE)

    add_footer(slide, 2)


def slide_03_architecture(prs):
    """Slide 3: Architecture globale."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Architecture Globale")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # Architecture pipeline boxes
    components = [
        ("WebSocket\nBinance/Coinbase", C_GREEN, 0.35),
        ("Ingester\nTypeScript", C_AMBER, 2.15),
        ("Kafka\nKRaft", C_PURPLE, 3.95),
        ("Processor\nTypeScript", C_AMBER, 5.75),
        ("API\nExpress+Socket.IO", C_GREEN, 7.55),
        ("Dashboard\nHTML/CSS/JS", C_RED, 9.35),
    ]

    box_w = 1.55
    box_h = 1.15
    y_box = 1.5

    for label, color, x in components:
        add_card(slide, x, y_box, box_w, box_h, bg=RGBColor(0x1E, 0x29, 0x3B))
        add_highlight_bar(slide, x, y_box, box_w, 0.05, color)
        add_textbox(slide, label, x, y_box + 0.15, box_w, box_h - 0.15,
                    font_size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    # Arrows between boxes
    arrows = [1.9, 3.7, 5.5, 7.3, 9.1]
    for ax in arrows:
        add_textbox(slide, "->", ax, y_box + 0.4, 0.25, 0.35,
                    font_size=16, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)

    # Details row
    details = [
        ("Port 9092\ntrades + metrics", 0.35),
        ("Reconnexion\nautomatique", 2.15),
        ("KRaft - no\nZookeeper", 3.95),
        ("VWAP / SMA\nZ-score", 5.75),
        ("REST + WS\npush live", 7.55),
        ("Chart.js\nDark theme", 9.35),
    ]
    for label, x in details:
        add_textbox(slide, label, x, 2.85, box_w, 0.6,
                    font_size=9, color=C_MUTED, align=PP_ALIGN.CENTER)

    # Data flow description
    add_card(slide, 0.5, 3.65, 12.33, 2.6)
    add_textbox(slide, "Flux de donnees", 0.75, 3.75, 6.0, 0.35,
                font_size=13, bold=True, color=C_AMBER)
    flow_lines = [
        "1. Les exchanges Binance (BTC/USDT, ETH/USDT) et Coinbase (BTC-USD) publient des trades via WebSocket.",
        "2. Le service Ingester consomme ces flux, normalise les messages dans une interface Trade unifiee,",
        "   puis produit vers Kafka (topic: crypto-trades, partitionne par symbole).",
        "3. Le Processor consomme crypto-trades, calcule VWAP, SMA-20, z-score et publie dans crypto-metrics.",
        "4. L'API Express consomme crypto-metrics, stocke en ring buffer et pousse via Socket.IO vers les clients.",
        "5. Le Dashboard (navigateur) recoit les updates en temps reel et met a jour les graphiques Chart.js.",
    ]
    for i, line in enumerate(flow_lines):
        add_textbox(slide, line, 0.75, 4.2 + i * 0.32, 11.8, 0.32,
                    font_size=9.5, color=C_WHITE if i == 0 or not line.startswith(" ") else C_MUTED)

    add_footer(slide, 3)


def slide_04_kafka(prs):
    """Slide 4: Apache Kafka KRaft."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_PURPLE)
    add_slide_title(slide, "Apache Kafka - Mode KRaft")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_PURPLE)

    # Left column - KRaft mode
    add_card(slide, 0.5, 1.3, 5.8, 2.7)
    add_textbox(slide, "Mode KRaft (sans Zookeeper)", 0.7, 1.4, 5.4, 0.4,
                font_size=13, bold=True, color=C_PURPLE)
    kraft_lines = [
        "- Kafka 3.x+ integre la gestion des metadonnees",
        "  directement (Kafka Raft Metadata Mode)",
        "- Elimine la dependance a Apache Zookeeper",
        "- Simplification du deploiement Docker (1 seul service)",
        "- Latence reduite: consensus Raft integre au broker",
        "- KAFKA_NODE_ID=1, KAFKA_PROCESS_ROLES=broker,controller",
        "- KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093",
    ]
    for i, line in enumerate(kraft_lines):
        add_textbox(slide, line, 0.7, 1.85 + i * 0.28, 5.4, 0.28,
                    font_size=9.5, color=C_WHITE)

    # Right column - Topics
    add_card(slide, 6.63, 1.3, 6.2, 2.7)
    add_textbox(slide, "Topics et Partitionnement", 6.83, 1.4, 5.8, 0.4,
                font_size=13, bold=True, color=C_AMBER)
    topics_data = [
        ("crypto-trades", "3 partitions", "7 jours", "Messages trades bruts normalises"),
        ("crypto-metrics", "3 partitions", "1 jour", "Metriques calculees par symbole"),
    ]
    add_textbox(slide, "Topic                  Partitions   Retention   Description",
                6.83, 1.85, 5.8, 0.3, font_size=8.5, bold=True, color=C_MUTED)
    add_highlight_bar(slide, 6.83, 2.12, 5.8, 0.02, C_MUTED)
    for i, (t, p, r, d) in enumerate(topics_data):
        y = 2.2 + i * 0.55
        bg = RGBColor(0x0F, 0x17, 0x2A) if i % 2 == 0 else RGBColor(0x1A, 0x25, 0x38)
        add_card(slide, 6.83, y, 5.8, 0.5, bg=bg)
        add_textbox(slide, t, 6.88, y + 0.05, 1.5, 0.4, font_size=9, bold=True, color=C_AMBER)
        add_textbox(slide, p, 8.55, y + 0.05, 1.0, 0.4, font_size=9, color=C_WHITE)
        add_textbox(slide, r, 9.6, y + 0.05, 0.9, 0.4, font_size=9, color=C_GREEN)
        add_textbox(slide, d, 10.55, y + 0.05, 2.0, 0.4, font_size=8, color=C_MUTED)

    # Bottom row - Config details
    add_card(slide, 0.5, 4.2, 5.8, 2.55)
    add_textbox(slide, "Configuration Kafka (docker-compose)", 0.7, 4.3, 5.4, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    config_lines = [
        "KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://...",
        "KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092",
        "KAFKA_AUTO_CREATE_TOPICS_ENABLE: true",
        "KAFKA_LOG_RETENTION_HOURS: 168 (7 jours)",
        "KAFKA_NUM_PARTITIONS: 3 (par defaut)",
        "KAFKA_DEFAULT_REPLICATION_FACTOR: 1 (single-node dev)",
    ]
    for i, line in enumerate(config_lines):
        add_textbox(slide, line, 0.7, 4.78 + i * 0.3, 5.4, 0.3,
                    font_size=9, color=C_WHITE, font_name="Courier New")

    # Kafka UI
    add_card(slide, 6.63, 4.2, 6.2, 2.55)
    add_textbox(slide, "Kafka UI - Monitoring", 6.83, 4.3, 5.8, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    ui_lines = [
        "Interface web kafka-ui (provectus/kafka-ui)",
        "Accessible sur http://localhost:8080",
        "",
        "Fonctionnalites:",
        "- Visualisation des topics et partitions",
        "- Consultation des messages en temps reel",
        "- Monitoring des consumer groups",
        "- Inspection des offsets et lag",
    ]
    for i, line in enumerate(ui_lines):
        color = C_GREEN if line.startswith("-") else C_WHITE
        add_textbox(slide, line, 6.83, 4.75 + i * 0.27, 5.8, 0.27,
                    font_size=9, color=color)

    add_footer(slide, 4)


def slide_05_ingester(prs):
    """Slide 5: Service Ingester."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Service Ingester - Collecte WebSocket")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # Sources
    add_card(slide, 0.5, 1.3, 3.8, 5.45)
    add_textbox(slide, "Sources de donnees", 0.7, 1.4, 3.4, 0.4,
                font_size=13, bold=True, color=C_AMBER)
    sources = [
        ("Binance", "wss://stream.binance.com:9443", ["BTC/USDT", "ETH/USDT"], C_GREEN),
        ("Coinbase", "wss://advanced-trade-ws.coinbase.com", ["BTC-USD"], C_PURPLE),
    ]
    for i, (name, url, symbols, color) in enumerate(sources):
        y = 1.9 + i * 1.5
        add_card(slide, 0.7, y, 3.4, 1.3, bg=RGBColor(0x0F, 0x17, 0x2A))
        add_highlight_bar(slide, 0.7, y, 0.05, 1.3, color)
        add_textbox(slide, name, 0.9, y + 0.05, 3.0, 0.38,
                    font_size=12, bold=True, color=color)
        add_textbox(slide, url, 0.9, y + 0.4, 3.0, 0.3,
                    font_size=7.5, color=C_MUTED, font_name="Courier New")
        add_textbox(slide, "Symboles: " + ", ".join(symbols), 0.9, y + 0.72, 3.0, 0.28,
                    font_size=9, color=C_WHITE)
        add_textbox(slide, "Format: JSON stream (trades)", 0.9, y + 0.98, 3.0, 0.25,
                    font_size=8.5, color=C_MUTED)

    add_textbox(slide, "Interface Trade (TypeScript):", 0.7, 4.95, 3.4, 0.35,
                font_size=10, bold=True, color=C_AMBER)
    trade_code = (
        "interface Trade {\n"
        "  symbol: string\n"
        "  price:  number\n"
        "  qty:    number\n"
        "  ts:     number  // ms\n"
        "  exchange: string\n"
        "}"
    )
    add_textbox(slide, trade_code, 0.7, 5.3, 3.4, 1.35,
                font_size=8.5, color=C_GREEN, font_name="Courier New")

    # Middle - Reconnection strategy
    add_card(slide, 4.55, 1.3, 4.1, 2.8)
    add_textbox(slide, "Strategie de reconnexion", 4.75, 1.4, 3.7, 0.4,
                font_size=12, bold=True, color=C_PURPLE)
    reconnect_lines = [
        "Backoff exponentiel avec jitter:",
        "",
        "delay = min(base * 2^attempt, maxDelay)",
        "       + random(0, jitter)",
        "",
        "base = 1000 ms",
        "maxDelay = 30000 ms",
        "jitter = 1000 ms",
        "",
        "Avantages:",
        "- Evite le thundering herd",
        "- Reconnexion automatique sans",
        "  intervention manuelle",
        "- Logs detailles par tentative",
    ]
    for i, line in enumerate(reconnect_lines):
        color = C_WHITE
        if line.startswith("delay") or line.startswith("base") or line.startswith("max") or line.startswith("jitter"):
            color = C_GREEN
            font_name = "Courier New"
        elif line.startswith("-"):
            color = C_MUTED
            font_name = "Calibri"
        else:
            font_name = "Calibri"
        add_textbox(slide, line, 4.75, 1.88 + i * 0.25, 3.7, 0.25,
                    font_size=9, color=color, font_name=font_name)

    # Middle - Normalisation
    add_card(slide, 4.55, 4.3, 4.1, 2.45)
    add_textbox(slide, "Normalisation des messages", 4.75, 4.4, 3.7, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    norm_lines = [
        "Binance: champ 'p' = prix, 'q' = quantite",
        "Coinbase: champ 'price', 'size'",
        "",
        "Converge vers Trade unifie avant",
        "publication Kafka:",
        "- Parsing JSON + validation",
        "- Conversion string -> number",
        "- Horodatage normalise en ms",
        "- Symbol: BTC-USD -> BTC/USD",
    ]
    for i, line in enumerate(norm_lines):
        color = C_MUTED if line.startswith("-") else C_WHITE
        add_textbox(slide, line, 4.75, 4.88 + i * 0.25, 3.7, 0.25,
                    font_size=9, color=color)

    # Right - Kafka producer
    add_card(slide, 8.9, 1.3, 3.93, 5.45)
    add_textbox(slide, "Kafka Producer", 9.1, 1.4, 3.53, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    producer_lines = [
        "Library: kafkajs",
        "Topic: crypto-trades",
        "Partitioning: hash(symbol)",
        "",
        "Configuration:",
        "  clientId: ingester",
        "  brokers: [kafka:9092]",
        "  retry: { retries: 5 }",
        "",
        "Message format:",
        "{",
        "  key: symbol (Buffer),",
        "  value: JSON.stringify(",
        "    trade",
        "  ),",
        "  timestamp: Date.now()",
        "}",
        "",
        "Throughput mesure:",
        "~200-500 msg/s par symbole",
        "en conditions normales.",
    ]
    for i, line in enumerate(producer_lines):
        color = C_WHITE
        if line.strip().startswith(("clientId", "brokers", "retry", "key:", "value:", "timestamp")):
            color = C_GREEN
            font_name = "Courier New"
        elif line in ("{", "}", "  ),"):
            color = C_MUTED
            font_name = "Courier New"
        elif line.startswith("~"):
            color = C_AMBER
            font_name = "Calibri"
        else:
            font_name = "Calibri"
        add_textbox(slide, line, 9.1, 1.88 + i * 0.26, 3.53, 0.26,
                    font_size=9, color=color, font_name=font_name)

    add_footer(slide, 5)


def slide_06_processor(prs):
    """Slide 6: Service Processor - Analytique."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_GREEN)
    add_slide_title(slide, "Service Processor - Analytique Temps Reel")
    add_highlight_bar(slide, 0.5, 1.1, 5.0, 0.04, C_GREEN)

    # VWAP
    add_card(slide, 0.5, 1.3, 3.9, 2.9)
    add_textbox(slide, "VWAP - Volume Weighted Average Price", 0.7, 1.4, 3.5, 0.5,
                font_size=11, bold=True, color=C_AMBER)
    add_textbox(slide,
                "VWAP = SUM(price_i * qty_i) / SUM(qty_i)",
                0.7, 1.95, 3.5, 0.4,
                font_size=10, bold=True, color=C_GREEN, font_name="Courier New")
    vwap_lines = [
        "Calcule sur la fenetre glissante",
        "des 100 derniers trades (circular buffer).",
        "",
        "Indicateur cle pour evaluer si le",
        "prix actuel est au-dessus ou en",
        "dessous du prix moyen pondere.",
        "",
        "Reset partiel a chaque nouveau",
        "trade: O(1) avec buffer circulaire.",
    ]
    for i, line in enumerate(vwap_lines):
        add_textbox(slide, line, 0.7, 2.42 + i * 0.24, 3.5, 0.24,
                    font_size=9, color=C_WHITE)

    # SMA
    add_card(slide, 4.65, 1.3, 3.9, 2.9)
    add_textbox(slide, "SMA-20 - Moyenne Mobile Simple", 4.85, 1.4, 3.5, 0.5,
                font_size=11, bold=True, color=C_PURPLE)
    add_textbox(slide,
                "SMA = (1/N) * SUM(close_i, i=t-N+1..t)",
                4.85, 1.95, 3.5, 0.4,
                font_size=9.5, bold=True, color=C_GREEN, font_name="Courier New")
    sma_lines = [
        "N = 20 periodes (trades)",
        "Lisse les fluctuations de prix",
        "a court terme.",
        "",
        "Usage: detecter la tendance",
        "generale (bullish/bearish).",
        "",
        "Compare au prix actuel pour",
        "signaler croisements notables.",
    ]
    for i, line in enumerate(sma_lines):
        add_textbox(slide, line, 4.85, 2.42 + i * 0.24, 3.5, 0.24,
                    font_size=9, color=C_WHITE)

    # Z-score
    add_card(slide, 8.8, 1.3, 4.03, 2.9)
    add_textbox(slide, "Z-Score - Detection d'Anomalies", 9.0, 1.4, 3.63, 0.5,
                font_size=11, bold=True, color=C_RED)
    add_textbox(slide,
                "z = (x - mean) / std",
                9.0, 1.95, 3.63, 0.4,
                font_size=10, bold=True, color=C_GREEN, font_name="Courier New")
    zscore_lines = [
        "Seuil d'alerte: |z| > 2.5",
        "Fenetre: 50 derniers prix",
        "",
        "Signification:",
        "z > 2.5  -> spike haussier",
        "z < -2.5 -> spike baissier",
        "",
        "Alerte envoyee dans le topic",
        "crypto-metrics avec flag",
        "isAnomaly: true",
    ]
    for i, line in enumerate(zscore_lines):
        color = C_RED if ("spike" in line or "Alerte" in line) else C_WHITE
        add_textbox(slide, line, 9.0, 2.42 + i * 0.24, 3.63, 0.24,
                    font_size=9, color=color)

    # Bottom - Other metrics + circular buffer
    add_card(slide, 0.5, 4.38, 6.1, 2.37)
    add_textbox(slide, "Autres indicateurs calcules", 0.7, 4.48, 5.7, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    other_metrics = [
        ("priceChange1m", "Variation du prix sur 1 minute en %"),
        ("priceChange5m", "Variation du prix sur 5 minutes en %"),
        ("volume1m", "Volume cumule sur 1 minute"),
        ("tradeCount1m", "Nombre de trades sur 1 minute"),
        ("high24h / low24h", "Plus haut/bas sur les dernieres 24h"),
    ]
    for i, (name, desc) in enumerate(other_metrics):
        y = 4.96 + i * 0.34
        add_textbox(slide, name, 0.7, y, 2.0, 0.32,
                    font_size=9, bold=True, color=C_GREEN, font_name="Courier New")
        add_textbox(slide, desc, 2.75, y, 3.6, 0.32,
                    font_size=9, color=C_MUTED)

    add_card(slide, 6.85, 4.38, 5.98, 2.37)
    add_textbox(slide, "Circular Buffer - Architecture", 7.05, 4.48, 5.58, 0.4,
                font_size=12, bold=True, color=C_PURPLE)
    cb_lines = [
        "Stockage des N derniers trades en memoire:",
        "class CircularBuffer<T> {",
        "  private buffer: T[]",
        "  private head = 0",
        "  push(item: T): void  // O(1)",
        "  getAll(): T[]        // O(N)",
        "}",
        "",
        "Avantage: pas de shift() couteux (O(N)),",
        "empreinte memoire constante.",
    ]
    for i, line in enumerate(cb_lines):
        color = C_GREEN if any(c in line for c in ["class", "private", "push", "get", "}", "{"]) else C_WHITE
        font_name = "Courier New" if any(c in line for c in ["class", "private", "push", "get", "}", "{", "T>"]) else "Calibri"
        add_textbox(slide, line, 7.05, 4.96 + i * 0.25, 5.58, 0.25,
                    font_size=9, color=color, font_name=font_name)

    add_footer(slide, 6)


def slide_07_api(prs):
    """Slide 7: Service API."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Service API - Express + Socket.IO")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # REST endpoints table
    add_textbox(slide, "Endpoints REST", 0.5, 1.25, 6.0, 0.38,
                font_size=13, bold=True, color=C_AMBER)
    endpoints = [
        ("GET", "/api/health", "Healthcheck du service API"),
        ("GET", "/api/symbols", "Liste des symboles surveilles"),
        ("GET", "/api/metrics/:symbol", "Dernieres metriques pour un symbole"),
        ("GET", "/api/history/:symbol", "Historique ring buffer (500 entrees)"),
        ("GET", "/api/anomalies", "Alertes anomalies recentes (z-score)"),
    ]
    header_y = 1.7
    add_card(slide, 0.5, header_y, 7.3, 0.38, bg=RGBColor(0x1E, 0x29, 0x3B))
    add_textbox(slide, "Methode", 0.6, header_y + 0.05, 0.9, 0.28,
                font_size=9, bold=True, color=C_MUTED)
    add_textbox(slide, "Route", 1.6, header_y + 0.05, 2.5, 0.28,
                font_size=9, bold=True, color=C_MUTED)
    add_textbox(slide, "Description", 4.2, header_y + 0.05, 3.5, 0.28,
                font_size=9, bold=True, color=C_MUTED)

    for i, (method, route, desc) in enumerate(endpoints):
        y = 2.15 + i * 0.4
        bg = RGBColor(0x0F, 0x17, 0x2A) if i % 2 == 0 else RGBColor(0x17, 0x20, 0x33)
        add_card(slide, 0.5, y, 7.3, 0.38, bg=bg)
        method_color = C_GREEN if method == "GET" else C_AMBER
        add_textbox(slide, method, 0.6, y + 0.05, 0.9, 0.28,
                    font_size=9, bold=True, color=method_color)
        add_textbox(slide, route, 1.6, y + 0.05, 2.5, 0.28,
                    font_size=9, color=C_AMBER, font_name="Courier New")
        add_textbox(slide, desc, 4.2, y + 0.05, 3.5, 0.28,
                    font_size=9, color=C_WHITE)

    # Socket.IO events
    add_textbox(slide, "Evenements Socket.IO", 0.5, 4.25, 6.0, 0.38,
                font_size=13, bold=True, color=C_PURPLE)
    events = [
        ("subscribe", "Client -> Serveur", "S'abonner a un symbole"),
        ("unsubscribe", "Client -> Serveur", "Se desabonner d'un symbole"),
        ("metrics", "Serveur -> Client", "Mise a jour des metriques (push)"),
        ("anomaly", "Serveur -> Client", "Alerte anomalie detectee"),
        ("error", "Serveur -> Client", "Erreur de traitement"),
    ]
    hdr2_y = 4.7
    add_card(slide, 0.5, hdr2_y, 7.3, 0.38, bg=RGBColor(0x1E, 0x29, 0x3B))
    add_textbox(slide, "Evenement", 0.6, hdr2_y + 0.05, 1.7, 0.28,
                font_size=9, bold=True, color=C_MUTED)
    add_textbox(slide, "Direction", 2.4, hdr2_y + 0.05, 1.7, 0.28,
                font_size=9, bold=True, color=C_MUTED)
    add_textbox(slide, "Description", 4.2, hdr2_y + 0.05, 3.5, 0.28,
                font_size=9, bold=True, color=C_MUTED)

    for i, (event, direction, desc) in enumerate(events):
        y = 5.15 + i * 0.38
        bg = RGBColor(0x0F, 0x17, 0x2A) if i % 2 == 0 else RGBColor(0x17, 0x20, 0x33)
        add_card(slide, 0.5, y, 7.3, 0.36, bg=bg)
        add_textbox(slide, event, 0.6, y + 0.05, 1.7, 0.26,
                    font_size=9, color=C_AMBER, font_name="Courier New")
        dir_color = C_GREEN if "Serveur ->" in direction else C_PURPLE
        add_textbox(slide, direction, 2.4, y + 0.05, 1.7, 0.26,
                    font_size=8.5, color=dir_color)
        add_textbox(slide, desc, 4.2, y + 0.05, 3.5, 0.26,
                    font_size=9, color=C_WHITE)

    # Right column - Ring buffer + CORS
    add_card(slide, 8.05, 1.25, 4.78, 3.2)
    add_textbox(slide, "Ring Buffer par symbole", 8.25, 1.35, 4.38, 0.4,
                font_size=12, bold=True, color=C_GREEN)
    rb_lines = [
        "Chaque symbole dispose d'un buffer",
        "circulaire de 500 metriques en memoire.",
        "",
        "Permet de servir l'historique sans",
        "persistance base de donnees.",
        "",
        "const ringBuffers = new Map<",
        "  string,",
        "  CircularBuffer<Metrics>",
        ">()  // keyed by symbol",
        "",
        "A chaque message Kafka: push() O(1)",
        "A chaque requete /history: getAll()",
    ]
    for i, line in enumerate(rb_lines):
        color = C_WHITE
        fn = "Calibri"
        if any(kw in line for kw in ["const", "Map<", "string,", ">()", "CircularBuffer"]):
            color = C_GREEN
            fn = "Courier New"
        add_textbox(slide, line, 8.25, 1.83 + i * 0.25, 4.38, 0.25,
                    font_size=9, color=color, font_name=fn)

    add_card(slide, 8.05, 4.62, 4.78, 2.13)
    add_textbox(slide, "CORS et Securite", 8.25, 4.72, 4.38, 0.4,
                font_size=12, bold=True, color=C_RED)
    cors_lines = [
        "- CORS: origines whitelist strictes",
        "- Helmet: headers HTTP securises",
        "- Rate limiting: 100 req/min/IP",
        "- Validation Zod: env vars au demarrage",
        "- Socket.IO: validation namespace",
        "- Non-root Docker: user node:node",
    ]
    for i, line in enumerate(cors_lines):
        add_textbox(slide, line, 8.25, 5.2 + i * 0.28, 4.38, 0.28,
                    font_size=9.5, color=C_MUTED)

    add_footer(slide, 7)


def slide_08_dashboard(prs):
    """Slide 8: Dashboard."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Dashboard - Interface Temps Reel")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # Dashboard mockup (text-based)
    add_card(slide, 0.5, 1.3, 7.7, 5.45, bg=RGBColor(0x0D, 0x14, 0x22))
    add_highlight_bar(slide, 0.5, 1.3, 7.7, 0.06, C_AMBER)

    add_textbox(slide, "[ Crypto Market Monitor ]  BTC/USDT  ETH/USDT  BTC-USD",
                0.65, 1.4, 7.4, 0.32, font_size=9, color=C_AMBER, font_name="Courier New")

    add_card(slide, 0.65, 1.8, 2.2, 0.85, bg=RGBColor(0x1A, 0x25, 0x38))
    add_textbox(slide, "PRIX ACTUEL", 0.75, 1.85, 2.0, 0.25,
                font_size=7, color=C_MUTED)
    add_textbox(slide, "$43,210.50", 0.75, 2.1, 2.0, 0.45,
                font_size=16, bold=True, color=C_GREEN, font_name="Courier New")

    add_card(slide, 3.05, 1.8, 2.2, 0.85, bg=RGBColor(0x1A, 0x25, 0x38))
    add_textbox(slide, "VWAP", 3.15, 1.85, 2.0, 0.25,
                font_size=7, color=C_MUTED)
    add_textbox(slide, "$43,089.20", 3.15, 2.1, 2.0, 0.45,
                font_size=16, bold=True, color=C_AMBER, font_name="Courier New")

    add_card(slide, 5.45, 1.8, 2.55, 0.85, bg=RGBColor(0x1A, 0x25, 0x38))
    add_textbox(slide, "SMA-20", 5.55, 1.85, 2.35, 0.25,
                font_size=7, color=C_MUTED)
    add_textbox(slide, "$42,950.75", 5.55, 2.1, 2.35, 0.45,
                font_size=16, bold=True, color=C_PURPLE, font_name="Courier New")

    # Chart representation
    add_card(slide, 0.65, 2.8, 7.3, 2.4, bg=RGBColor(0x0F, 0x17, 0x2A))
    add_textbox(slide, "Prix (BTC/USDT) - Chart.js Line + Volume Bars",
                0.75, 2.88, 7.1, 0.28, font_size=8, color=C_MUTED)

    chart_line = "43500 |              *                                    "
    chart_line2 = "43000 |         *       *   *  *  *  *                    "
    chart_line3 = "42500 |   *  *                       *  *  *  *  *  *    "
    chart_line4 = "42000 +--------------------------------------------->>   "
    add_textbox(slide, chart_line, 0.75, 3.25, 7.1, 0.25, font_size=7.5, color=C_GREEN, font_name="Courier New")
    add_textbox(slide, chart_line2, 0.75, 3.5, 7.1, 0.25, font_size=7.5, color=C_GREEN, font_name="Courier New")
    add_textbox(slide, chart_line3, 0.75, 3.75, 7.1, 0.25, font_size=7.5, color=C_GREEN, font_name="Courier New")
    add_textbox(slide, chart_line4, 0.75, 4.0, 7.1, 0.25, font_size=7.5, color=C_MUTED, font_name="Courier New")

    # Anomaly feed
    add_card(slide, 0.65, 5.35, 7.3, 1.25, bg=RGBColor(0x1A, 0x10, 0x10))
    add_textbox(slide, "!! ANOMALIE DETECTEE  BTC/USDT  z-score: 3.12  Prix: $43,210  14:32:07",
                0.75, 5.45, 7.1, 0.3, font_size=8.5, color=C_RED, font_name="Courier New")
    add_textbox(slide, "!! ANOMALIE DETECTEE  ETH/USDT  z-score: 2.78  Prix: $2,890   14:31:55",
                0.75, 5.78, 7.1, 0.3, font_size=8.5, color=C_AMBER, font_name="Courier New")
    add_textbox(slide, "[son AudioContext active sur anomalie]",
                0.75, 6.1, 7.1, 0.35, font_size=8, color=C_MUTED, font_name="Courier New")

    # Right column - Tech stack
    add_card(slide, 8.45, 1.3, 4.38, 5.45)
    add_textbox(slide, "Stack Frontend", 8.65, 1.4, 3.98, 0.4,
                font_size=13, bold=True, color=C_AMBER)

    stack_items = [
        ("HTML/CSS/JS vanilla", "Pas de framework - bundle minimal"),
        ("Chart.js", "Graphiques temps reel (line + bar)"),
        ("Socket.IO Client", "Reception push depuis l'API"),
        ("CSS Variables", "Theming dark mode coherent"),
        ("AudioContext API", "Beep sur detection anomalie"),
        ("Glassmorphism", "Cards semi-transparentes (backdrop-blur)"),
        ("CSS Grid/Flex", "Layout responsive adaptatif"),
    ]
    for i, (tech, desc) in enumerate(stack_items):
        y = 1.95 + i * 0.52
        add_card(slide, 8.65, y, 3.98, 0.45, bg=RGBColor(0x0F, 0x17, 0x2A))
        add_textbox(slide, tech, 8.75, y + 0.04, 1.55, 0.37,
                    font_size=9.5, bold=True, color=C_AMBER)
        add_textbox(slide, desc, 10.35, y + 0.04, 2.18, 0.37,
                    font_size=8.5, color=C_MUTED)

    add_textbox(slide, "i18n FR/EN integre", 8.65, 5.7, 3.98, 0.3,
                font_size=10, bold=True, color=C_PURPLE)
    add_textbox(slide, "Bascule de langue sans rechargement, persistance localStorage",
                8.65, 6.0, 3.98, 0.45, font_size=8.5, color=C_WHITE)

    add_footer(slide, 8)


def slide_09_securite(prs):
    """Slide 9: Securite."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_RED)
    add_slide_title(slide, "Securite - Mesures et Durcissement")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_RED)

    categories = [
        ("HTTP & API", C_RED, [
            "helmet: Content-Security-Policy, X-Frame-Options,",
            "  HSTS, X-Content-Type-Options",
            "express-rate-limit: 100 req/min par IP",
            "CORS: origines autorisees explicites (whitelist)",
            "Pas de stack trace exposee au client HTTP",
        ]),
        ("Validation & Env", C_AMBER, [
            "Zod: validation stricte des variables d'env",
            "  au demarrage (echec fast-fail si manquante)",
            "Aucun secret en dur dans le code source",
            "Variables sensibles via .env (gitignore)",
            "Types TypeScript stricts (noImplicitAny: true)",
        ]),
        ("Docker & Infra", C_GREEN, [
            "Containers non-root: USER node:node",
            "Images Alpine/Distroless: surface d'attaque reduite",
            "Healthchecks sur chaque service",
            "Reseau Docker isole (bridge interne)",
            "Pas de ports inutiles exposes vers l'hote",
        ]),
        ("Donnees & Connexions", C_PURPLE, [
            "WebSocket: reconnexion avec backoff exponentiel",
            "Kafka: pas d'auth en dev local (acceptable)",
            "Ring buffers: pas de persistance disque de donnees brutes",
            "Logs: sans donnees sensibles utilisateur",
            "OWASP Top 10: verification XSS, injection, IDOR",
        ]),
    ]

    for i, (cat, color, items) in enumerate(categories):
        col = i % 2
        row = i // 2
        x = 0.5 + col * 6.45
        y = 1.3 + row * 3.15
        add_card(slide, x, y, 6.2, 2.9)
        add_highlight_bar(slide, x, y, 0.08, 2.9, color)
        add_textbox(slide, cat, x + 0.25, y + 0.1, 5.7, 0.42,
                    font_size=13, bold=True, color=color)
        for j, item in enumerate(items):
            add_textbox(slide, item, x + 0.25, y + 0.65 + j * 0.42, 5.8, 0.42,
                        font_size=9.5, color=C_WHITE if not item.startswith(" ") else C_MUTED)

    add_footer(slide, 9)


def slide_10_i18n(prs):
    """Slide 10: Multilinguisme i18n."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_PURPLE)
    add_slide_title(slide, "Multilinguisme - Module i18n FR/EN")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_PURPLE)

    # Architecture
    add_card(slide, 0.5, 1.3, 5.5, 5.45)
    add_textbox(slide, "Architecture i18n", 0.7, 1.4, 5.1, 0.4,
                font_size=13, bold=True, color=C_PURPLE)
    arch_lines = [
        "Module: dashboard/js/i18n.js",
        "",
        "Principe:",
        "- Attribut data-i18n sur chaque element HTML",
        "- Dictionnaire JS par langue (fr, en)",
        "- Fonction t(key) retourne la traduction",
        "- Bascule sans rechargement de page",
        "- Langue persistee en localStorage",
        "",
        "Exemple HTML:",
        '<span data-i18n="price">Prix</span>',
        "",
        "Exemple JS:",
        "document.querySelectorAll('[data-i18n]')",
        "  .forEach(el => {",
        "    el.textContent = t(el.dataset.i18n)",
        "  })",
        "",
        "Langues supportees: FR (defaut), EN",
        "Clef manquante: fallback vers FR",
    ]
    for i, line in enumerate(arch_lines):
        color = C_WHITE
        fn = "Calibri"
        if line.startswith("<") or "querySelectorAll" in line or "forEach" in line or "el.textContent" in line or "}" in line or "el.dataset" in line:
            color = C_GREEN
            fn = "Courier New"
        elif line.startswith("- "):
            color = C_MUTED
        add_textbox(slide, line, 0.7, 1.9 + i * 0.26, 5.1, 0.26,
                    font_size=9, color=color, font_name=fn)

    # Translation keys table
    add_card(slide, 6.25, 1.3, 6.58, 5.45)
    add_textbox(slide, "Cles de traduction (extrait)", 6.45, 1.4, 6.18, 0.4,
                font_size=13, bold=True, color=C_AMBER)

    keys = [
        ("Cle", "FR", "EN"),
        ("title", "Surveillance Crypto", "Crypto Monitor"),
        ("price", "Prix actuel", "Current price"),
        ("volume", "Volume", "Volume"),
        ("anomaly", "Anomalie detectee", "Anomaly detected"),
        ("vwap", "VWAP", "VWAP"),
        ("sma", "Moyenne mobile 20", "Moving avg 20"),
        ("change1m", "Variation 1 min", "1 min change"),
        ("change5m", "Variation 5 min", "5 min change"),
        ("lang_toggle", "EN", "FR"),
        ("status_connected", "Connecte", "Connected"),
        ("status_disconnected", "Deconnecte", "Disconnected"),
        ("last_update", "Derniere mise a jour", "Last update"),
    ]

    for i, (key, fr, en) in enumerate(keys):
        y = 1.85 + i * 0.35
        if i == 0:
            bg = RGBColor(0x1E, 0x29, 0x3B)
            key_color = C_MUTED
            fr_color = C_MUTED
            en_color = C_MUTED
            bold = True
        else:
            bg = RGBColor(0x0F, 0x17, 0x2A) if i % 2 else RGBColor(0x17, 0x20, 0x33)
            key_color = C_AMBER
            fr_color = C_WHITE
            en_color = C_GREEN
            bold = False
        add_card(slide, 6.45, y, 6.18, 0.33, bg=bg)
        add_textbox(slide, key, 6.5, y + 0.03, 1.6, 0.27,
                    font_size=9, bold=bold, color=key_color, font_name="Courier New")
        add_textbox(slide, fr, 8.2, y + 0.03, 2.2, 0.27,
                    font_size=9, bold=bold, color=fr_color)
        add_textbox(slide, en, 10.5, y + 0.03, 2.0, 0.27,
                    font_size=9, bold=bold, color=en_color)

    add_footer(slide, 10)


def slide_11_docker(prs):
    """Slide 11: Deploiement Docker."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_NAVY)
    add_highlight_bar(slide, 0, 0, 13.33, 0.06, C_AMBER)
    add_slide_title(slide, "Deploiement - Docker Compose")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # Services table
    add_textbox(slide, "Services Docker Compose", 0.5, 1.25, 8.0, 0.38,
                font_size=13, bold=True, color=C_AMBER)

    services = [
        ("kafka", "confluentinc/cp-kafka:7.6", "9092:9092", "Broker Kafka en mode KRaft"),
        ("kafka-ui", "provectus/kafka-ui:latest", "8080:8080", "Interface web monitoring Kafka"),
        ("ingester", "node:20-alpine", "—", "Collecte WebSocket Binance + Coinbase"),
        ("processor", "node:20-alpine", "—", "Calcul VWAP, SMA, Z-score"),
        ("api", "node:20-alpine", "3000:3000", "API Express + Socket.IO"),
        ("dashboard", "nginx:alpine", "8000:80", "Serve HTML/CSS/JS via nginx"),
    ]

    header_y = 1.7
    add_card(slide, 0.5, header_y, 12.33, 0.38, bg=RGBColor(0x1E, 0x29, 0x3B))
    for col, (text, width, x) in enumerate([
        ("Service", 1.5, 0.6),
        ("Image", 2.8, 2.2),
        ("Ports", 1.5, 5.1),
        ("Role", 4.5, 6.7),
    ]):
        add_textbox(slide, text, x, header_y + 0.05, width, 0.28,
                    font_size=9, bold=True, color=C_MUTED)

    for i, (svc, image, ports, role) in enumerate(services):
        y = 2.15 + i * 0.5
        bg = RGBColor(0x0F, 0x17, 0x2A) if i % 2 == 0 else RGBColor(0x17, 0x20, 0x33)
        add_card(slide, 0.5, y, 12.33, 0.47, bg=bg)
        add_highlight_bar(slide, 0.5, y, 0.04, 0.47, C_AMBER if i < 2 else C_GREEN)
        add_textbox(slide, svc, 0.65, y + 0.07, 1.45, 0.33,
                    font_size=9.5, bold=True, color=C_AMBER, font_name="Courier New")
        add_textbox(slide, image, 2.2, y + 0.07, 2.8, 0.33,
                    font_size=8.5, color=C_MUTED, font_name="Courier New")
        add_textbox(slide, ports, 5.1, y + 0.07, 1.5, 0.33,
                    font_size=9, color=C_GREEN, font_name="Courier New")
        add_textbox(slide, role, 6.7, y + 0.07, 5.9, 0.33,
                    font_size=9, color=C_WHITE)

    # Healthchecks + volumes
    add_card(slide, 0.5, 5.2, 5.9, 2.1)
    add_textbox(slide, "Healthchecks", 0.7, 5.3, 5.5, 0.38,
                font_size=12, bold=True, color=C_GREEN)
    hc_lines = [
        "kafka:    nc -z localhost 9092",
        "api:      curl -f /api/health",
        "dashboard: curl -f /",
        "",
        "interval: 10s  timeout: 5s  retries: 5",
        "Dependences: ingester/processor dependent de kafka",
    ]
    for i, line in enumerate(hc_lines):
        fn = "Courier New" if any(kw in line for kw in ["nc ", "curl", "interval"]) else "Calibri"
        color = C_GREEN if line.startswith("kafka") or line.startswith("api") or line.startswith("dash") else C_MUTED
        add_textbox(slide, line, 0.7, 5.78 + i * 0.25, 5.5, 0.25,
                    font_size=9, color=color, font_name=fn)

    add_card(slide, 6.65, 5.2, 6.18, 2.1)
    add_textbox(slide, "Volumes et demarrage", 6.85, 5.3, 5.78, 0.38,
                font_size=12, bold=True, color=C_AMBER)
    vol_lines = [
        "Volume: kafka_data (donnees Kafka persistees)",
        "",
        "Commandes:",
        "  docker compose up -d     # demarrage",
        "  docker compose logs -f   # logs live",
        "  docker compose down -v   # reset complet",
        "",
        "Acces services apres demarrage:",
        "  Dashboard:  http://localhost:8000",
        "  API REST:   http://localhost:3000/api",
        "  Kafka UI:   http://localhost:8080",
    ]
    for i, line in enumerate(vol_lines):
        fn = "Courier New" if line.strip().startswith(("docker", "http", "kafka_data")) else "Calibri"
        color = C_AMBER if line.strip().startswith("http") else (C_GREEN if "docker" in line else C_WHITE)
        add_textbox(slide, line, 6.85, 5.78 + i * 0.25, 5.78, 0.25,
                    font_size=9, color=color, font_name=fn)

    add_footer(slide, 11)


def slide_12_conclusion(prs):
    """Slide 12: Conclusion et bilan."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, C_DARK)
    add_highlight_bar(slide, 0, 0, 13.33, 0.08, C_AMBER)
    add_highlight_bar(slide, 0, 0.08, 0.08, 7.42, C_PURPLE)
    add_slide_title(slide, "Conclusion et Bilan")
    add_highlight_bar(slide, 0.5, 1.1, 4.0, 0.04, C_AMBER)

    # Accomplishments
    add_card(slide, 0.5, 1.3, 5.8, 3.4, bg=RGBColor(0x0F, 0x17, 0x2A))
    add_textbox(slide, "Ce qui a ete realise", 0.7, 1.4, 5.4, 0.4,
                font_size=13, bold=True, color=C_GREEN)
    done_items = [
        "Pipeline complet: WebSocket -> Kafka -> Analytics -> Dashboard",
        "Kafka KRaft sans Zookeeper (production-ready)",
        "3 feeds WebSocket: Binance (x2 symboles) + Coinbase",
        "3 indicateurs temps reel: VWAP, SMA-20, Z-score anomaly",
        "Dashboard live avec Chart.js + alertes sonores",
        "i18n FR/EN sans framework, persistance localStorage",
        "Securite: helmet + rate-limit + Zod validation + CORS",
        "Deploiement Docker Compose 6 services avec healthchecks",
        "Realise par 2 personnes (projet prevu pour 4)",
    ]
    for i, item in enumerate(done_items):
        add_textbox(slide, "OK  " + item, 0.7, 1.9 + i * 0.34, 5.4, 0.32,
                    font_size=9.5, color=C_WHITE)

    # Perspectives
    add_card(slide, 6.65, 1.3, 6.18, 3.4, bg=RGBColor(0x0F, 0x17, 0x2A))
    add_textbox(slide, "Perspectives et evolutions", 6.85, 1.4, 5.78, 0.4,
                font_size=13, bold=True, color=C_PURPLE)
    future_items = [
        "Persistance: TimescaleDB ou InfluxDB pour historique long terme",
        "Alertes: notifications Telegram/email sur anomalie",
        "Machine Learning: prediction de tendance (LSTM, Prophet)",
        "Broker secondaire: Kraken ou OKX pour diversite",
        "Auth utilisateur: JWT + gestion de portefeuilles",
        "Backtest: replay de donnees historiques sur le pipeline",
        "CI/CD: GitHub Actions + tests automatises E2E",
        "Monitoring: Prometheus + Grafana pour metriques infra",
    ]
    for i, item in enumerate(future_items):
        add_textbox(slide, "+  " + item, 6.85, 1.9 + i * 0.34, 5.78, 0.32,
                    font_size=9.5, color=C_MUTED)

    # Skills acquired
    add_card(slide, 0.5, 4.85, 12.33, 1.9, bg=RGBColor(0x0F, 0x17, 0x2A))
    add_textbox(slide, "Competences acquises", 0.7, 4.95, 11.9, 0.4,
                font_size=12, bold=True, color=C_AMBER)
    skills = [
        "Apache Kafka KRaft",
        "WebSocket haute-freq.",
        "Analytics temps reel",
        "TypeScript strict",
        "Docker Compose",
        "Socket.IO push",
        "Securite API",
        "i18n vanilla JS",
    ]
    sk_w = 12.33 / len(skills) - 0.1
    for i, sk in enumerate(skills):
        x = 0.6 + i * (sk_w + 0.1)
        add_card(slide, x, 5.4, sk_w, 0.75, bg=RGBColor(0x1E, 0x29, 0x3B))
        add_textbox(slide, sk, x, 5.4, sk_w, 0.75,
                    font_size=8.5, bold=True, color=C_AMBER, align=PP_ALIGN.CENTER)

    add_textbox(slide, "Adam Beloucif  -  Emilien Morice  -  M1 Data Engineering & IA  -  EFREI Paris 2025-2026",
                0.5, 6.9, 12.33, 0.3, font_size=9, color=C_MUTED, align=PP_ALIGN.CENTER)
    add_highlight_bar(slide, 0.08, 7.42, 13.25, 0.08, C_AMBER)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slide_01_title(prs)
    slide_02_contexte(prs)
    slide_03_architecture(prs)
    slide_04_kafka(prs)
    slide_05_ingester(prs)
    slide_06_processor(prs)
    slide_07_api(prs)
    slide_08_dashboard(prs)
    slide_09_securite(prs)
    slide_10_i18n(prs)
    slide_11_docker(prs)
    slide_12_conclusion(prs)

    out_dir = os.path.join(os.path.dirname(__file__))
    out_path = os.path.join(out_dir, "crypto-market-monitor.pptx")
    prs.save(out_path)
    print(f"PPTX saved: {out_path}")
    size = os.path.getsize(out_path)
    print(f"File size: {size:,} bytes ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
