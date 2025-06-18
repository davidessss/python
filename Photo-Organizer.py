import os
import datetime
import shutil
import sys
import logging
from tqdm import tqdm
 
# Configura il logging
logging.basicConfig(
    filename='photo_organizer.log',  # Nome del file di log
    level=logging.INFO,  # Impostiamo il livello di log (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
)
 
mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
 
img = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".gif", ".webp", ".svg", ".apng", ".avif")
 
video = (".webm", ".mts", ".m2ts", ".TS", ".mov", ".mp4", ".m4p", ".m4v", ".mxf")
 
imgraw = (".nef", ".cr2", ".cr3")
 
def main():
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)
 
    SD = sys.argv[1]
    HardDisk = sys.argv[2]    
    logging.info(f"Percorso SD: {SD}")
    logging.info(f"Percorso HD: {HardDisk}")
 
    JPG = HardDisk + "JPG/"
    RAW = HardDisk + "RAW/"
    VIDEO = HardDisk + "VIDEO/"
 
    NumJPGCopiati = 0
    NumJPGNonCopiati = 0
    NumRAWCopiati = 0
    NumRAWNonCopiati = 0
    NumVIDEOCopiati = 0
    NumVIDEONonCopiati = 0
    NumFileEstSbagliata = 0
    NumFileNonCopiati = 0
    file_list = []
     
    for root, dirs, files in os.walk(SD):
        for file in files:
            file_list.append((root, file))
 
    for root, file in tqdm(file_list, desc="Copia file", unit="file"):
        if is_image(file):
            if copia_file(JPG, root, file):
                NumJPGCopiati += 1
            else:
                NumJPGNonCopiati += 1
        elif is_raw(file):
            if copia_file(RAW, root, file):
                NumRAWCopiati += 1
            else:
                NumRAWNonCopiati += 1
        elif is_video(file):
            if copia_file(VIDEO, root, file):
                NumVIDEOCopiati += 1
            else:
                NumVIDEONonCopiati += 1
        else:
            logging.warning(f"{file} - Estensione Sbagliata")
            NumFileEstSbagliata += 1
 
    logging.info(f"Numero JPG COPIATI = {NumJPGCopiati}")
    logging.info(f"Numero JPG Non COPIATI = {NumJPGNonCopiati}")
    logging.info(f"Numero RAW COPIATI = {NumRAWCopiati}")
    logging.info(f"Numero RAW Non COPIATI = {NumRAWNonCopiati}")
    logging.info(f"Numero VIDEO COPIATI = {NumVIDEOCopiati}")
    logging.info(f"Numero VIDEO Non COPIATI = {NumVIDEONonCopiati}")
    logging.info(f"Numero Estensione Sbagliata = {NumFileEstSbagliata}")
     
    TotaleCopiati = NumJPGCopiati + NumRAWCopiati + NumVIDEOCopiati
    TotaleNonCopiati = NumJPGNonCopiati + NumRAWNonCopiati + NumVIDEONonCopiati + NumFileEstSbagliata
     
    logging.info(f"Numero FILE Copiati Totali = {TotaleCopiati}")
    logging.info(f"Numero FILE Non Copiati Totali = {TotaleNonCopiati}")
    logging.info(f"Numero FILE Totali = {TotaleCopiati + TotaleNonCopiati}")
 
def print_help():
    print("Utilizzo:")
    print("  python Photo-Organizer.py <PERCORSO_SORGENTE> <PERCORSO_DESTINAZIONE> ...")
    print("Esempio:")
    print("  python Photo-Organizer.py /media/davide/NIKON D500/DCIM/115ND500/ /home/davide/Immagini/")
    print("\nDescrizione:")
    print("  Questo script accetta due argomenti e copia ")
    print("  immagini (.jpg, .jpeg, .jfif, .pjpeg, .pjp, .png, .gif, .webp, .svg, .apng, .avif)")
    print("  video (.webm, .mts, .m2ts, .TS, .mov, .mp4, .m4p, .m4v, .mxf)")
    print("  immagini RAW (.nef,.cr2,.cr3)")
    print("  Se non inserisci argomenti, mostra questo messaggio di aiuto.")
 
def get_dest_path(cfile, HD, file):
    datafile = datetime.datetime.fromtimestamp(os.path.getmtime(cfile))
    Anno = HD + datafile.strftime("%Y")
    GiornoMese = Anno + "/" + datafile.strftime("%d") + "-" + mesi[int(datafile.strftime("%m"))-1]
    return os.path.join(GiornoMese, file)
 
def is_image(file):
    return os.path.splitext(file)[1].lower() in img
 
def is_raw(file):
    return os.path.splitext(file)[1].lower() in imgraw
 
def is_video(file):
    return os.path.splitext(file)[1].lower() in video
 
def copia_file(HD, root, file):
    cfile = os.path.join(root, file)
    dest_path = get_dest_path(cfile, HD, file)
    if os.path.exists(dest_path):
        logging.info(f"{file} - Già Esistente.")
        return False
    else:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copyfile(cfile, dest_path)
        logging.info(f"{file} - Copiato con successo in {dest_path}")
        return True
 
if __name__ == "__main__":
    main()
