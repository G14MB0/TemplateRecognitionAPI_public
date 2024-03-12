import cv2
import numpy as np

# Carica l'immagine originale e l'immagine di riferimento
img = cv2.imread('lancette.jpg', 0) # Immagine target
template = cv2.imread('lancetta.jpg', 0) # Immagine di riferimento

# Genera immagini di bordi usando Canny
# edges_img = cv2.Canny(img, 50, 150)
# edges_template = cv2.Canny(template, 50, 150)

# Inizializza il detector e il matcher
orb = cv2.ORB_create(nfeatures=1500)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Trova i keypoints e i descrittori con ORB
kp1, des1 = orb.detectAndCompute(img, None)
kp2, des2 = orb.detectAndCompute(template, None)

# Effettua il matching dei descrittori
matches = bf.match(des1, des2)

# Filtra i matches (questo passaggio è opzionale e dipende dal contesto)
# matches = sorted(matches, key=lambda x: x.distance)

# Disegna i primi 10 matches
img_matches = cv2.drawMatches(img, kp1, template, kp2, matches[:10], None, flags=2)

# Mostra l'immagine
cv2.imshow('Matches', img_matches)
cv2.waitKey(0)
cv2.destroyAllWindows()
