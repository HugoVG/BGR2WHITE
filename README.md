﻿# BGR2WHITE
 Applicatie voor het verwijderen van een grijze achtergrond.
 door middel van OpenCV2 en PILLOW
 OpenCV2 zoekt voor contouren dit is niet aan te raden bij je standaard foto's maar wel bij foto's van model van ver af
 de OpenCV2 Functie wordt benoemd als BGR2WHITE in de code.
 de PILLOW functie zoekt voor elke pixel waarbij de band van R, G en B groter is dan 223 in alle kleur banden
 stel een pixel is RGB(240,242,255), Dan wordt deze opgesplits in R(240) G(242) B(255), dan wordt geëvalueerd of de band groter is dan 223
 if pixel[x,y][0] and pixel[x,y][1] and pixel[x,y][2] > 223 
 dan maakt het deze pixel wit #[0] = r, [1] = g, [2] = b.
 
de applicatie is naar exe vertaald met auto-py-to-exe
