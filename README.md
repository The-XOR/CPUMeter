# CPUMeter
Una pazzia computer-motoristica

Il gauge che ho utilizzato e' cus qui: 
un contagiri elettronico a 12 voltaggi.

Preliminari (sempre importanti):
- aprire il gauge, scollegare lo strumento a lancetta dal circuito elettronico interno e portare i fili fuori: verra' comandato direttamente dal circuito esterno.

- Lista della spesa:
  - n. 1 contagiri (senza, l'intero progetto perde un po' di senso). Quello utilizzato e' questo qui:
      https://it.aliexpress.com/item/1005007490570643.html
  - n. 1 DC/DC booster. Il gauge e' alimentato a 12 voltaggi, quindi serve un po' di sprint. Quello che ho    
      utilizzato e' questo qui: https://it.aliexpress.com/item/1005006031037900.html
  - n. 1 RP2040-Zero (https://it.aliexpress.com/item/1005006865919374.html)
  - n. 1 resistenza 820ohm
  - n. 1 resistenza 1 Kohm
  - n. 3 resistenze 10 Kohm
  - n. 2 condensatori ceramici 1000 nF
  - n. 3 transistor NPN tipo 2N2222 o simili

- Taratura DC/DC booster:
  collegare il DCDCB ai pin 1 et 2 del RP2040 (rispettivamente +5V e GND). Con un tester, regolare la tensione
  di uscita a 11.2V

- Software:
  Caricare il micropitone sull'RP2040 quindi copiare il file pwm.py

- Uso:
  Una volta avviato il software del microcontrollore, questo aspetta un byte (valori da 0 a 100) corrispondente
  al valore del carico attuale della CPU. Se il byte viene ricevuto correttamente, si accende la retroilluminazione del gauge e la lancetta viene portata sul valore corrispondente

Questa repository contiene una sorta di scheletro in linguaggio autohotkey per mandare periodicamente (ogni secondo) il valore di carico della CPU sulla porta seriale

