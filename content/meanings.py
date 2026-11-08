"""Meanings pages: symbols, flowers, superstitions, stones. Static articles."""
from sp import article_page


def _table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


# ---------------------------------------------------------------- 1. Yellow rose
def yellow_rose():
    en = """
<p>A yellow rose means friendship, joy and warm wishes. It is the rose you give to say "I'm glad you exist" without romantic overtones, which makes it the safest rose for a colleague, a neighbour, a friend recovering from an illness or someone you want to congratulate. The older Victorian reading (jealousy, a love that is fading) has almost disappeared from everyday use, but it still shows up in flower-language lists, so it is worth knowing.</p>

<h2>Where the meaning comes from</h2>
<p>Yellow roses are latecomers in Europe. Wild roses on the continent were pink, white or red; the first yellow species arrived from Persia and Central Asia in the eighteenth century, and they were famously scentless or even unpleasant-smelling. That poor reputation likely fed the Victorian habit of pairing yellow with suspicion, infidelity and jealousy. Nineteenth-century flower-language manuals, which assigned a message to almost every bloom, usually list the yellow rose under "decrease of love" or "jealousy".</p>
<p>The twentieth century rewrote the script. Breeders produced fragrant, sturdy yellow varieties, and florists in North America began promoting yellow as the colour of sunshine and friendship. By the 1950s the friendly meaning had taken over, and it is the one almost everyone recognises today.</p>

<h2>Shades and variations</h2>
<ul>
<li><strong>Pale or butter yellow</strong> reads as gentle and comforting; a good choice for get-well bouquets.</li>
<li><strong>Bright golden yellow</strong> is celebratory: new job, graduation, a birthday.</li>
<li><strong>Yellow with red tips</strong> is traditionally read as friendship turning into love, a useful middle ground when red feels too strong.</li>
<li><strong>Yellow and white together</strong> suggests a fresh start and is common at housewarmings.</li>
</ul>
<p>In Texas the yellow rose carries extra weight thanks to the folk song "The Yellow Rose of Texas", and in some Latin American countries yellow flowers in general are associated with remembrance of the dead, so check local custom before sending them abroad.</p>

<h2>When to give yellow roses</h2>
<p>Give them to a friend you have not seen in a while, to someone starting something new, to a host, or to a person going through a hard stretch who needs cheering rather than romance. Avoid them as the only flower on a first date or an anniversary unless the other person loves yellow: the friendship reading is strong enough that it can feel like a gentle "no". An odd number of stems is the florist's convention, and three or five yellow roses in a small vase look more intentional than a dozen.</p>

<h2>Common questions</h2>
<p><strong>Do yellow roses mean jealousy?</strong> Historically yes, in Victorian lists; in practice today, almost never. <strong>Can I give yellow roses to a man?</strong> Yes; they are among the most gender-neutral flowers. <strong>Yellow roses at a funeral?</strong> They are appropriate for a friend, where they say "I remember our friendship", and they are often chosen for celebrations of life.</p>

<p class="small">Sources: Victorian flower-language dictionaries, horticultural histories of rose breeding, and florist trade guides on colour symbolism.</p>
"""
    fr = """
<p>La rose jaune signifie l'amitié, la joie et les vœux chaleureux. C'est la rose que l'on offre pour dire « je suis content·e que tu existes » sans sous-entendu amoureux, ce qui en fait la plus sûre pour un collègue, une voisine, un ami en convalescence ou quelqu'un que l'on veut féliciter. La lecture victorienne plus ancienne (jalousie, amour qui s'éteint) a presque disparu de l'usage courant, mais elle figure encore dans les listes du langage des fleurs : autant la connaître.</p>

<h2>D'où vient cette signification</h2>
<p>Les roses jaunes sont arrivées tard en Europe. Les rosiers sauvages du continent étaient roses, blancs ou rouges ; les premières espèces jaunes sont venues de Perse et d'Asie centrale au XVIII<sup>e</sup> siècle, et elles étaient réputées sans parfum, voire malodorantes. Cette mauvaise réputation a sans doute nourri l'habitude victorienne d'associer le jaune au soupçon, à l'infidélité et à la jalousie. Les manuels du langage des fleurs du XIX<sup>e</sup> siècle, qui attribuaient un message à presque chaque fleur, classent généralement la rose jaune sous « déclin de l'amour » ou « jalousie ».</p>
<p>Le XX<sup>e</sup> siècle a réécrit l'histoire. Les obtenteurs ont créé des variétés jaunes parfumées et robustes, et les fleuristes d'Amérique du Nord ont fait du jaune la couleur du soleil et de l'amitié. Dès les années 1950, le sens amical l'avait emporté, et c'est celui que presque tout le monde reconnaît aujourd'hui.</p>

<h2>Nuances et variantes</h2>
<ul>
<li><strong>Jaune pâle ou beurre</strong> : doux et réconfortant ; un bon choix pour un bouquet de prompt rétablissement.</li>
<li><strong>Jaune doré vif</strong> : festif ; nouvel emploi, diplôme, anniversaire.</li>
<li><strong>Jaune à pointes rouges</strong> : traditionnellement, une amitié qui devient amour ; un juste milieu quand le rouge paraît trop direct.</li>
<li><strong>Jaune et blanc ensemble</strong> : un nouveau départ ; courant pour une pendaison de crémaillère.</li>
</ul>
<p>Au Texas, la rose jaune a un poids particulier grâce à la chanson populaire « The Yellow Rose of Texas », et dans certains pays d'Amérique latine les fleurs jaunes en général sont liées au souvenir des défunts : vérifiez la coutume locale avant d'en envoyer à l'étranger.</p>

<h2>Quand offrir des roses jaunes</h2>
<p>Offrez-les à un ami perdu de vue, à une personne qui commence quelque chose, à un hôte, ou à quelqu'un qui traverse une période difficile et a besoin de réconfort plutôt que de romance. Évitez-les comme seule fleur d'un premier rendez-vous ou d'un anniversaire de couple, sauf si l'autre adore le jaune : le sens amical est assez fort pour ressembler à un « non » poli. Un nombre impair de tiges est la convention des fleuristes, et trois ou cinq roses jaunes dans un petit vase paraissent plus intentionnelles qu'une douzaine.</p>

<h2>Questions fréquentes</h2>
<p><strong>La rose jaune signifie-t-elle la jalousie ?</strong> Historiquement oui, dans les listes victoriennes ; aujourd'hui, presque jamais. <strong>Peut-on offrir des roses jaunes à un homme ?</strong> Oui, c'est l'une des fleurs les plus neutres. <strong>Des roses jaunes à des funérailles ?</strong> Elles conviennent pour un ami, où elles disent « je me souviens de notre amitié », et on les choisit souvent pour les cérémonies d'hommage.</p>

<p class="small">Sources : dictionnaires victoriens du langage des fleurs, histoires horticoles de la création des rosiers, guides professionnels de fleuristes sur le symbolisme des couleurs.</p>
"""
    article_page("meanings",
        {"en": "yellow-rose-meaning", "fr": "signification-rose-jaune"},
        {"en": "Yellow rose meaning: friendship, joy and one old warning", "fr": "Signification de la rose jaune : amitié, joie et un vieux soupçon"},
        {"en": "What a yellow rose means today (friendship, joy), where the old jealousy reading came from, and when to give one.",
         "fr": "Ce que signifie la rose jaune aujourd'hui (amitié, joie), d'où vient l'ancien sens de jalousie, et quand l'offrir."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 2. Rose colours
def rose_colours():
    rows_en = [
        ("Red", "Love, desire, courage", "Anniversaries, Valentine's Day, declarations"),
        ("Pink", "Gratitude, admiration, gentleness", "Thank-yous, Mother's Day, new babies"),
        ("White", "Purity, new beginnings, remembrance", "Weddings, funerals, apologies"),
        ("Yellow", "Friendship, joy", "Friends, congratulations, get-well wishes"),
        ("Orange", "Enthusiasm, energy, fascination", "New ventures, encouragement, a bold crush"),
        ("Peach", "Sincerity, modesty, appreciation", "Closing a deal, thanking a mentor"),
        ("Lavender", "Enchantment, love at first sight", "Early romance, something unexpected"),
        ("Burgundy / dark red", "Deep, settled love; unconscious beauty", "Long marriages, mature relationships"),
    ]
    rows_fr = [
        ("Rouge", "Amour, désir, courage", "Anniversaires de couple, Saint-Valentin, déclarations"),
        ("Rose", "Gratitude, admiration, douceur", "Remerciements, fête des Mères, naissances"),
        ("Blanc", "Pureté, nouveau départ, souvenir", "Mariages, funérailles, excuses"),
        ("Jaune", "Amitié, joie", "Amis, félicitations, prompt rétablissement"),
        ("Orange", "Enthousiasme, énergie, fascination", "Nouveaux projets, encouragements, un coup de cœur audacieux"),
        ("Pêche", "Sincérité, modestie, reconnaissance", "Conclure une entente, remercier un mentor"),
        ("Lavande", "Enchantement, coup de foudre", "Début de romance, l'inattendu"),
        ("Bordeaux / rouge foncé", "Amour profond et installé ; beauté inconsciente", "Longs mariages, relations mûres"),
    ]
    en = f"""
<p>Red roses mean love, pink means gratitude, white means purity or remembrance, yellow means friendship, and orange means enthusiasm. Those five cover most bouquets. The table below adds peach, lavender and dark red, and tells you the occasion each colour fits best, so you can choose quickly and avoid the two classic mistakes: yellow for a lover, red for a boss.</p>

<h2>The eight colours at a glance</h2>
{_table(["Colour", "Meaning", "Good for"], rows_en)}

<h2>Where these meanings come from</h2>
<p>Most of what we "know" about rose colours is a nineteenth-century invention. Victorian Britain and France were fond of floriography, a coded language in which each flower and colour carried a message that could be sent when words were improper. Dozens of dictionaries were published, and they did not always agree with each other; the red rose for love and the white rose for innocence are the most stable entries, while orange and lavender roses barely existed yet and acquired their meanings later, mostly through florists in the twentieth century. Some associations are much older: red roses were linked to Aphrodite and Venus in Greek and Roman writing, and the white rose became a Marian symbol in medieval Christianity.</p>

<h2>Combinations and numbers</h2>
<ul>
<li><strong>Red and white together</strong> traditionally mean unity, which is why they are popular at weddings.</li>
<li><strong>Yellow with red tips</strong> signals friendship warming into love.</li>
<li><strong>A single rose</strong> says "you are the one"; <strong>a dozen</strong> is the classic declaration; <strong>two dozen</strong> says "I think of you every hour".</li>
<li><strong>Blue and black roses</strong> do not exist in nature; they are dyed or very dark red. Blue is read as mystery or the unattainable, black as farewell or rebirth, depending on who you ask.</li>
</ul>

<h2>Common questions</h2>
<p><strong>Which colour for a first date?</strong> Pink or peach: warm without pressure. <strong>For a sympathy bouquet?</strong> White, sometimes pale pink; yellow if the person was a close friend. <strong>For a colleague?</strong> Yellow, peach or orange; never red alone. <strong>Does the number of roses really matter?</strong> Only as much as you want it to; the colour sends the louder signal.</p>

<p class="small">Sources: Victorian and Edwardian flower-language dictionaries, classical and medieval references to the rose, and modern florist trade guides.</p>
"""
    fr = f"""
<p>Les roses rouges signifient l'amour, les roses roses la gratitude, les blanches la pureté ou le souvenir, les jaunes l'amitié et les orange l'enthousiasme. Ces cinq couleurs couvrent la plupart des bouquets. Le tableau ci-dessous ajoute la pêche, la lavande et le rouge foncé, et indique l'occasion qui convient à chacune, pour choisir vite et éviter les deux erreurs classiques : du jaune pour un amoureux, du rouge pour un patron.</p>

<h2>Les huit couleurs en un coup d'œil</h2>
{_table(["Couleur", "Signification", "Convient pour"], rows_fr)}

<h2>D'où viennent ces significations</h2>
<p>L'essentiel de ce que l'on « sait » des couleurs de roses est une invention du XIX<sup>e</sup> siècle. L'Angleterre et la France victoriennes raffolaient du langage des fleurs, un code où chaque fleur et chaque couleur portait un message qu'on pouvait envoyer quand les mots étaient déplacés. Des dizaines de dictionnaires ont paru, et ils ne s'accordaient pas toujours ; la rose rouge pour l'amour et la rose blanche pour l'innocence sont les entrées les plus stables, tandis que les roses orange et lavande existaient à peine et ont reçu leur sens plus tard, surtout par les fleuristes du XX<sup>e</sup> siècle. Certaines associations sont bien plus anciennes : la rose rouge était liée à Aphrodite et à Vénus chez les auteurs grecs et romains, et la rose blanche est devenue un symbole marial dans la chrétienté médiévale.</p>

<h2>Combinaisons et nombres</h2>
<ul>
<li><strong>Rouge et blanc ensemble</strong> : l'union, d'où leur popularité aux mariages.</li>
<li><strong>Jaune à pointes rouges</strong> : une amitié qui se réchauffe en amour.</li>
<li><strong>Une seule rose</strong> dit « c'est toi » ; <strong>une douzaine</strong> est la déclaration classique ; <strong>deux douzaines</strong> disent « je pense à toi à chaque heure ».</li>
<li><strong>Les roses bleues et noires</strong> n'existent pas dans la nature ; elles sont teintes ou d'un rouge très sombre. Le bleu se lit comme le mystère ou l'inaccessible, le noir comme l'adieu ou la renaissance, selon la source.</li>
</ul>

<h2>Questions fréquentes</h2>
<p><strong>Quelle couleur pour un premier rendez-vous ?</strong> Rose ou pêche : chaleureux sans pression. <strong>Pour un bouquet de condoléances ?</strong> Blanc, parfois rose pâle ; jaune si la personne était un ami proche. <strong>Pour un collègue ?</strong> Jaune, pêche ou orange ; jamais du rouge seul. <strong>Le nombre de roses compte-t-il vraiment ?</strong> Autant que vous le voulez ; la couleur envoie le signal le plus fort.</p>

<p class="small">Sources : dictionnaires du langage des fleurs de l'époque victorienne et édouardienne, références antiques et médiévales à la rose, guides professionnels de fleuristes.</p>
"""
    article_page("meanings",
        {"en": "rose-colours-meanings", "fr": "signification-couleurs-roses"},
        {"en": "Rose colours and their meanings: 8 colours explained", "fr": "Signification des couleurs de roses : 8 couleurs expliquées"},
        {"en": "Red, pink, white, yellow, orange, peach, lavender and dark red roses: what each colour means and which occasion it fits.",
         "fr": "Rouge, rose, blanc, jaune, orange, pêche, lavande, rouge foncé : ce que chaque couleur de rose signifie et pour quelle occasion."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 3. Teeth falling out dream
def teeth_dream():
    en = """
<p>Dreaming that your teeth fall out is one of the most common dreams in the world, and the usual interpretation is anxiety: about losing control, about how you look, about saying the wrong thing, or about a change you did not choose. Folk traditions add darker readings (a death in the family, bad news from afar), while psychologists tend to see a stress dream, sometimes with a very physical cause: clenching or grinding your teeth in your sleep. None of these is "the" answer, but together they explain why so many people wake up checking their mouth.</p>

<h2>What the dream usually looks like</h2>
<p>People describe the same handful of scenes: a tooth wobbles and comes out in the hand; teeth crumble like chalk; they fall out one after another while you try to hold them in; you are talking to someone and feel them loosen. Dream surveys across several countries place teeth dreams among the top ten recurring themes, alongside falling, being chased and being unprepared for an exam. The dream is reported at every age and by people with perfectly healthy teeth.</p>

<h2>Folk and traditional interpretations</h2>
<ul>
<li><strong>Loss or death:</strong> in many European and Middle Eastern traditions, a falling tooth announced the death of a relative; a painless loss was sometimes said to mean an older person, a painful one a younger relative. In Islamic dream-interpretation manuals, teeth stand for members of the household, and losing one can mean illness, debt or separation.</li>
<li><strong>Money:</strong> some Chinese and Western folk readings link teeth to wealth and read the dream as financial loss, or, more cheerfully, as debts about to be paid.</li>
<li><strong>Lies and speech:</strong> a tradition found in both European and Chinese sources holds that losing teeth means you have been speaking carelessly or that someone is lying to you.</li>
<li><strong>Growth:</strong> a gentler reading, common in modern dream dictionaries, treats the dream like a child losing milk teeth: something old is making room for something new.</li>
</ul>

<h2>The psychological view</h2>
<p>Freud read teeth dreams as sexual anxiety; few people follow him there today. Modern dream researchers point to two more grounded explanations. First, the dream tends to cluster around periods of stress, transitions and worries about appearance, speech or ageing, so it may simply dramatise a feeling of losing one's grip. Second, a study of dreamers found that teeth dreams were associated with dental irritation on waking (tension in the jaw, sensitive gums), which suggests the sleeping brain sometimes weaves a real sensation into a story. Both explanations can be true at once, and neither means anything is wrong with you.</p>

<h2>What to do with it</h2>
<p>Note what was happening in your life the week you had the dream; if it recurs, a pattern usually appears. If you also wake with a tight jaw, headaches or worn teeth, mention it to a dentist, since night-time grinding is common and easy to manage. Otherwise, treat the dream as a signal to look at what feels out of control, not as a prediction.</p>

<p class="small">Sources: folklore and dream-interpretation collections from Europe, the Middle East and China, dream-content surveys, and peer-reviewed sleep and dream research.</p>
"""
    fr = """
<p>Rêver que ses dents tombent est l'un des rêves les plus répandus au monde, et l'interprétation habituelle est l'anxiété : peur de perdre le contrôle, de son apparence, de dire ce qu'il ne faut pas, ou d'un changement qu'on n'a pas choisi. Les traditions populaires ajoutent des lectures plus sombres (un décès dans la famille, une mauvaise nouvelle venue de loin), tandis que les psychologues y voient plutôt un rêve de stress, parfois avec une cause très physique : serrer ou grincer des dents en dormant. Aucune de ces réponses n'est « la » bonne, mais ensemble elles expliquent pourquoi tant de gens se réveillent en se tâtant la bouche.</p>

<h2>À quoi ressemble ce rêve</h2>
<p>Les récits reprennent toujours les mêmes scènes : une dent bouge et tombe dans la main ; les dents s'effritent comme de la craie ; elles tombent l'une après l'autre pendant qu'on essaie de les retenir ; on parle à quelqu'un et on les sent se déchausser. Les enquêtes sur le contenu des rêves menées dans plusieurs pays placent les dents parmi les dix thèmes récurrents les plus fréquents, aux côtés de la chute, de la poursuite et de l'examen pour lequel on n'est pas préparé. Le rêve se rencontre à tout âge et chez des personnes aux dents parfaitement saines.</p>

<h2>Interprétations populaires et traditionnelles</h2>
<ul>
<li><strong>Perte ou deuil :</strong> dans beaucoup de traditions européennes et du Moyen-Orient, une dent qui tombe annonçait la mort d'un proche ; une perte sans douleur désignait parfois une personne âgée, une perte douloureuse un parent plus jeune. Dans les manuels d'interprétation des rêves de tradition islamique, les dents représentent les membres de la maisonnée, et en perdre une peut signifier maladie, dette ou séparation.</li>
<li><strong>Argent :</strong> certaines lectures populaires chinoises et occidentales lient les dents à la richesse et voient dans le rêve une perte financière ou, plus gaiement, des dettes bientôt remboursées.</li>
<li><strong>Mensonge et parole :</strong> une tradition présente dans des sources européennes comme chinoises veut que perdre ses dents signale qu'on a parlé à la légère, ou que quelqu'un vous ment.</li>
<li><strong>Croissance :</strong> une lecture plus douce, fréquente dans les dictionnaires de rêves modernes, compare le rêve à l'enfant qui perd ses dents de lait : quelque chose d'ancien laisse place à du neuf.</li>
</ul>

<h2>Le point de vue psychologique</h2>
<p>Freud lisait les rêves de dents comme une angoisse sexuelle ; peu de gens le suivent encore là. Les chercheurs actuels avancent deux explications plus terre à terre. D'abord, le rêve tend à se concentrer dans les périodes de stress, de transition et d'inquiétude sur l'apparence, la parole ou le vieillissement ; il mettrait simplement en scène le sentiment de perdre prise. Ensuite, une étude auprès de rêveurs a relevé un lien entre les rêves de dents et une irritation dentaire au réveil (tension de la mâchoire, gencives sensibles), ce qui suggère que le cerveau endormi tisse parfois une sensation réelle dans une histoire. Les deux explications peuvent être vraies à la fois, et aucune ne signifie que quelque chose cloche chez vous.</p>

<h2>Qu'en faire</h2>
<p>Notez ce qui se passait dans votre vie la semaine du rêve ; s'il revient, un motif finit souvent par apparaître. Si vous vous réveillez aussi avec la mâchoire serrée, des maux de tête ou des dents usées, parlez-en à un dentiste : le grincement nocturne est fréquent et facile à prendre en charge. Sinon, voyez le rêve comme un signal pour regarder ce qui vous échappe, pas comme une prédiction.</p>

<p class="small">Sources : recueils de folklore et d'interprétation des rêves d'Europe, du Moyen-Orient et de Chine, enquêtes sur le contenu des rêves, recherches évaluées par les pairs sur le sommeil et les rêves.</p>
"""
    article_page("meanings",
        {"en": "dream-teeth-falling-out-meaning", "fr": "rever-dents-qui-tombent-signification"},
        {"en": "Dreaming of teeth falling out: what it means", "fr": "Rêver que ses dents tombent : signification"},
        {"en": "Why so many people dream their teeth fall out: folk interpretations, the psychological view, and what to do about it.",
         "fr": "Pourquoi tant de gens rêvent que leurs dents tombent : lectures populaires, point de vue psychologique et quoi en faire."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 4. 11:11
def eleven_eleven():
    en = """
<p>Seeing 11:11 is widely taken as a sign to make a wish, and in New Age and "angel number" circles it is read as a message that you are on the right path, waking up spiritually, or about to meet someone important. There is no scientific evidence that the time carries a message, but there is a good explanation for why you keep noticing it, and the habit of pausing when it appears is harmless and, for many people, genuinely pleasant.</p>

<h2>Where the 11:11 tradition comes from</h2>
<p>Making a wish at 11:11 seems to be a twentieth-century schoolyard custom, first noted in English-speaking countries and spread by word of mouth, then by digital clocks, which made four identical digits far more visible than analogue hands ever did. The spiritual layer was added in the late 1980s and 1990s by New Age writers who described 11:11 as a "wake-up code" and a doorway to higher awareness. The idea travelled quickly through the early internet and later through social media, where "angel numbers" (repeating sequences such as 111, 222, 444) became a whole genre of interpretation.</p>

<h2>The main readings</h2>
<ul>
<li><strong>Make a wish:</strong> the oldest and simplest. Some versions say you must not tell anyone, or that it only works if you noticed the time by chance.</li>
<li><strong>Alignment:</strong> in numerology, 1 stands for beginnings and willpower; four of them are read as a strong push to start something or trust an intuition.</li>
<li><strong>A loved one is thinking of you:</strong> a common folk reading, especially of someone far away or deceased.</li>
<li><strong>Twin flame:</strong> in some spiritual communities 11:11 is said to announce a profound connection with another person.</li>
<li><strong>Remembrance:</strong> in the United Kingdom, Canada, France and elsewhere, 11 November at 11 a.m. marks the 1918 armistice and is observed with a silence. It has nothing to do with wishes, but the overlap is why 11:11 feels so weighty in November.</li>
</ul>

<h2>Why you keep seeing it</h2>
<p>Two well-documented habits of the mind are at work. The first is selective attention: once 11:11 has meaning for you, you notice it and forget the hundreds of times you glanced at 11:09 or 2:37. The second is the frequency illusion, the sense that something you just learned about is suddenly everywhere. Add the fact that 11:11 appears twice a day on a 12-hour clock (once on a 24-hour one) and that mid-morning is a moment when many people check their phones, and the "coincidence" becomes expected. This does not make the moment meaningless; it just moves the meaning from the clock to you.</p>

<h2>What to do when you see it</h2>
<p>Use it as a pause. Many people make a wish, name one thing they are grateful for, or ask themselves one honest question about the day. If the time appears while you are agonising over a decision, treat it as a nudge to decide rather than as the decision itself. And if 11:11 reminds you of a particular person, sending them a message is a perfectly good use of the signal.</p>

<p class="small">Sources: folklore collections on wishing customs, New Age and numerology literature from the 1990s onward, and introductory cognitive-psychology texts on attention and the frequency illusion.</p>
"""
    fr = """
<p>Voir 11h11 est largement perçu comme le signal de faire un vœu, et dans les milieux New Age et des « nombres angéliques », on y lit un message : vous êtes sur la bonne voie, vous vous éveillez spirituellement, ou vous allez rencontrer quelqu'un d'important. Aucune preuve scientifique ne montre que l'heure porte un message, mais il existe une bonne explication au fait que vous la remarquiez sans cesse, et l'habitude de s'arrêter un instant quand elle apparaît est sans danger et, pour beaucoup, réellement agréable.</p>

<h2>D'où vient la tradition du 11h11</h2>
<p>Faire un vœu à 11h11 semble être une coutume de cour d'école du XX<sup>e</sup> siècle, d'abord relevée dans les pays anglophones et transmise de bouche à oreille, puis par les horloges numériques, qui ont rendu quatre chiffres identiques bien plus visibles que ne l'ont jamais été des aiguilles. La couche spirituelle a été ajoutée à la fin des années 1980 et dans les années 1990 par des auteurs New Age qui décrivaient 11h11 comme un « code d'éveil » et une porte vers une conscience supérieure. L'idée a voyagé vite sur les débuts d'Internet, puis sur les réseaux sociaux, où les « nombres angéliques » (suites répétées comme 111, 222, 444) sont devenus tout un genre d'interprétation.</p>

<h2>Les principales lectures</h2>
<ul>
<li><strong>Faire un vœu :</strong> la plus ancienne et la plus simple. Certaines versions exigent de ne le dire à personne, ou précisent que cela ne marche que si l'on a vu l'heure par hasard.</li>
<li><strong>Alignement :</strong> en numérologie, le 1 représente le commencement et la volonté ; quatre 1 se lisent comme une forte incitation à démarrer quelque chose ou à suivre une intuition.</li>
<li><strong>Quelqu'un pense à vous :</strong> une lecture populaire courante, surtout pour une personne éloignée ou disparue.</li>
<li><strong>Flamme jumelle :</strong> dans certaines communautés spirituelles, 11h11 annoncerait une connexion profonde avec une autre personne.</li>
<li><strong>Mémoire :</strong> au Royaume-Uni, au Canada, en France et ailleurs, le 11 novembre à 11 heures marque l'armistice de 1918 et s'accompagne d'une minute de silence. Rien à voir avec les vœux, mais ce recoupement explique pourquoi 11h11 paraît si chargé en novembre.</li>
</ul>

<h2>Pourquoi vous le voyez tout le temps</h2>
<p>Deux habitudes bien documentées de l'esprit sont à l'œuvre. La première est l'attention sélective : dès que 11h11 a un sens pour vous, vous le remarquez et oubliez les centaines de fois où vous avez regardé 11h09 ou 14h37. La seconde est l'illusion de fréquence, l'impression qu'une chose qu'on vient d'apprendre est soudain partout. Ajoutez que 11h11 apparaît deux fois par jour sur une horloge à 12 heures (une fois sur une horloge à 24 heures) et que la fin de matinée est un moment où beaucoup consultent leur téléphone : la « coïncidence » devient attendue. Cela ne vide pas le moment de sens ; cela déplace simplement le sens de l'horloge vers vous.</p>

<h2>Que faire quand vous le voyez</h2>
<p>Servez-vous-en comme d'une pause. Beaucoup font un vœu, nomment une chose dont ils sont reconnaissants, ou se posent une question honnête sur leur journée. Si l'heure surgit pendant que vous hésitez sur une décision, prenez-la comme une invitation à trancher, pas comme la décision elle-même. Et si 11h11 vous rappelle une personne en particulier, lui envoyer un message est un excellent usage du signal.</p>

<p class="small">Sources : recueils de folklore sur les coutumes de vœux, littérature New Age et numérologique à partir des années 1990, manuels d'introduction à la psychologie cognitive sur l'attention et l'illusion de fréquence.</p>
"""
    article_page("meanings",
        {"en": "11-11-meaning", "fr": "signification-11h11"},
        {"en": "11:11 meaning: wishes, angel numbers and why you keep seeing it", "fr": "Signification de 11h11 : vœux, nombres angéliques et pourquoi vous le voyez partout"},
        {"en": "What 11:11 means in folklore, numerology and New Age thought, where the wish custom came from, and why you notice it so often.",
         "fr": "Ce que 11h11 signifie en folklore, en numérologie et dans la pensée New Age, l'origine du vœu, et pourquoi on le remarque si souvent."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 5. Black cat
def black_cat():
    en = """
<p>A black cat is bad luck in much of the United States, Spain, Italy and parts of continental Europe, and good luck in Britain, Ireland, Scotland, Japan and among sailors' families almost everywhere. The same animal, the same colour, opposite verdicts: the black cat is the clearest example of how superstitions are local habits rather than universal truths. If one crosses your path today, the honest answer is that it means a cat was going somewhere.</p>

<h2>How the black cat became unlucky</h2>
<p>Cats were revered in ancient Egypt, and nothing in Greek or Roman writing singles out black ones. The turn came in medieval Europe. From the thirteenth century, church writers associated cats with heresy and night-time rituals, and by the sixteenth and seventeenth centuries the black cat had become the standard "familiar" of the accused witch in English, Scottish and continental trial records. Folk belief followed: a black cat was a witch in disguise, or a demon's messenger, and meeting one meant misfortune was near. Puritan settlers carried the fear to New England, which is why the American version is so strong, and why black cats still decorate Halloween.</p>

<h2>Where black cats are lucky</h2>
<ul>
<li><strong>England, Scotland and Ireland:</strong> a black cat crossing your path or arriving at your door brings good fortune; a black cat given to a bride was a traditional wedding gift in parts of England.</li>
<li><strong>Japan:</strong> black cats ward off evil and are thought to help single women attract suitors; the beckoning <em>maneki-neko</em> figurine exists in a black version for protection.</li>
<li><strong>Sailors and fishing towns</strong> in Britain, Ireland and elsewhere kept black cats aboard or at home to ensure a safe return; fishermen's wives were said to keep one for exactly this reason.</li>
<li><strong>Parts of France and Germany</strong> hold mixed views: a cat crossing from left to right is lucky, from right to left unlucky, or the other way round depending on the region.</li>
<li><strong>Russia and much of Eastern Europe</strong> are mixed as well, though black cats are often seen as household protectors.</li>
</ul>

<h2>Variations on the superstition</h2>
<p>Many versions attach the luck to direction: a cat walking toward you brings fortune, walking away takes it. Others say a black cat that comes to live with you brings prosperity, while one that merely passes brings nothing. In Italy, the fear is strong enough that a national "black cat day" was created to counter it. Shelter workers in several countries report that black cats take longer to be adopted, partly because of the superstition and partly, more prosaically, because they photograph poorly.</p>

<h2>Common questions</h2>
<p><strong>What should I do if a black cat crosses my path?</strong> Nothing; or, if you enjoy rituals, the old English advice is to greet it politely. <strong>Is it bad luck to own one?</strong> In every lucky-cat country it is the opposite, and most cat owners would say the same anywhere. <strong>Why are black cats linked to Halloween?</strong> Through the witch-trial imagery and the Victorian fashion for Gothic decoration, not through any older Celtic belief.</p>

<p class="small">Sources: European witch-trial records and histories, folklore collections from Britain, Ireland, Japan and the United States, and animal-shelter reports on adoption patterns.</p>
"""
    fr = """
<p>Le chat noir porte malheur dans une grande partie des États-Unis, en Espagne, en Italie et dans plusieurs régions d'Europe continentale, et il porte bonheur en Angleterre, en Écosse, en Irlande, au Japon et dans les familles de marins presque partout. Même animal, même couleur, verdicts opposés : le chat noir est l'exemple le plus net de ce qu'une superstition est une habitude locale et non une vérité universelle. Si l'un d'eux croise votre chemin aujourd'hui, la réponse honnête est qu'un chat allait quelque part.</p>

<h2>Comment le chat noir est devenu maléfique</h2>
<p>Les chats étaient vénérés dans l'Égypte ancienne, et rien dans les textes grecs ou romains ne distingue les noirs. Le tournant se produit dans l'Europe médiévale. À partir du XIII<sup>e</sup> siècle, des auteurs d'Église associent les chats à l'hérésie et aux rituels nocturnes, et aux XVI<sup>e</sup> et XVII<sup>e</sup> siècles le chat noir est devenu le « familier » type de la sorcière accusée dans les procès anglais, écossais et continentaux. La croyance populaire a suivi : un chat noir était une sorcière déguisée ou le messager d'un démon, et le croiser annonçait un malheur proche. Les colons puritains ont emporté cette peur en Nouvelle-Angleterre, ce qui explique la force de la version américaine et la présence des chats noirs dans les décors d'Halloween.</p>

<h2>Où le chat noir porte bonheur</h2>
<ul>
<li><strong>Angleterre, Écosse et Irlande :</strong> un chat noir qui croise votre chemin ou se présente à votre porte apporte la chance ; offrir un chat noir à une mariée était un cadeau de mariage traditionnel dans certaines régions d'Angleterre.</li>
<li><strong>Japon :</strong> les chats noirs éloignent le mal et aideraient les femmes célibataires à attirer des prétendants ; le <em>maneki-neko</em>, le chat qui salue de la patte, existe en version noire pour la protection.</li>
<li><strong>Marins et villages de pêcheurs</strong> de Grande-Bretagne, d'Irlande et d'ailleurs gardaient un chat noir à bord ou à la maison pour assurer un retour sans encombre ; les femmes de pêcheurs en gardaient un précisément pour cela.</li>
<li><strong>Certaines régions de France et d'Allemagne</strong> sont partagées : un chat qui traverse de gauche à droite porte chance, de droite à gauche malchance, ou l'inverse selon la région.</li>
<li><strong>Russie et une grande partie de l'Europe de l'Est</strong> sont également partagées, mais le chat noir y est souvent vu comme un protecteur du foyer.</li>
</ul>

<h2>Variantes de la superstition</h2>
<p>Bien des versions lient la chance à la direction : un chat qui vient vers vous apporte la fortune, un chat qui s'éloigne l'emporte. D'autres disent qu'un chat noir qui vient vivre chez vous apporte la prospérité, tandis que celui qui passe simplement n'apporte rien. En Italie, la peur est assez forte pour qu'une « journée nationale du chat noir » ait été créée pour la combattre. Les refuges de plusieurs pays rapportent que les chats noirs mettent plus de temps à être adoptés, en partie à cause de la superstition et en partie, plus prosaïquement, parce qu'ils sont difficiles à photographier.</p>

<h2>Questions fréquentes</h2>
<p><strong>Que faire si un chat noir croise mon chemin ?</strong> Rien ; ou, si vous aimez les rituels, le vieux conseil anglais est de le saluer poliment. <strong>Est-ce que c'est malchanceux d'en posséder un ?</strong> Dans tous les pays du chat porte-bonheur, c'est l'inverse, et la plupart des propriétaires de chats diraient la même chose partout. <strong>Pourquoi le chat noir est-il lié à Halloween ?</strong> Par l'imagerie des procès de sorcellerie et la mode victorienne du décor gothique, pas par une croyance celtique plus ancienne.</p>

<p class="small">Sources : archives et histoires des procès de sorcellerie en Europe, recueils de folklore de Grande-Bretagne, d'Irlande, du Japon et des États-Unis, rapports de refuges sur les adoptions.</p>
"""
    article_page("meanings",
        {"en": "black-cat-superstition-meaning", "fr": "chat-noir-superstition-signification"},
        {"en": "Black cat: superstition and meaning around the world", "fr": "Chat noir : superstition et signification dans le monde"},
        {"en": "Why black cats are unlucky in some countries and lucky in Britain, Japan and among sailors, with the history behind the superstition.",
         "fr": "Pourquoi le chat noir porte malheur ici et bonheur en Angleterre, au Japon et chez les marins, avec l'histoire de la superstition."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 6. Four-leaf clover
def four_leaf_clover():
    en = """
<p>A four-leaf clover means luck, and by tradition each leaf stands for something: faith, hope, love and, for the fourth, luck itself. Its rarity is the whole point: the commonly cited figure is about 1 in 5,000 clovers, though actual odds vary a lot from patch to patch, because the extra leaf is partly genetic and some lawns produce them far more often than others.</p>

<h2>Origins of the belief</h2>
<p>Clover grows across Europe, and the idea that an unusual plant protects its finder is very old. Irish tradition gives the three-leaf shamrock to Saint Patrick, who is said to have used it to explain the Trinity, and the four-leaf version naturally became the shamrock's lucky cousin. English and Irish folklore from the seventeenth century onward describes four-leaf clovers as charms that let you see fairies, detect witches and protect against evil spells. Victorian sentiment turned the charm into a keepsake pressed in books and sent in letters, and twentieth-century advertising did the rest: the four-leaf clover became a universal logo for good fortune.</p>

<h2>What the leaves mean</h2>
<ul>
<li><strong>First leaf:</strong> faith.</li>
<li><strong>Second leaf:</strong> hope.</li>
<li><strong>Third leaf:</strong> love.</li>
<li><strong>Fourth leaf:</strong> luck.</li>
</ul>
<p>Five-leaf clovers exist and are rarer still; folk tradition promises money or an especially strong charm, and some versions say they bring bad luck instead, which tells you how improvised these rules are. Clovers with six or more leaves have been recorded, and a Japanese grower holds a record for a plant with dozens of leaflets, all bred deliberately.</p>

<h2>How rare is it, really?</h2>
<p>The 1-in-5,000 figure is repeated everywhere, but it comes from informal counts rather than a formal survey, and surveys by enthusiasts have found rates closer to 1 in 1,000 in some fields and far lower in others. The fourth leaf appears to be caused by a recessive gene in white clover (<em>Trifolium repens</em>), made more or less likely by growing conditions such as temperature and soil. That is why one patch can yield several in a single afternoon while the lawn next door produces none. Practical tip: scan a clover patch slowly without focusing on individual plants; the extra leaf breaks the visual pattern and tends to jump out.</p>

<h2>What to do with one</h2>
<p>Press it between paper towels inside a heavy book for a week or two, then laminate it or slip it into a locket, phone case or wallet. Giving one away is traditionally said to double the luck, which makes it an unusually good gift for an exam, a first day at a new job or a departure. And if you simply want one, cultivated four-leaf clovers are sold as live plants and seeds; the folklore insists that only a found clover counts, but the plant will not know the difference.</p>

<p class="small">Sources: Irish and English folklore collections, botanical references on <em>Trifolium repens</em>, and published counts by clover-collecting enthusiasts.</p>
"""
    fr = """
<p>Le trèfle à quatre feuilles signifie la chance, et par tradition chaque feuille représente quelque chose : la foi, l'espérance, l'amour et, pour la quatrième, la chance elle-même. Sa rareté fait tout son intérêt : le chiffre couramment cité est d'environ 1 trèfle sur 5 000, mais les vraies probabilités varient beaucoup d'un carré d'herbe à l'autre, parce que la feuille supplémentaire est en partie génétique et que certaines pelouses en produisent bien plus que d'autres.</p>

<h2>Origines de la croyance</h2>
<p>Le trèfle pousse dans toute l'Europe, et l'idée qu'une plante inhabituelle protège celui qui la trouve est très ancienne. La tradition irlandaise attribue le trèfle à trois feuilles, le <em>shamrock</em>, à saint Patrick, qui s'en serait servi pour expliquer la Trinité ; la version à quatre feuilles est naturellement devenue son cousin porte-bonheur. Le folklore anglais et irlandais décrit, à partir du XVII<sup>e</sup> siècle, des trèfles à quatre feuilles comme des talismans qui permettent de voir les fées, de repérer les sorcières et de se protéger des mauvais sorts. La sensibilité victorienne a fait du talisman un souvenir pressé dans les livres et glissé dans les lettres, et la publicité du XX<sup>e</sup> siècle a terminé le travail : le trèfle à quatre feuilles est devenu un logo universel de la bonne fortune.</p>

<h2>Ce que signifient les feuilles</h2>
<ul>
<li><strong>Première feuille :</strong> la foi.</li>
<li><strong>Deuxième feuille :</strong> l'espérance.</li>
<li><strong>Troisième feuille :</strong> l'amour.</li>
<li><strong>Quatrième feuille :</strong> la chance.</li>
</ul>
<p>Les trèfles à cinq feuilles existent et sont encore plus rares ; la tradition promet de l'argent ou un charme particulièrement puissant, et certaines versions disent au contraire qu'ils portent malheur, ce qui montre à quel point ces règles sont improvisées. Des trèfles à six feuilles et plus ont été recensés, et un cultivateur japonais détient un record pour une plante à plusieurs dizaines de folioles, toutes obtenues par sélection.</p>

<h2>Quelle rareté, au fond ?</h2>
<p>Le chiffre de 1 sur 5 000 est repris partout, mais il vient de comptages informels plutôt que d'une étude en règle, et les relevés d'amateurs ont trouvé des taux proches de 1 sur 1 000 dans certains champs et bien plus faibles ailleurs. La quatrième feuille semble due à un gène récessif du trèfle blanc (<em>Trifolium repens</em>), rendu plus ou moins probable par les conditions de culture comme la température et le sol. C'est pourquoi un carré peut en donner plusieurs en un après-midi quand la pelouse voisine n'en produit aucun. Conseil pratique : balayez lentement le regard sur un tapis de trèfles sans fixer chaque plante ; la feuille en trop casse le motif visuel et saute aux yeux.</p>

<h2>Qu'en faire</h2>
<p>Pressez-le entre deux feuilles de papier absorbant dans un livre lourd pendant une à deux semaines, puis plastifiez-le ou glissez-le dans un médaillon, une coque de téléphone ou un portefeuille. Le donner doublerait la chance, dit la tradition, ce qui en fait un cadeau idéal pour un examen, un premier jour de travail ou un départ. Et si vous en voulez simplement un, des trèfles à quatre feuilles cultivés se vendent en plantes et en graines ; le folklore insiste sur le fait que seul un trèfle trouvé compte, mais la plante ne verra pas la différence.</p>

<p class="small">Sources : recueils de folklore irlandais et anglais, références botaniques sur <em>Trifolium repens</em>, comptages publiés par des collectionneurs de trèfles.</p>
"""
    article_page("meanings",
        {"en": "four-leaf-clover-meaning-odds", "fr": "signification-trefle-quatre-feuilles"},
        {"en": "Four-leaf clover: meaning, odds and what each leaf stands for", "fr": "Signification du trèfle à quatre feuilles : chance, rareté et sens des feuilles"},
        {"en": "What a four-leaf clover means, what each leaf stands for, the commonly cited 1-in-5,000 odds, and how to keep one.",
         "fr": "Ce que signifie le trèfle à quatre feuilles, le sens de chaque feuille, la rareté souvent citée de 1 sur 5 000, et comment le conserver."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 7. Birthstones
def birthstones():
    rows_en = [
        ("January", "Garnet", "Garnet", "Protection, friendship"),
        ("February", "Amethyst", "Amethyst", "Calm, clarity"),
        ("March", "Bloodstone", "Aquamarine", "Courage, serenity"),
        ("April", "Diamond", "Diamond", "Strength, lasting love"),
        ("May", "Emerald", "Emerald", "Rebirth, wisdom"),
        ("June", "Pearl, moonstone", "Alexandrite", "Purity, balance"),
        ("July", "Ruby", "Ruby", "Passion, vitality"),
        ("August", "Sardonyx", "Peridot, spinel", "Happiness, protection"),
        ("September", "Sapphire", "Sapphire", "Wisdom, loyalty"),
        ("October", "Opal", "Tourmaline", "Hope, creativity"),
        ("November", "Topaz", "Citrine", "Warmth, abundance"),
        ("December", "Turquoise, lapis lazuli", "Tanzanite, zircon, blue topaz", "Good fortune, success"),
    ]
    rows_fr = [
        ("Janvier", "Grenat", "Grenat", "Protection, amitié"),
        ("Février", "Améthyste", "Améthyste", "Calme, lucidité"),
        ("Mars", "Héliotrope (jaspe sanguin)", "Aigue-marine", "Courage, sérénité"),
        ("Avril", "Diamant", "Diamant", "Force, amour durable"),
        ("Mai", "Émeraude", "Émeraude", "Renaissance, sagesse"),
        ("Juin", "Perle, pierre de lune", "Alexandrite", "Pureté, équilibre"),
        ("Juillet", "Rubis", "Rubis", "Passion, vitalité"),
        ("Août", "Sardonyx", "Péridot, spinelle", "Bonheur, protection"),
        ("Septembre", "Saphir", "Saphir", "Sagesse, loyauté"),
        ("Octobre", "Opale", "Tourmaline", "Espoir, créativité"),
        ("Novembre", "Topaze", "Citrine", "Chaleur, abondance"),
        ("Décembre", "Turquoise, lapis-lazuli", "Tanzanite, zircon, topaze bleue", "Chance, réussite"),
    ]
    en = f"""
<p>Your birthstone depends on your month: garnet for January, amethyst for February, aquamarine for March, diamond for April, emerald for May, pearl or alexandrite for June, ruby for July, peridot for August, sapphire for September, opal or tourmaline for October, topaz or citrine for November, and turquoise, tanzanite or blue topaz for December. Several months have two lists, a traditional one and a modern one, and both are considered correct. The table shows them side by side.</p>

<h2>Birthstones by month</h2>
{_table(["Month", "Traditional", "Modern", "Said to bring"], rows_en)}

<h2>Where the list comes from</h2>
<p>The idea of twelve stones goes back to the breastplate of the high priest described in the Book of Exodus, which was set with twelve gems for the twelve tribes of Israel. Early Christian writers linked those stones to the twelve apostles and then to the twelve months, and by the Renaissance it was fashionable in parts of Europe to own all twelve and wear each in its month. Wearing only the stone of your birth month is a more recent habit, usually traced to eighteenth-century Poland and popularised in the nineteenth century.</p>
<p>The "modern" list was standardised in 1912 by the American National Association of Jewelers, partly to replace stones that were rare or fragile with ones easier to sell: aquamarine took over from bloodstone in March, and alexandrite joined pearl in June. Later additions include tanzanite for December (2002) and spinel for August (2016). British and other national lists differ slightly, so if your family's tradition names another stone, it is probably not wrong, just older or from elsewhere.</p>

<h2>Choosing and wearing a birthstone</h2>
<ul>
<li><strong>Durability matters.</strong> Diamond, sapphire and ruby handle daily wear; opal, pearl and turquoise scratch and lose water easily, so they suit earrings and pendants better than rings.</li>
<li><strong>Price varies enormously.</strong> Months with a modern alternative often have a far cheaper option: citrine instead of imperial topaz, blue topaz instead of tanzanite, spinel instead of a top ruby for July lookalikes.</li>
<li><strong>Treatments are normal.</strong> Most commercial citrine is heated amethyst, most blue topaz is irradiated, and many sapphires are heat-treated; a reputable jeweller will say so.</li>
</ul>

<h2>Common questions</h2>
<p><strong>Which list should I follow?</strong> Either; the modern list is what most jewellers mean by default. <strong>Do birthstones have powers?</strong> The qualities in the table are traditional associations, not demonstrated effects. <strong>Can I wear another month's stone?</strong> Of course; many people wear a child's or partner's birthstone.</p>

<p class="small">Sources: biblical and early Christian references to the twelve stones, nineteenth- and twentieth-century jewellers' trade lists, and gemmological handbooks on durability and treatments.</p>
"""
    fr = f"""
<p>Votre pierre de naissance dépend de votre mois : grenat pour janvier, améthyste pour février, aigue-marine pour mars, diamant pour avril, émeraude pour mai, perle ou alexandrite pour juin, rubis pour juillet, péridot pour août, saphir pour septembre, opale ou tourmaline pour octobre, topaze ou citrine pour novembre, et turquoise, tanzanite ou topaze bleue pour décembre. Plusieurs mois ont deux listes, une traditionnelle et une moderne, et les deux sont considérées comme justes. Le tableau les présente côte à côte.</p>

<h2>Les pierres de naissance mois par mois</h2>
{_table(["Mois", "Traditionnelle", "Moderne", "Apporterait"], rows_fr)}

<h2>D'où vient la liste</h2>
<p>L'idée de douze pierres remonte au pectoral du grand prêtre décrit dans le livre de l'Exode, orné de douze gemmes pour les douze tribus d'Israël. Les premiers auteurs chrétiens ont relié ces pierres aux douze apôtres, puis aux douze mois, et à la Renaissance il était à la mode, dans certaines régions d'Europe, de posséder les douze et de porter chacune pendant son mois. Ne porter que la pierre de son mois de naissance est une habitude plus récente, qu'on fait généralement remonter à la Pologne du XVIII<sup>e</sup> siècle et qui s'est répandue au XIX<sup>e</sup>.</p>
<p>La liste « moderne » a été normalisée en 1912 par l'association nationale des bijoutiers américains, en partie pour remplacer des pierres rares ou fragiles par d'autres plus faciles à vendre : l'aigue-marine a pris la place de l'héliotrope en mars, et l'alexandrite a rejoint la perle en juin. Parmi les ajouts plus tardifs : la tanzanite pour décembre (2002) et le spinelle pour août (2016). Les listes britannique et d'autres pays diffèrent légèrement ; si la tradition de votre famille nomme une autre pierre, elle n'est probablement pas fausse, seulement plus ancienne ou venue d'ailleurs.</p>

<h2>Choisir et porter sa pierre</h2>
<ul>
<li><strong>La solidité compte.</strong> Le diamant, le saphir et le rubis supportent le port quotidien ; l'opale, la perle et la turquoise se rayent et se déshydratent facilement, et conviennent mieux aux boucles d'oreilles et aux pendentifs qu'aux bagues.</li>
<li><strong>Les prix varient énormément.</strong> Les mois dotés d'une variante moderne offrent souvent une option bien moins chère : la citrine plutôt que la topaze impériale, la topaze bleue plutôt que la tanzanite, le spinelle plutôt qu'un rubis de haut de gamme pour un effet « juillet ».</li>
<li><strong>Les traitements sont la norme.</strong> La plupart des citrines du commerce sont des améthystes chauffées, la plupart des topazes bleues sont irradiées, et bien des saphirs sont chauffés ; un bijoutier sérieux le précisera.</li>
</ul>

<h2>Questions fréquentes</h2>
<p><strong>Quelle liste suivre ?</strong> L'une ou l'autre ; la liste moderne est celle que la plupart des bijoutiers utilisent par défaut. <strong>Les pierres ont-elles des pouvoirs ?</strong> Les qualités du tableau sont des associations traditionnelles, pas des effets démontrés. <strong>Puis-je porter la pierre d'un autre mois ?</strong> Bien sûr ; beaucoup portent celle d'un enfant ou d'un conjoint.</p>

<p class="small">Sources : références bibliques et paléochrétiennes aux douze pierres, listes professionnelles de bijoutiers des XIX<sup>e</sup> et XX<sup>e</sup> siècles, manuels de gemmologie sur la dureté et les traitements.</p>
"""
    article_page("meanings",
        {"en": "birthstones-by-month", "fr": "pierres-de-naissance-par-mois"},
        {"en": "Birthstones by month: traditional and modern list", "fr": "Pierres de naissance par mois : liste traditionnelle et moderne"},
        {"en": "The birthstone for each of the 12 months, traditional and modern, with what each is said to bring and where the list comes from.",
         "fr": "La pierre de naissance de chacun des 12 mois, traditionnelle et moderne, ce qu'on lui attribue et l'origine de la liste."},
        {"en": en, "fr": fr})


# ---------------------------------------------------------------- 8. Peony
def peony():
    en = """
<p>The peony means prosperity, honour, romance and a happy marriage. In China it is the "king of flowers" and a symbol of wealth and good fortune; in the Western flower language it stands for bashfulness and, more recently, for a long and happy union, which is why it is the flower of the twelfth wedding anniversary and a favourite at weddings. Its brief, lavish bloom in late spring also makes it a symbol of fleeting beauty.</p>

<h2>Origins: China, Japan and Europe</h2>
<p>Peonies have been cultivated in China for well over a thousand years, first as a medicinal root and then, from the Tang dynasty onward, as the flower of the imperial court. The tree peony (<em>mudan</em>) appears in poetry, painting and porcelain as a stand-in for rank, riches and feminine beauty, and the city of Luoyang still holds a peony festival each spring. The flower reached Japan around the eighth century, where it took on connotations of bravery and good fortune and became a common tattoo motif alongside lions and dragons.</p>
<p>Europe knew a native species, and the name comes from Paeon, physician of the gods in Greek myth, who was said to have been turned into the flower to save him from a jealous teacher. Medieval herbals valued peony root as a remedy, and the great garden varieties we grow today were bred in France in the nineteenth century, which is why so many bear French names.</p>

<h2>Colours and their shades of meaning</h2>
<ul>
<li><strong>Pink</strong> is the romantic peony: love, marriage, good luck in a relationship.</li>
<li><strong>White</strong> suggests modesty and is traditionally the "bashful" peony; it is also used to say sorry.</li>
<li><strong>Red</strong> carries the Chinese meaning most strongly: wealth, honour, respect.</li>
<li><strong>Coral and yellow</strong> are modern hybrids and read as cheerful and celebratory.</li>
</ul>
<p>The Victorian "bashfulness" meaning comes from a story in which nymphs hid in peony petals, and from the flower's habit of hiding its centre in a mass of petals.</p>

<h2>When to give peonies</h2>
<p>Weddings and the twelfth anniversary are the classic occasions. Peonies also suit a housewarming (prosperity for the new home), a promotion, or any occasion where you want something grander than roses but still soft. Because the season is short (roughly late April to June in the northern hemisphere), a bunch of peonies is a treat rather than a default, and people know it. Buy them in tight bud and they will open over several days; a sugar cube in the water is an old florist's trick that does no harm.</p>

<h2>Common questions</h2>
<p><strong>Are peonies lucky?</strong> In Chinese tradition, strongly so, especially for wealth and marriage. <strong>Is it bad luck to have them in the house?</strong> No; the one caution in old European folklore is against digging up a peony, which was said to anger the plant and bring misfortune, a story probably invented to protect slow-growing roots. <strong>Peony versus rose?</strong> Roses speak of love; peonies speak of a good life together.</p>

<p class="small">Sources: histories of Chinese and Japanese garden culture, Victorian flower-language dictionaries, Greek mythological references, and horticultural histories of peony breeding.</p>
"""
    fr = """
<p>La pivoine signifie la prospérité, l'honneur, la romance et le mariage heureux. En Chine, elle est la « reine des fleurs » et un symbole de richesse et de bonne fortune ; dans le langage des fleurs occidental, elle représente la timidité et, plus récemment, l'union longue et heureuse, ce qui en fait la fleur des douze ans de mariage et une favorite des noces. Sa floraison brève et somptueuse à la fin du printemps en fait aussi un symbole de la beauté éphémère.</p>

<h2>Origines : Chine, Japon et Europe</h2>
<p>La pivoine est cultivée en Chine depuis bien plus de mille ans, d'abord pour sa racine médicinale, puis, à partir de la dynastie Tang, comme fleur de la cour impériale. La pivoine arbustive (<em>mudan</em>) apparaît dans la poésie, la peinture et la porcelaine comme emblème du rang, de la richesse et de la beauté féminine, et la ville de Luoyang tient encore chaque printemps un festival de la pivoine. La fleur gagne le Japon vers le VIII<sup>e</sup> siècle, où elle prend des connotations de bravoure et de chance et devient un motif de tatouage courant aux côtés des lions et des dragons.</p>
<p>L'Europe connaissait une espèce indigène, et le nom vient de Péon, médecin des dieux dans la mythologie grecque, qui aurait été transformé en fleur pour échapper à un maître jaloux. Les herbiers médiévaux prisaient la racine de pivoine comme remède, et les grandes variétés de jardin que nous cultivons aujourd'hui ont été créées en France au XIX<sup>e</sup> siècle, d'où leurs nombreux noms français.</p>

<h2>Couleurs et nuances de sens</h2>
<ul>
<li><strong>Rose</strong> : la pivoine romantique ; amour, mariage, chance en couple.</li>
<li><strong>Blanche</strong> : la modestie ; c'est traditionnellement la pivoine « timide », et on l'offre aussi pour s'excuser.</li>
<li><strong>Rouge</strong> : porte le plus fortement le sens chinois ; richesse, honneur, respect.</li>
<li><strong>Corail et jaune</strong> : des hybrides modernes, perçus comme gais et festifs.</li>
</ul>
<p>Le sens victorien de « timidité » vient d'une histoire où des nymphes se cachaient dans les pétales de pivoine, et de l'habitude de la fleur de dissimuler son cœur sous une masse de pétales.</p>

<h2>Quand offrir des pivoines</h2>
<p>Les mariages et les douze ans d'union sont les occasions classiques. La pivoine convient aussi à une pendaison de crémaillère (prospérité pour la nouvelle maison), à une promotion, ou à toute occasion où l'on veut quelque chose de plus grandiose que des roses tout en restant doux. Comme la saison est courte (environ de la fin avril à juin dans l'hémisphère Nord), une botte de pivoines est un cadeau rare plutôt qu'un choix par défaut, et les gens le savent. Achetez-les en boutons serrés : elles s'ouvriront sur plusieurs jours ; un morceau de sucre dans l'eau est un vieux truc de fleuriste qui ne fait pas de mal.</p>

<h2>Questions fréquentes</h2>
<p><strong>La pivoine porte-t-elle bonheur ?</strong> Dans la tradition chinoise, nettement, surtout pour la richesse et le mariage. <strong>Est-ce malchanceux d'en avoir à la maison ?</strong> Non ; la seule mise en garde du vieux folklore européen vise le fait de déterrer une pivoine, ce qui fâcherait la plante et attirerait le malheur, une histoire sans doute inventée pour protéger des racines à croissance lente. <strong>Pivoine ou rose ?</strong> La rose parle d'amour ; la pivoine parle d'une belle vie à deux.</p>

<p class="small">Sources : histoires de la culture des jardins en Chine et au Japon, dictionnaires victoriens du langage des fleurs, références à la mythologie grecque, histoires horticoles de la création des pivoines.</p>
"""
    article_page("meanings",
        {"en": "peony-meaning", "fr": "signification-pivoine"},
        {"en": "Peony meaning: prosperity, romance and a happy marriage", "fr": "Signification de la pivoine : prospérité, romance et mariage heureux"},
        {"en": "What the peony symbolises in China, Japan and the West, what each colour means, and when to give one.",
         "fr": "Ce que symbolise la pivoine en Chine, au Japon et en Occident, le sens de chaque couleur, et quand l'offrir."},
        {"en": en, "fr": fr})


yellow_rose()
rose_colours()
teeth_dream()
eleven_eleven()
black_cat()
four_leaf_clover()
birthstones()
peony()
