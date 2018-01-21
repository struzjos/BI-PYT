Svou semestrální práci jsem udělal jako balíček plug-inů do Gimpu. Nainstalování plag-inů je velmi jednoduché stačí je uložit do složky "plug-ins" a gimp si je při spuštění sám načte. Na linuxu je cesta k této složce jednoduchá ~/.gimp-2.8/plug-ins/ (plus nesmíme zapomenout přidat souborům právo exucutable), na windows plag-iny také fungují, ale někdy se objevují problémy s načtením, cesta na windows je C:\Program Files\GIMP #\lib\gimp\#.#\plug-ins (# - verze gimpu). Filtery poté najdeme pod "Filters"->"JS-Filters".

Filtry:

Flip: tento filtr převrátí obraz buď vertikálně nebo horizontálně

Shift colors: tento filter obraz ztmavý nebo zesvětlí o zadanou konstantu.

Shift colors by mutiplying: tento filter obraz ztmavý nebo zesvětlí o násobek zadané konstanty.

Emboss, Gaussian blur a Sharpen: tyto filtery provedou úpravu obrazu pomocí matice.

Negative, Noise: oba tyto fltry využívají broadcasting v numpy. Negativ jak již název napovídá udělá negative a Noise udělá šum, buď pro všechny kanály stejně nebo pro každý zvlášť.

Sepia, Monochrome: sepia udělá efekt staré fotografie a monochrome převede obraz do odstínu šedi.

Color filter: toto je nejslozitejsi filtr jaky jsem udelal, uzivatel si zvoli barvu a rozpeti a filter prevede cely obraz do odstinu sedi az na uzivatelem zadanou barvu v zadanem rozpeti.