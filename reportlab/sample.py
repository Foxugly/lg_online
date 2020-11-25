# -*- coding: utf-8 -*-
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class LGCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def show_page(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.header()
            self.footer()
            canvas.Canvas.show_page(self)
        canvas.Canvas.save(self)

    @staticmethod
    def get_image(path, x, y, width=1 * cm):
        img = ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return path, x, y, width, (width * aspect)

    def header(self):
        # self.drawRightString(195*mm, 272*mm, "HEADER1")
        p, x0, y0, x1, y1 = self.get_image('logo_lieutenant_guillaume.png', 20 * mm, 262 * mm, 8 * cm)
        self.drawImage(p, x0, y0, x1, y1, mask="auto")
        # self.drawString(195*mm, 252*mm, "HEADER2")

    def footer(self):
        self.drawRightString(200 * mm, 20 * mm, "FOOTER")


class Procuration:
    def __init__(self, *args, **kwargs):
        self.doc = SimpleDocTemplate("procuration.pdf", pagesize=A4, rightMargin=72, leftMargin=72, topMargin=120,
                                     bottomMargin=18)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=12, ))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=24, ))
        self.text = []
        ptext = '<b>Procuration</b>'
        self.text.append(Paragraph(ptext, styles["Center"]))
        self.text.append(Spacer(0, 50))
        p = '''Je soussignée [NOM SOCIETE] ([NUM TVA]) dont le siège est situé [RUE] [NUM] - [code postal] [COMMUNE] (BE),'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        p = '''Représenté(e) par : [Nom Gérant], N.N. : [numéro national], résidante à [adresse résidence] ;'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        p = '''En sa qualité de gérant de [NOM SOCIETE Sprl] ; [NUM TVA]'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        p = '''Dont le siège est situé [adresse siège] (BE)'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        p = '''Déclare par la présente donner mandat et procuration à L.G. & Associates SCSPRL – 29 avenue Reine Marie Henriette à 1190 Forest, BE0454.784.696, Cabinet de comptabilité agréé sous le numéro IPCF: 70483836, pouvant être représenté par Monsieur Olivier Guillaume ou l’un de ses collaborateurs pour :'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        ptext = '''<ul>
        <li>intervenir en leur nom et pour leur compte auprès de l’administration des contributions directes, de l’administration de la TVA et de l’enregistrement et des domaines pour signer et introduire les déclarations ;</li>
        <li>rédiger les réponses aux questions, aux demandes d’informations, aux avis de modifications, déclarations de régularisations et réclamations ;</li>
        <li>mener des discussions et signer des accords avec les services de contrôle et la direction et les représenter dans leurs relations avec les administrations précitées.</li>
        </ul>'''
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        p = '''De plus, tous les renseignements à cette fin peuvent être pris auprès de tierces personneset d’institutions et tous les documents nécessaires être signés par le mandataire.'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        p = '''Par ailleurs, le mandataire est autorisé à transférer à des tiers la présente procuration par le biais d’une procuration spéciale.'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.text.append(Spacer(0, 10))
        p = '''L’actuelle procuration restera valable hormis révocation écrite et expresse signifiée au mandataire et à l’Administration.'''
        ptext = '%s' % p
        self.text.append(Paragraph(ptext, styles["Justify"]))
        self.doc.build(self.text, canvasmaker=LGCanvas)


if __name__ == "__main__":
    proc = Procuration()
