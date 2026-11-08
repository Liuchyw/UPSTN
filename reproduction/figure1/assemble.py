from pathlib import Path
import pymupdf as fitz
HERE=Path(__file__).resolve().parent;OUT=HERE/'output';MM=72/25.4
doc=fitz.open();p=doc.new_page(width=183*MM,height=105*MM)
for name,rect in [('a_traffic_structure',(0,0,80*MM,105*MM)),('b_paired_horizon_differences',(84*MM,0,183*MM,50*MM)),('c_fixed_day_loss_effects',(84*MM,52*MM,183*MM,105*MM))]:
    with fitz.open(OUT/(name+'.pdf')) as src:p.show_pdf_page(fitz.Rect(rect),src,0)
p.draw_line((82*MM,1*MM),(82*MM,104*MM),color=(.35,.35,.35),width=.65,dashes='[3 3] 0')
p.draw_line((84*MM,51*MM),(183*MM,51*MM),color=(.35,.35,.35),width=.65,dashes='[3 3] 0')
doc.save(OUT/'Figure1_motivation_diagram.pdf',garbage=4,deflate=True)
p.get_pixmap(dpi=300).save(OUT/'Figure1_motivation_diagram.png')
