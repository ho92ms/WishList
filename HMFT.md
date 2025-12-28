# Hivatalos Magyar Felelősségmegmaradás Törvénye (HMFT) – Formális Specifikáció (Németh Dávid)

### 1. Definíciók és Jelölésrendszer

Legyen $U$ a teljes univerzum, és $M \subset U$ a zárt magyar rendszer. Definiáljuk az ágensek halmazát:

$$A = \{a_{\text{én}}, a_{\text{te}}, a_{\text{kormány}}, a_{\text{sors}}, \dots\}$$

Legyen $T = [t_0, \infty) \subset \mathbb{R}$ az időtartomány, ahol $t_0$ a kritikus hibaesemény bekövetkezése.

**1.1. Axióma (A Felelősségmegmaradás Törvénye)**
Jelölje $\mathcal{F} : A \times T \rightarrow \mathbb{R}$ a felelősségmérték függvényt. Ekkor minden $t \in T$ időpillanatban teljesül, hogy:

$$\sum_{a \in A} \mathcal{F}(a, t) \equiv C$$

Ahol $C = 1$ (normalizált egységnyi felelősség, azaz 100%).

---

### 2. Az $F_{\text{én}}$ Sajátfüggvény Analízise

Vizsgáljuk az $a_{\text{én}}$ ágenshez tartozó parciális függvényt, legyen ez $f(t) := \mathcal{F}(a_{\text{én}}, t)$.

**2.1. Definíció (A viselkedési egyenlet)**

$$f(t) = -\tanh(t - t_0) - \Theta(t - t_0) + \alpha \cdot \Theta(t - (t_0 + \varepsilon_1)) + \beta \cdot \Theta(t - (t_0 + \varepsilon_2)) $$
$$+ \frac{1}{2} \cdot \mathbb{I}_{\text{szóltam}} $$

Ahol:
*   $\tanh$: Hiperbolikus tangens (a felelősség azonnali telítése a negatív tartományba).
*   $\mathbb{I}_{\text{szóltam}}$: Indikátorváltozó, értéke $1$, ha az „Én szóltam” esemény bekövetkezett, egyébként $0$.
*   $\Theta$: **Heaviside-lépcsőfüggvény**. Értéke $0$, ha az argumentum negatív, és $1$, ha pozitív. (Ez modellezi a diszkrét eseményeket, amikor a felelősség "ugrásszerűen" eltűnik).
*   $\alpha, \beta$: A 3. fejezetben részletezett áthárítási együtthatók.

---

**2.2. Tétel (Aszimptotikus viselkedés)**
A függvény határértékei a kritikus pontokban:

$$\lim_{t \to t_0} f(t) \approx -1 + \frac{1}{2} \cdot \mathbb{I}_{\text{szóltam}} \quad (-100\%)$$

A végtelenben a rendszer beáll egy stabil, de elérhetetlen állapotba:
$$\lim_{t \to \infty} f(t) = \sup \{ M \mid M \in \text{Morális Magaslat} \}$$

*Bizonyítás:* A $\lim_{x \to \infty} \tanh(x) = 1$ tulajdonság és a l'Hôpital-szabály triviális alkalmazásával adódik.

*(Megjegyzés: Ha 𝕀<sub>szóltam</sub> = 1, akkor a bűntudat mértéke csak -50%, de a rendszer globális állapota ettől még összeomlott.)*



Nézzük meg, miért jön ki a -1 és hogy mit jelent ez:

### 2.2. Tétel ellenőrzése - a kikérem magamnak szingularitás:
A képlet a **t₀** pillanatban (közvetlenül utána, **t → t₀⁺**): 

$$f(t) = \underbrace{-\tanh(0)}_{\approx 0} - \underbrace{\Theta(0^+)}_{1} + \underbrace{\text{többi tag}}_{0} = -1$$


Tehát **számításilag helyes**, a határérték tényleg -1.

### 2.2.1. A "Magyar Valóság" értelmezése (Miért jó a -100%?)
A dokumentum elején deklaráltuk a **Felelősségmegmaradás Törvényét**:

$$
\sum \text{Felelősség} = 1 
$$

-azaz 100%.

Ha a saját felelősség (
$f(t)$
) a hiba pillanatában **-1** (-100%), az a következőt jelenti az egyenlet átrendezésével:

$$
f_{\text{saját}} + f_{\text{többiek}} = 1
$$

$$
-1 + f_{\text{többiek}} = 1
$$

$$
f_{\text{többiek}} = 2 
$$

azaz 200%.

**Mit jelent ez magyarra fordítva?**

Azt, hogy a hiba pillanatában az első reakció nem a semlegesség (0), hanem az **aktív támadás **:
> *"Nem elég, hogy nem én rontottam el (-1), de most még nekem kell helyrehozni azt, amit ti duplán elcs##tetek (+2)!"*
---

### 3. A Felelősségváltozás Dinamikája (Deriváltak)

A felelősség időbeli változását a disztribúcióelmélet eszközeivel írjuk le.

**3.1. Állítás**
A felelősség deriváltja, $f'(t)$ nem folytonos, hanem Dirac-delta impulzusokat tartalmaz:

$$\frac{df}{dt} = \alpha \cdot \delta(t - (t_0 + \varepsilon_1)) + \beta \cdot \delta(t - (t_0 + \varepsilon_2))$$

Ahol:
*   $\delta$: Dirac-delta disztribúció (pillanatszerű hárítás).
*   $\alpha = \text{„De hát te mondtad...” konstans}$.
*   $\beta = \text{„Jószándék” konstans}$.
*   $\varepsilon_{1,2} \to 0$ (az áthárítás reakcióideje elhanyagolhatóan kicsi).

---

### 4. Rendszerdinamika és Vektorterek

Tekintsük a felelősséget vektormezőként: $\mathbf{F}(\mathbf{r}, t)$.

**4.1. Tétel (Divergenciamentesség)**

A rendszer zárt, forrásmentes:

$$\text{div } \mathbf{F} = \nabla \cdot \mathbf{F} = 0$$

*Interpretáció:* A felelősség nem keletkezik és nem szűnik meg, csak vándorol.

---

**4.2. Tétel (Nem konzervatív erőtér)**

A mező rotációja nem zérus:

$$\text{rot } \mathbf{F} = \nabla \times \mathbf{F} \neq \mathbf{0}$$

*Következmény:* A felelősség örvényes mozgást végez az $a_{\text{én}} \to a_{\text{te}} \to a_{\text{körülmények}} \to a_{\text{én}}$ zárt görbén. A rendszerben a munkavégzés (értsd: megoldás keresése) nem útfüggetlen, hanem végtelen ciklusba torkollik.

---

**4.3. Differenciálegyenlet-rendszer (Mátrixos alak)**
Legyen $\mathbf{x}(t)$ a felelősségvektor. Ekkor:

$$\dot{\mathbf{x}}(t) = \mathbf{K} \cdot \mathbf{x}(t)$$

Ahol $\mathbf{K}$ az $n \times n$-es *Áthárítási Mátrix*, melyre igaz, hogy $\det(\mathbf{K}) \neq 0$ (a probléma nem triviális).

---

### 5. A Főtétel (HMFT I.)

**Tétel:** Minden magyar topológiai térben a felelősség $L_1$ normája állandó, de a lokális fluktuáció mértéke elérheti a $\pm 2C$ értéket az $O(\text{anyós})$ környezetben.

**Bizonyítás (Indirekt):** Tegyük fel, hogy létezik olyan **t\***, ahol valaki vállalja a felelősséget (**Fₑₙ(t\*) = 1**). Ebből következne, hogy a rendszer nem magyar, ami ellentmond a kiindulási feltételnek (**M ⊂ Magyarország**). Ellentmondásra jutottunk. ■


---

### 6. Komplexitáselméleti Megközelítés

Vizsgáljuk a felelős megtalálásának számítási igényét a $M$ rendszerben.

**6.1. Definíció (A Felelős-Keresési Probléma - FKP)**
Adott egy $G(V, E)$ irányított gráf (úgynevezett *Szervezeti Ábra*), ahol $v \in V$ a munkavállalók, és $e(u,v) \in E$ a „tedd át másra” reláció. A feladat találni egy olyan $v_{felelös}$ csúcsot, amelyre $\text{deg}(v) = 0$ (nyelő csúcs).

---

**6.2. Tétel (NP-nehézség)**
Az FKP probléma $\text{NP}$-teljes, sőt, a gyakorlatban gyakran eldönthetetlen (hasonlóan a Megállási Problémához).

*Bizonyítás:* Redukáljuk a problémát a *Hamilton-körre*. Ha a felelősség egy zárt körben halad (pl. Ügyintéző $\to$ Osztályvezető $\to$ Portás $\to$ Ügyintéző), akkor a keresési algoritmus végtelen ciklusba lép. Mivel a magyar bürokráciában a körök létezése garantált (lásd 4.2 Tétel), az algoritmus sosem terminál. A futásidő $O(\text{hivatali-ügyintézési-határidő}^n)$, ahol $n \to \infty$.

---

### 7. A Kvantum-bürokrácia Elmélete

A klasszikus fizika nem képes leírni a pályázati pénzek viselkedését, ezért bevezetjük a kvantummechanikai formalizmust.

**7.1. Tétel (Schrödinger Munkavégzése)**
Legyen $\Psi$ a "Megcsináltam a feladatot" állapotfüggvény. Amíg a főnök (megfigyelő) nem nyitja ki az irodaajtót, a munka állapota szuperpozícióban van:

$$|\Psi\rangle = \frac{1}{\sqrt{2}} \big( | \text{Kész} \rangle + | \text{Még hozzá se kezdtem} \rangle \big)$$

---

**7.2. A Heisenberg-féle Pályázati Határozatlanság**
Jelölje $\Delta x$ a projekt megvalósulási helyét (pl. EU-s lombkorona sétány) és $\Delta p$ az eltűnt közpénz mennyiségét. Ekkor:

$$\Delta x \cdot \Delta p \ge \frac{\hbar}{2} \cdot \text{Korrupciós Együttható}$$

*Interpretáció:* Minél pontosabban tudjuk, hogy *hol* épült meg valami (pl. a pusztában), annál kevésbé tudjuk megmondani, *hova* tűnt a pénz, és fordítva.

---

**7.3. Tétel (Az Eseményhorizont)**
A konyhában vagy a dohányzóban töltött idő ($t_{break}$) és az elvégzett munka ($W$) között fordított arányosság áll fenn, de kívülről nézve az ágens *foglaltnak* tűnik.

---

**7.4. Állítás (A Meetingek Termodinamikája)**
Egy értekezlet hasznossága ($U$) exponenciálisan csökken a résztvevők számával ($N$) és az elfogyasztott pogácsa mennyiségével ($P$):

$$U(N, P) = \frac{1}{e^{N}} \cdot \frac{1}{P + 1}$$

*Következmény:* Ha $N > 5$, az értekezlet entrópiája maximális, információcsere nem történik, csak a levegő melegítése (globális felmelegedéshez való hozzájárulás).



---

### 8. Hálózati Kommunikáció és Csomagvesztés

A felelősség továbbítása során a kommunikációs csatorna (pl. e-mail, Teams, „szóltam a Józsinak”) zajos.

**8.1. A Ping-Pong Protokoll**
Legyen $A$ és $B$ két entitás. A felelősségátvitel a következő kézfogással (handshake) történik:
1.  $A \to B$: `SYN` ("Te jössz.")
2.  $B \to A$: `SYN-ACK` ("Dehogy jövök, ez a te asztalod.")
3.  $A \to B$: `RST` ("Én ezt nem láttam, szabadságon voltam.")

---

**8.2. Adatvesztési Tétel (A "Spam-mappa" szingularitás)**  
Minden $m$ fontosságú üzenet esetén annak a valószínűsége, hogy a fogadó fél „nem kapta meg”, arányos a munka elvégzésének nehézségével:

$$
P(\text{nem láttam}) = 1 - e^{-(\lambda \ \cdot\  \mathrm{meló} \ \cdot\  M)}
$$

Ahol $\lambda$ a *lustasági állandó*, $M$ pedig a meló mennyisége.



---

### 9. Optimalizálás: A "Megoldjuk Okosba" Módszer

A klasszikus optimalizálási módszerek (pl. gradiens ereszkedés) helyett a magyar térben a *Lagrange-multiplikátorok* egy speciális esetét, az úgynevezett **Kenőpénz-multiplikátort** alkalmazzuk.

---

**9.1. Célfüggvény**
Minimalizálandó a $W$ (Work) energia, a következő kényszerfeltételek mellett:
*   $S$ (Salary) $\to \max$
*   $T$ (Time in office) $\to \min$

---

**9.2. A Megoldás**
A lokális optimum nem a globális minimumban található, hanem a rendszer határain kívül, az úgynevezett *Szürke Zónában*.
Matematikailag ez egy szinguláris pont, ahol a szabályok deriváltja nem értelmezhető:

$$\lim_{\text{ismerős} \to \infty} \text{Büntetés} = 0$$

---

### 10. Melléklet: Konstansok és Állandók

A számításokhoz szükséges empirikus állandók (Standard Hungarian Model):

*   **Péntek Délutáni Együttható ($k_{fri}$):** $0.05$ (Ekkor már senki nem vesz fel telefont).
*   **Neptun-állandó ($\tau_{down}$):** Az az időintervallum, amíg a rendszer éppen nem elérhető tárgyfelvételkor. $\tau_{down} \approx \infty$.
*   **MÁV-Késési Faktor ($\delta_{MÁV}$):** A téridő görbülete miatt a vonatok nem késnek, csak a mi időérzékelésünk torzul a várakozás során.

---

**Záró megjegyzés:**
*"A bizonyítások elegánsak, de a 'Majd holnap folytatjuk' lemma alkalmazása a 3. fejezetben nem teljesen rigorózus, bár kétségtelenül életszerű. Javaslom a cikk elfogadását :)"*

2025.12.28.
Németh Dávid