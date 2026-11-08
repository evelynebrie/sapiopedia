"""Quizzes: 4-result personality quizzes. Option k of every question scores result k."""
from sp import quiz_page

def quiz_colour():
    Q = {"en": [
        ("When you have a free evening, you…", ["Plan something with friends", "Start a new project", "Read or watch something quietly", "Go outside, whatever the weather"]),
        ("At work or school, people count on you to…", ["Bring energy", "Find solutions", "Keep things calm", "Say what others won't"]),
        ("Your ideal weekend place is…", ["A city full of people", "A workshop or a kitchen", "A quiet lake", "A mountain trail"]),
        ("When plans change at the last minute, you…", ["Love it", "Adapt and fix it", "Need a moment", "Push for your own plan"]),
        ("Pick a word:", ["Spark", "Build", "Still", "Bold"]),
        ("Your friends would say you are…", ["Warm", "Clever", "Steady", "Brave"]),
    ], "fr": [
        ("Quand vous avez une soirée libre, vous…", ["Organisez quelque chose avec des amis", "Commencez un nouveau projet", "Lisez ou regardez quelque chose au calme", "Sortez, peu importe la météo"]),
        ("Au travail ou à l'école, on compte sur vous pour…", ["Apporter de l'énergie", "Trouver des solutions", "Garder le calme", "Dire ce que les autres taisent"]),
        ("Votre endroit idéal pour un week-end :", ["Une ville pleine de monde", "Un atelier ou une cuisine", "Un lac tranquille", "Un sentier de montagne"]),
        ("Quand les plans changent à la dernière minute, vous…", ["Adorez ça", "Vous adaptez et réglez ça", "Avez besoin d'un moment", "Défendez votre propre plan"]),
        ("Choisissez un mot :", ["Étincelle", "Bâtir", "Calme", "Audace"]),
        ("Vos amis diraient que vous êtes…", ["Chaleureux", "Ingénieux", "Posé", "Courageux"]),
    ]}
    R = {"en": [("Coral", "#d9644a", "Warm, social, the one who gets everyone talking."),
                ("Teal", "#2f6f8f", "Curious and practical, you fix things and make them better."),
                ("Sage", "#6b8f71", "Calm and steady, the person people come to when it matters."),
                ("Amber", "#c9893a", "Bold and direct, you go first and say it straight.")],
         "fr": [("Corail", "#d9644a", "Chaleureux, sociable, celui qui fait parler tout le monde."),
                ("Sarcelle", "#2f6f8f", "Curieux et pratique, vous réparez et vous améliorez."),
                ("Sauge", "#6b8f71", "Calme et posé, la personne vers qui on va quand ça compte."),
                ("Ambre", "#c9893a", "Audacieux et direct, vous passez en premier et vous dites les choses.")]}
    quiz_page("quizzes",
        slug={"en": "what-colour-is-your-personality", "fr": "quelle-couleur-est-votre-personnalite"},
        title={"en": "What colour is your personality?", "fr": "Quelle couleur est votre personnalité ?"},
        desc={"en": "A 60-second quiz that gives you a colour and a shareable result card.", "fr": "Un quiz de 60 secondes qui vous donne une couleur et une image de résultat à partager."},
        Q=Q, R=R, kicker={"en": "Your colour is", "fr": "Votre couleur est"})

def quiz_mental_age():
    Q = {"en": [
        ("It's raining and you have nowhere to be. You…", ["Build a blanket fort or play a game", "Text everyone to see who's free", "Finally sort out that drawer", "Make tea and watch the rain"]),
        ("A friend cancels at the last minute. Your reaction?", ["Sulk for five minutes, then find something fun", "Pivot to plan B without missing a beat", "Honestly? Relieved, you have things to do", "Glad they told you; you'll see them another time"]),
        ("Your relationship with your phone:", ["It's for games and funny videos", "It's basically attached to your hand", "It's for the calendar and the group chat", "You answer when you hear it ring"]),
        ("What do you do with a surprise day off?", ["Something you've never tried", "Say yes to whatever comes up", "Catch up on everything that's piled up", "A long walk and an early night"]),
        ("At a dinner, you are the one who…", ["Starts the silly game", "Tells the story everyone retells", "Checks everyone has what they need", "Listens and asks the best question"]),
        ("Your idea of a good purchase:", ["Something bright and useless", "Tickets to something", "Something that makes life run smoother", "Something that will last twenty years"]),
        ("Pick a snack:", ["Cereal straight from the box", "Whatever the food truck has", "Something you meal-prepped", "Toast, done properly"]),
    ], "fr": [
        ("Il pleut et vous n'avez rien de prévu. Vous…", ["Construisez un fort de couvertures ou lancez un jeu", "Écrivez à tout le monde pour voir qui est libre", "Rangez enfin ce tiroir", "Préparez un thé et regardez la pluie"]),
        ("Un ami annule à la dernière minute. Votre réaction ?", ["Vous boudez cinq minutes, puis vous trouvez autre chose d'amusant", "Vous passez au plan B sans hésiter", "Franchement ? Soulagé, vous avez des choses à faire", "Content qu'il vous ait prévenu, vous le verrez une autre fois"]),
        ("Votre relation avec votre téléphone :", ["Il sert aux jeux et aux vidéos drôles", "Il est pratiquement collé à votre main", "Il sert à l'agenda et au groupe de discussion", "Vous répondez quand vous l'entendez sonner"]),
        ("Que faites-vous d'une journée de congé imprévue ?", ["Quelque chose que vous n'avez jamais essayé", "Vous dites oui à ce qui se présente", "Vous rattrapez tout ce qui s'est accumulé", "Une longue marche et un coucher tôt"]),
        ("À un souper, vous êtes la personne qui…", ["Lance le jeu ridicule", "Raconte l'histoire que tout le monde répète ensuite", "Vérifie que chacun a ce qu'il lui faut", "Écoute et pose la meilleure question"]),
        ("Votre idée d'un bon achat :", ["Quelque chose de coloré et d'inutile", "Des billets pour un spectacle", "Quelque chose qui simplifie le quotidien", "Quelque chose qui durera vingt ans"]),
        ("Choisissez une collation :", ["Des céréales directement dans la boîte", "Ce qu'offre le camion de cuisine de rue", "Un plat préparé à l'avance", "Une rôtie, faite comme il faut"]),
    ]}
    R = {"en": [("12 years old", "#B8405E", "You never lost the knack for wonder. Everything is still a game, and that is exactly why people love being around you."),
                ("25 years old", "#2E5F6E", "Curious, restless and always up for one more thing. Your calendar is full because your heart is."),
                ("40 years old", "#6E4A78", "You know what you want and how to get it done. The grown-up in the room, with a sense of humour to match."),
                ("70 years old", "#D9915F", "Wise, unhurried and impossible to rattle. You have already figured out that the small pleasures are the big ones.")],
         "fr": [("12 ans", "#B8405E", "Vous n'avez jamais perdu le sens de l'émerveillement. Tout est encore un jeu, et c'est exactement pour ça qu'on aime être avec vous."),
                ("25 ans", "#2E5F6E", "Curieux, en mouvement et toujours prêt pour une chose de plus. Votre agenda est plein parce que votre cœur l'est aussi."),
                ("40 ans", "#6E4A78", "Vous savez ce que vous voulez et comment y arriver. L'adulte de la pièce, avec l'humour qui va avec."),
                ("70 ans", "#D9915F", "Sage, sans hâte et impossible à déstabiliser. Vous avez déjà compris que les petits plaisirs sont les grands.")]}
    quiz_page("quizzes",
        slug={"en": "what-is-your-mental-age-quiz", "fr": "quel-est-votre-age-mental-quiz"},
        title={"en": "What is your mental age?", "fr": "Quel est votre âge mental ?"},
        desc={"en": "A 60-second quiz that reveals your mental age, from 12 to 70, with a result card to share.", "fr": "Un quiz de 60 secondes qui révèle votre âge mental, de 12 à 70 ans, avec une image de résultat à partager."},
        Q=Q, R=R, kicker={"en": "Your mental age is", "fr": "Votre âge mental est"})

def quiz_country():
    Q = {"en": [
        ("Your perfect morning starts with…", ["Quiet, order and a precise cup of tea", "Espresso at the counter and a chat", "Fresh air and a view of water", "Music, sun and a late start"]),
        ("How do you handle a disagreement?", ["Calmly, with respect for everyone's position", "Loudly, warmly, and it's over in ten minutes", "You apologise first, then talk it through", "You laugh it off and move on together"]),
        ("Your style could be described as…", ["Minimal and considered", "Effortlessly elegant", "Practical, with a good coat", "Colourful and relaxed"]),
        ("The best meal is…", ["Small, beautiful and seasonal", "Long, loud and homemade", "Hearty, shared around a fire", "Grilled, generous and eaten outside"]),
        ("What matters most in a friend?", ["Loyalty and discretion", "Passion and honesty", "Kindness and reliability", "Joy and spontaneity"]),
        ("Your ideal landscape:", ["A temple garden in the mist", "A hillside of olive trees", "A lake surrounded by forest", "A beach that never ends"]),
        ("How do you celebrate good news?", ["A quiet moment of gratitude", "Calling your whole family", "A toast with close friends", "Dancing, obviously"]),
    ], "fr": [
        ("Votre matin parfait commence par…", ["Le calme, l'ordre et un thé préparé avec soin", "Un expresso au comptoir et une conversation", "L'air frais et une vue sur l'eau", "De la musique, du soleil et un réveil tardif"]),
        ("Comment gérez-vous un désaccord ?", ["Calmement, en respectant la position de chacun", "Fort, chaleureusement, et c'est réglé en dix minutes", "Vous vous excusez d'abord, puis vous en discutez", "Vous en riez et vous passez à autre chose ensemble"]),
        ("On pourrait décrire votre style comme…", ["Minimaliste et réfléchi", "Élégant sans effort", "Pratique, avec un bon manteau", "Coloré et décontracté"]),
        ("Le meilleur repas est…", ["Petit, beau et de saison", "Long, bruyant et fait maison", "Copieux, partagé autour d'un feu", "Grillé, généreux et mangé dehors"]),
        ("Ce qui compte le plus chez un ami ?", ["La loyauté et la discrétion", "La passion et la franchise", "La gentillesse et la fiabilité", "La joie et la spontanéité"]),
        ("Votre paysage idéal :", ["Un jardin de temple dans la brume", "Une colline d'oliviers", "Un lac entouré de forêt", "Une plage qui ne finit jamais"]),
        ("Comment célébrez-vous une bonne nouvelle ?", ["Un moment de gratitude en silence", "Un appel à toute la famille", "Un verre avec vos proches", "En dansant, évidemment"]),
    ]}
    R = {"en": [("Japan", "#6C8C66", "Thoughtful, precise and quietly deep. You find beauty in details most people walk straight past."),
                ("Italy", "#B8405E", "You live with your whole heart: food, family, arguments and all. Life around you is never bland."),
                ("Canada", "#2E5F6E", "Kind, grounded and genuinely reliable. You make people feel safe, and you are at your best outdoors."),
                ("Brazil", "#6E4A78", "Warm, rhythmic and impossible not to smile around. You turn ordinary days into celebrations.")],
         "fr": [("Le Japon", "#6C8C66", "Réfléchi, précis et d'une profondeur discrète. Vous voyez la beauté dans des détails que la plupart des gens ignorent."),
                ("L'Italie", "#B8405E", "Vous vivez avec tout votre cœur : la table, la famille, les discussions animées. Autour de vous, la vie n'est jamais fade."),
                ("Le Canada", "#2E5F6E", "Gentil, posé et vraiment fiable. Les gens se sentent en sécurité avec vous, et vous êtes au mieux en plein air."),
                ("Le Brésil", "#6E4A78", "Chaleureux, rythmé et impossible à côtoyer sans sourire. Vous transformez les jours ordinaires en fêtes.")]}
    quiz_page("quizzes",
        slug={"en": "which-country-matches-your-personality-quiz", "fr": "quel-pays-vous-ressemble-quiz"},
        title={"en": "Which country matches your personality?", "fr": "Quel pays vous ressemble ?"},
        desc={"en": "Japan, Italy, Canada or Brazil? A 60-second personality quiz that finds the country that matches you.", "fr": "Japon, Italie, Canada ou Brésil ? Un quiz de personnalité de 60 secondes pour trouver le pays qui vous ressemble."},
        Q=Q, R=R, kicker={"en": "Your country is", "fr": "Votre pays est"})

def quiz_animal():
    Q = {"en": [
        ("Faced with a locked door, you…", ["Find another way in", "Study the lock until it makes sense", "Ask someone passing by", "Wait patiently; it will open"]),
        ("Your energy peaks…", ["At dusk, when things get interesting", "Late at night, in the quiet", "Mid-morning, surrounded by people", "After a very good meal"]),
        ("People come to you for…", ["A clever shortcut", "A wise opinion", "A good laugh and a pep talk", "A hug and a safe place"]),
        ("Your ideal home is…", ["Cosy, hidden and full of treasures", "High up with a view and lots of books", "Open, bright and close to the water", "Warm, solid and smelling of something baking"]),
        ("In a group project, you…", ["Spot the angle nobody saw", "Do the research everyone relies on", "Keep the team talking and laughing", "Carry the heavy parts without complaint"]),
        ("Pick a weather:", ["Crisp autumn evening", "Clear, starry night", "Sunny with a breeze", "First snow, seen from indoors"]),
        ("Your biggest strength:", ["Adaptability", "Insight", "Connection", "Loyalty"]),
    ], "fr": [
        ("Devant une porte fermée à clé, vous…", ["Trouvez un autre chemin", "Étudiez la serrure jusqu'à la comprendre", "Demandez à quelqu'un qui passe", "Attendez patiemment, elle s'ouvrira"]),
        ("Votre énergie est à son maximum…", ["Au crépuscule, quand ça devient intéressant", "Tard le soir, dans le silence", "En milieu de matinée, entouré de gens", "Après un très bon repas"]),
        ("Les gens viennent vous voir pour…", ["Un raccourci ingénieux", "Un avis réfléchi", "Un bon rire et des encouragements", "Un câlin et un endroit sûr"]),
        ("Votre maison idéale est…", ["Douillette, cachée et pleine de trésors", "En hauteur, avec une vue et beaucoup de livres", "Ouverte, lumineuse et près de l'eau", "Chaleureuse, solide et parfumée de quelque chose qui cuit"]),
        ("Dans un projet d'équipe, vous…", ["Voyez l'angle que personne n'avait vu", "Faites les recherches sur lesquelles tout le monde s'appuie", "Gardez l'équipe en train de parler et de rire", "Portez les parties lourdes sans vous plaindre"]),
        ("Choisissez une météo :", ["Une soirée d'automne fraîche", "Une nuit claire et étoilée", "Du soleil avec une brise", "La première neige, vue de l'intérieur"]),
        ("Votre plus grande force :", ["L'adaptabilité", "La clairvoyance", "Le lien avec les autres", "La loyauté"]),
    ]}
    R = {"en": [("Fox", "#D9915F", "Quick, clever and always one step ahead. You read a room in seconds and find the door nobody else noticed."),
                ("Owl", "#6C8C66", "Observant, wise and happiest when the world goes quiet. You see what others miss and say it only when it matters."),
                ("Dolphin", "#B8405E", "Playful, social and brilliant at bringing people together. Your joy is contagious and your loyalty runs deep."),
                ("Bear", "#2E5F6E", "Strong, protective and deeply comforting. You move at your own pace, and the people you love know they can always count on you.")],
         "fr": [("Le renard", "#D9915F", "Vif, rusé et toujours un pas en avance. Vous lisez une pièce en quelques secondes et trouvez la porte que personne n'a remarquée."),
                ("Le hibou", "#6C8C66", "Observateur, sage et le plus heureux quand le monde se tait. Vous voyez ce que les autres manquent et vous le dites seulement quand ça compte."),
                ("Le dauphin", "#B8405E", "Joueur, sociable et doué pour rassembler les gens. Votre joie est contagieuse et votre loyauté, profonde."),
                ("L'ours", "#2E5F6E", "Fort, protecteur et profondément rassurant. Vous avancez à votre rythme, et ceux que vous aimez savent qu'ils peuvent toujours compter sur vous.")]}
    quiz_page("quizzes",
        slug={"en": "what-animal-are-you-quiz", "fr": "quel-animal-etes-vous-quiz"},
        title={"en": "What animal are you?", "fr": "Quel animal êtes-vous ?"},
        desc={"en": "Fox, owl, dolphin or bear? Take this 60-second quiz to find your spirit animal and share the result.", "fr": "Renard, hibou, dauphin ou ours ? Faites ce quiz de 60 secondes pour découvrir votre animal et partager le résultat."},
        Q=Q, R=R, kicker={"en": "Your animal is", "fr": "Votre animal est"})

def quiz_introvert():
    Q = {"en": [
        ("After a big party, you feel…", ["Drained, and in need of a quiet day", "Energised and ready for the after-party", "Fine either way, depends on the party", "Happy you went, happier to be home"]),
        ("Your ideal Friday night:", ["Alone with a book or a show", "Out with as many people as possible", "Could go either way, you'll decide at six", "Dinner with two or three close friends"]),
        ("When your phone rings unexpectedly, you…", ["Let it go to voicemail", "Pick up on the first ring", "Answer if you know who it is", "Answer, then keep it short and warm"]),
        ("In meetings, you…", ["Think first, write your ideas afterwards", "Talk through your ideas out loud", "Adjust to the room", "Speak up when it's about something you care about"]),
        ("Small talk with strangers is…", ["Exhausting", "The best part of the day", "Fine in small doses", "Surprisingly easy, you just need a reason"]),
        ("You recharge by…", ["Being completely alone", "Being around people", "Switching between both", "A long one-on-one conversation"]),
        ("Your friends would say you are…", ["Thoughtful and private", "Outgoing and fun", "Flexible and easy", "Warm, once they got to know you"]),
    ], "fr": [
        ("Après une grande fête, vous vous sentez…", ["Vidé, avec besoin d'une journée tranquille", "Plein d'énergie, prêt pour la suite", "Bien dans les deux cas, ça dépend de la fête", "Content d'y être allé, plus content d'être rentré"]),
        ("Votre vendredi soir idéal :", ["Seul avec un livre ou une série", "Dehors avec le plus de monde possible", "L'un ou l'autre, vous déciderez à dix-huit heures", "Un souper avec deux ou trois amis proches"]),
        ("Quand votre téléphone sonne sans prévenir, vous…", ["Laissez la boîte vocale répondre", "Répondez à la première sonnerie", "Répondez si vous savez qui appelle", "Répondez, puis restez bref et chaleureux"]),
        ("En réunion, vous…", ["Réfléchissez d'abord, écrivez vos idées ensuite", "Développez vos idées à voix haute", "Vous ajustez à la salle", "Prenez la parole quand le sujet vous tient à cœur"]),
        ("Les conversations légères avec des inconnus, c'est…", ["Épuisant", "Le meilleur moment de la journée", "Correct à petites doses", "Étonnamment facile, il vous faut juste une raison"]),
        ("Vous rechargez vos batteries en…", ["Étant complètement seul", "Étant entouré de gens", "Alternant entre les deux", "Ayant une longue conversation en tête-à-tête"]),
        ("Vos amis diraient que vous êtes…", ["Réfléchi et réservé", "Sociable et amusant", "Souple et facile à vivre", "Chaleureux, une fois qu'ils vous connaissent"]),
    ]}
    R = {"en": [("Introvert", "#6E4A78", "Your inner world is rich and your attention is a gift. You do your best thinking in the quiet, and the people you let in are lucky."),
                ("Extrovert", "#D9915F", "You light up a room and you know it. People are your fuel, and your enthusiasm pulls everyone along for the ride."),
                ("Ambivert", "#6C8C66", "You read the moment and give it what it needs: a party on Friday, silence on Saturday. Few people are this adaptable."),
                ("Social introvert", "#B8405E", "You love people, in the right dose. Deep conversations over crowds, and a home to return to afterwards. The best of both.")],
         "fr": [("Introverti", "#6E4A78", "Votre monde intérieur est riche et votre attention est un cadeau. Vous réfléchissez le mieux dans le calme, et ceux que vous laissez entrer ont de la chance."),
                ("Extraverti", "#D9915F", "Vous illuminez une pièce et vous le savez. Les gens sont votre carburant, et votre enthousiasme entraîne tout le monde."),
                ("Ambiverti", "#6C8C66", "Vous lisez le moment et lui donnez ce qu'il demande : une fête le vendredi, le silence le samedi. Peu de gens sont aussi adaptables."),
                ("Introverti sociable", "#B8405E", "Vous aimez les gens, à la bonne dose. Les vraies conversations plutôt que la foule, et un chez-vous où revenir ensuite. Le meilleur des deux.")]}
    quiz_page("quizzes",
        slug={"en": "introvert-extrovert-or-ambivert-quiz", "fr": "introverti-extraverti-ou-ambiverti-quiz"},
        title={"en": "Introvert, extrovert or ambivert?", "fr": "Introverti, extraverti ou ambiverti ?"},
        desc={"en": "Introvert, extrovert, ambivert or social introvert? Find out in this 60-second quiz and share your result.", "fr": "Introverti, extraverti, ambiverti ou introverti sociable ? Découvrez-le avec ce quiz de 60 secondes à partager."},
        Q=Q, R=R, kicker={"en": "You are an", "fr": "Vous êtes"})

def quiz_season():
    Q = {"en": [
        ("Your favourite kind of light:", ["Soft morning light through new leaves", "Blazing noon sun", "Golden light at five o'clock", "Blue light on fresh snow"]),
        ("How do you approach a new project?", ["With fresh ideas and a burst of hope", "Full speed, all in", "Carefully, savouring each step", "Slowly, after a lot of thinking"]),
        ("Your comfort drink:", ["Green tea or lemonade", "Something iced", "Spiced cider or a latte", "Hot chocolate, no debate"]),
        ("What do people love about you?", ["Your optimism", "Your energy", "Your warmth", "Your calm"]),
        ("Your ideal afternoon:", ["Planting something, anything", "A lake, a swim, a crowd of friends", "A long walk through fallen leaves", "A blanket, a window, a book"]),
        ("Pick a scent:", ["Rain on fresh grass", "Sunscreen and salt", "Wood smoke and cinnamon", "Pine and cold air"]),
        ("Pick a feeling:", ["Beginning", "Freedom", "Nostalgia", "Peace"]),
    ], "fr": [
        ("Votre lumière préférée :", ["La lumière douce du matin à travers les jeunes feuilles", "Le soleil éclatant de midi", "La lumière dorée de dix-sept heures", "La lumière bleue sur la neige fraîche"]),
        ("Comment abordez-vous un nouveau projet ?", ["Avec des idées neuves et un élan d'espoir", "À fond, sans retenue", "Avec soin, en savourant chaque étape", "Lentement, après beaucoup de réflexion"]),
        ("Votre boisson réconfortante :", ["Un thé vert ou une limonade", "Quelque chose de glacé", "Un cidre épicé ou un café au lait", "Un chocolat chaud, sans discussion"]),
        ("Ce que les gens aiment chez vous ?", ["Votre optimisme", "Votre énergie", "Votre chaleur", "Votre calme"]),
        ("Votre après-midi idéal :", ["Planter quelque chose, n'importe quoi", "Un lac, une baignade, une bande d'amis", "Une longue marche dans les feuilles tombées", "Une couverture, une fenêtre, un livre"]),
        ("Choisissez une odeur :", ["La pluie sur l'herbe fraîche", "La crème solaire et le sel", "La fumée de bois et la cannelle", "Le sapin et l'air froid"]),
        ("Choisissez une sensation :", ["Le commencement", "La liberté", "La nostalgie", "La paix"]),
    ]}
    R = {"en": [("Spring", "#2E5F6E", "Hopeful, fresh and always starting something. You believe things can grow, and around you they usually do."),
                ("Summer", "#6E4A78", "Bright, generous and fully alive. You say yes to the day and bring everyone along with you."),
                ("Autumn", "#D9915F", "Warm, reflective and beautifully layered. You know how to slow down and make a moment feel like a memory."),
                ("Winter", "#6C8C66", "Calm, clear and quietly strong. You find stillness where others see cold, and your home is where people come to rest.")],
         "fr": [("Le printemps", "#2E5F6E", "Plein d'espoir, frais et toujours en train de commencer quelque chose. Vous croyez que les choses peuvent pousser, et autour de vous, elles poussent."),
                ("L'été", "#6E4A78", "Lumineux, généreux et pleinement vivant. Vous dites oui à la journée et vous emmenez tout le monde avec vous."),
                ("L'automne", "#D9915F", "Chaleureux, réfléchi et riche en nuances. Vous savez ralentir et transformer un instant en souvenir."),
                ("L'hiver", "#6C8C66", "Calme, clair et d'une force tranquille. Vous trouvez la sérénité où d'autres voient le froid, et c'est chez vous qu'on vient se reposer.")]}
    quiz_page("quizzes",
        slug={"en": "what-season-are-you-quiz", "fr": "quelle-saison-etes-vous-quiz"},
        title={"en": "What season are you?", "fr": "Quelle saison êtes-vous ?"},
        desc={"en": "Spring, summer, autumn or winter? A 60-second personality quiz that tells you which season you are.", "fr": "Printemps, été, automne ou hiver ? Un quiz de personnalité de 60 secondes qui vous dit quelle saison vous êtes."},
        Q=Q, R=R, kicker={"en": "Your season is", "fr": "Votre saison est"})

def quiz_flower():
    Q = {"en": [
        ("How do you walk into a room?", ["Gracefully, and people notice", "Beaming, saying hello to everyone", "Quietly, finding a comfortable corner", "On your own terms, a little late"]),
        ("Your ideal garden:", ["Lush, romantic and a little overgrown", "Big, open and full of bees", "Neat rows with a soothing scent", "Wild, with a stone wall to climb"]),
        ("How do you show someone you care?", ["A thoughtful, beautiful gift", "Showing up, loudly and often", "Making them a cup of something calming", "Defending them fiercely"]),
        ("Your favourite time of day:", ["Late afternoon, soft light", "High noon", "Early evening, when it cools down", "Dawn, before anyone is up"]),
        ("What do you need to thrive?", ["Attention and a bit of fuss", "Sun, sun and more sun", "Routine and quiet", "Space and freedom"]),
        ("Your style is…", ["Layered and luxurious", "Bright and cheerful", "Soft, muted tones", "Natural, slightly untamed"]),
        ("Pick a word:", ["Bloom", "Shine", "Breathe", "Roam"]),
    ], "fr": [
        ("Comment entrez-vous dans une pièce ?", ["Avec grâce, et on vous remarque", "Rayonnant, en saluant tout le monde", "Discrètement, en trouvant un coin confortable", "À votre façon, un peu en retard"]),
        ("Votre jardin idéal :", ["Luxuriant, romantique et un peu sauvage", "Grand, ouvert et plein d'abeilles", "Des rangs nets et un parfum apaisant", "Libre, avec un mur de pierre à grimper"]),
        ("Comment montrez-vous à quelqu'un que vous tenez à lui ?", ["Un cadeau réfléchi et beau", "En étant là, souvent et avec éclat", "En lui préparant une boisson réconfortante", "En le défendant farouchement"]),
        ("Votre moment préféré de la journée :", ["La fin d'après-midi, lumière douce", "Le plein midi", "Le début de soirée, quand ça se rafraîchit", "L'aube, avant que tout le monde se lève"]),
        ("De quoi avez-vous besoin pour vous épanouir ?", ["D'attention et d'un peu de soin", "De soleil, encore du soleil", "De routine et de calme", "D'espace et de liberté"]),
        ("Votre style est…", ["Superposé et luxueux", "Vif et joyeux", "Des tons doux et feutrés", "Naturel, légèrement indompté"]),
        ("Choisissez un mot :", ["Éclore", "Rayonner", "Respirer", "Vagabonder"]),
    ]}
    R = {"en": [("Peony", "#B8405E", "Generous, romantic and a little bit extravagant. You bloom big, and when you do, nobody can look away."),
                ("Sunflower", "#2E5F6E", "You turn toward the light and bring everyone with you. Open, loyal and impossible not to smile at."),
                ("Lavender", "#6E4A78", "Calm, healing and quietly elegant. People breathe easier when you are nearby, even if they can't say why."),
                ("Wild rose", "#D9915F", "Beautiful, free and not to be tamed. You grow where you choose, and your thorns are just honesty.")],
         "fr": [("La pivoine", "#B8405E", "Généreuse, romantique et un brin extravagante. Quand vous éclosez, c'est en grand, et personne ne peut détourner le regard."),
                ("Le tournesol", "#2E5F6E", "Vous vous tournez vers la lumière et vous entraînez tout le monde avec vous. Ouvert, loyal et impossible à regarder sans sourire."),
                ("La lavande", "#6E4A78", "Apaisante, calme et d'une élégance discrète. Les gens respirent mieux près de vous, même sans savoir pourquoi."),
                ("La rose sauvage", "#D9915F", "Belle, libre et impossible à dompter. Vous poussez où vous le choisissez, et vos épines ne sont que de la franchise.")]}
    quiz_page("quizzes",
        slug={"en": "what-flower-are-you-quiz", "fr": "quelle-fleur-etes-vous-quiz"},
        title={"en": "What flower are you?", "fr": "Quelle fleur êtes-vous ?"},
        desc={"en": "Peony, sunflower, lavender or wild rose? Discover your flower with this 60-second quiz and a shareable card.", "fr": "Pivoine, tournesol, lavande ou rose sauvage ? Découvrez votre fleur avec ce quiz de 60 secondes et une image à partager."},
        Q=Q, R=R, kicker={"en": "Your flower is", "fr": "Votre fleur est"})

def quiz_traveller():
    Q = {"en": [
        ("Three weeks before a trip, you…", ["Have a colour-coded itinerary", "Have a flight and nothing else", "Have a list of restaurants, in order", "Have booked one place and plan to stay there"]),
        ("Your suitcase is…", ["Packed from a checklist", "Half empty, you'll figure it out", "Mostly room for things to bring back", "Light, with a book and good shoes"]),
        ("You get lost in a new city. You…", ["Open the map you downloaded earlier", "Love it; this is the whole point", "Follow the smell of something cooking", "Sit on a bench and watch for a while"]),
        ("The best souvenir is…", ["A photo of every place on the list", "A story you can't quite explain", "A spice or a recipe", "A café where they learned your name"]),
        ("Your ideal travel companion…", ["Trusts the plan", "Says yes to anything", "Will share every dish", "Doesn't mind a slow morning"]),
        ("On the last day, you…", ["Have ticked off everything", "Discover something that changes the trip", "Go back to your favourite restaurant", "Feel like a local already"]),
        ("Pick a word:", ["Itinerary", "Detour", "Market", "Stay"]),
    ], "fr": [
        ("Trois semaines avant un voyage, vous…", ["Avez un itinéraire classé par couleurs", "Avez un vol et rien d'autre", "Avez une liste de restaurants, dans l'ordre", "Avez réservé un seul endroit et comptez y rester"]),
        ("Votre valise est…", ["Faite à partir d'une liste", "À moitié vide, vous verrez bien", "Surtout de la place pour ce que vous rapporterez", "Légère, avec un livre et de bonnes chaussures"]),
        ("Vous vous perdez dans une nouvelle ville. Vous…", ["Ouvrez la carte téléchargée à l'avance", "Adorez ça, c'est tout l'intérêt", "Suivez l'odeur de quelque chose qui cuit", "Vous assoyez sur un banc et observez un moment"]),
        ("Le meilleur souvenir est…", ["Une photo de chaque endroit de la liste", "Une histoire que vous n'arrivez pas vraiment à expliquer", "Une épice ou une recette", "Un café où l'on a appris votre prénom"]),
        ("Votre compagnon de voyage idéal…", ["Fait confiance au plan", "Dit oui à tout", "Partage chaque plat", "Ne voit pas d'inconvénient à un matin lent"]),
        ("Le dernier jour, vous…", ["Avez tout coché", "Découvrez quelque chose qui change le voyage", "Retournez à votre restaurant préféré", "Vous sentez déjà du quartier"]),
        ("Choisissez un mot :", ["Itinéraire", "Détour", "Marché", "Rester"]),
    ]}
    R = {"en": [("The planner", "#6C8C66", "Nothing gets missed when you travel. Your friends tease you about the spreadsheet, then thank you for the perfect day."),
                ("The wanderer", "#B8405E", "You follow your feet and the best stories follow you. The unplanned detour is where your trip really begins."),
                ("The foodie", "#2E5F6E", "You understand a place through its table. Markets, kitchens and the one dish nobody else dared to order."),
                ("The slow traveller", "#6E4A78", "You don't visit places, you live in them for a while. One neighbourhood, one café, and you leave with friends.")],
         "fr": [("Le planificateur", "#6C8C66", "Rien n'échappe à votre voyage. Vos amis vous taquinent au sujet du tableau, puis vous remercient pour la journée parfaite."),
                ("Le vagabond", "#B8405E", "Vous suivez vos pas et les meilleures histoires vous suivent. C'est au détour imprévu que votre voyage commence vraiment."),
                ("Le gourmand", "#2E5F6E", "Vous comprenez un lieu par sa table. Les marchés, les cuisines et le plat que personne d'autre n'a osé commander."),
                ("Le voyageur lent", "#6E4A78", "Vous ne visitez pas les endroits, vous y vivez un moment. Un quartier, un café, et vous repartez avec des amis.")]}
    quiz_page("quizzes",
        slug={"en": "what-kind-of-traveller-are-you-quiz", "fr": "quel-type-de-voyageur-etes-vous-quiz"},
        title={"en": "What kind of traveller are you?", "fr": "Quel type de voyageur êtes-vous ?"},
        desc={"en": "Planner, wanderer, foodie or slow traveller? A 60-second quiz that reveals your travel style, with a card to share.", "fr": "Planificateur, vagabond, gourmand ou voyageur lent ? Un quiz de 60 secondes qui révèle votre style de voyage."},
        Q=Q, R=R, kicker={"en": "You are", "fr": "Vous êtes"})

def quiz_room():
    Q = {"en": [
        ("Guests arrive. Where do they end up?", ["Around you while you cook", "Browsing your shelves", "Outside, looking at the view", "Nowhere; your home is for your people only"]),
        ("Your favourite sound:", ["Something sizzling", "Pages turning", "Birds and distant traffic", "Rain on the window"]),
        ("What do you offer someone who is sad?", ["Food, immediately", "A quote or a book that helped you", "Fresh air and a walk", "A blanket and no questions"]),
        ("Your ideal Sunday:", ["A long, messy brunch", "An afternoon lost in reading", "Coffee outside, feet up", "Staying in pyjamas until noon"]),
        ("Your biggest strength:", ["Generosity", "Curiosity", "Perspective", "Comfort"]),
        ("Pick a light:", ["Warm pendant over a table", "A reading lamp", "Daylight, as much as possible", "Candles and a dimmer"]),
        ("Pick a word:", ["Nourish", "Learn", "Breathe", "Rest"]),
    ], "fr": [
        ("Des invités arrivent. Où finissent-ils ?", ["Autour de vous pendant que vous cuisinez", "Devant vos étagères", "Dehors, à regarder la vue", "Nulle part, votre maison est réservée à vos proches"]),
        ("Votre son préféré :", ["Quelque chose qui grésille dans la poêle", "Des pages qui tournent", "Les oiseaux et la circulation au loin", "La pluie sur la fenêtre"]),
        ("Qu'offrez-vous à quelqu'un qui est triste ?", ["À manger, tout de suite", "Une citation ou un livre qui vous a aidé", "De l'air frais et une marche", "Une couverture et aucune question"]),
        ("Votre dimanche idéal :", ["Un long brunch désordonné", "Un après-midi perdu dans la lecture", "Un café dehors, les pieds surélevés", "Rester en pyjama jusqu'à midi"]),
        ("Votre plus grande force :", ["La générosité", "La curiosité", "Le recul", "Le réconfort"]),
        ("Choisissez un éclairage :", ["Une suspension chaude au-dessus d'une table", "Une lampe de lecture", "La lumière du jour, le plus possible", "Des chandelles et un gradateur"]),
        ("Choisissez un mot :", ["Nourrir", "Apprendre", "Respirer", "Se reposer"]),
    ]}
    R = {"en": [("The kitchen", "#D9915F", "You are the heart of the house. People gather around you without being asked, and nobody ever leaves hungry."),
                ("The library", "#6C8C66", "Curious, calm and full of stories. You are the room people visit when they want to think, or to be understood."),
                ("The balcony", "#B8405E", "You give people perspective and fresh air. Half inside, half out, you are where the best late-night talks happen."),
                ("The bedroom", "#2E5F6E", "Soft, private and deeply restorative. You are where people feel safe enough to finally let go.")],
         "fr": [("La cuisine", "#D9915F", "Vous êtes le cœur de la maison. Les gens se rassemblent autour de vous sans qu'on le leur demande, et personne ne repart le ventre vide."),
                ("La bibliothèque", "#6C8C66", "Curieux, calme et plein d'histoires. Vous êtes la pièce où l'on vient pour réfléchir, ou pour être compris."),
                ("Le balcon", "#B8405E", "Vous offrez du recul et de l'air frais. Mi-dedans, mi-dehors, c'est chez vous que naissent les meilleures conversations de fin de soirée."),
                ("La chambre", "#2E5F6E", "Douce, intime et profondément réparatrice. Vous êtes l'endroit où l'on se sent assez en sécurité pour enfin lâcher prise.")]}
    quiz_page("quizzes",
        slug={"en": "which-room-of-the-house-are-you-quiz", "fr": "quelle-piece-de-la-maison-etes-vous-quiz"},
        title={"en": "Which room of the house are you?", "fr": "Quelle pièce de la maison êtes-vous ?"},
        desc={"en": "Kitchen, library, balcony or bedroom? A 60-second personality quiz that tells you which room you are.", "fr": "Cuisine, bibliothèque, balcon ou chambre ? Un quiz de personnalité de 60 secondes qui vous dit quelle pièce vous êtes."},
        Q=Q, R=R, kicker={"en": "You are", "fr": "Vous êtes"})

def quiz_name():
    Q = {"en": [
        ("Your handwriting is…", ["Loopy and expressive", "Fast and slightly messy", "Clean and even", "Small and practical"]),
        ("Your ideal city:", ["Paris at dusk", "Lisbon in the sun", "Marrakech at the market", "Any city with a good bike lane"]),
        ("How do you dress for a first date?", ["Something with a bit of drama", "Whatever makes you laugh in the mirror", "Something soft and well cut", "Exactly what you wore to work"]),
        ("Your love language:", ["Handwritten notes", "Surprise adventures", "Long, patient listening", "Fixing things before you're asked"]),
        ("Your favourite hour:", ["Golden hour", "Lunchtime", "Dawn", "Whenever the work is done"]),
        ("Your friends describe you as…", ["Romantic", "Sunny", "Serene", "Solid"]),
        ("Pick an instrument:", ["Cello", "Trumpet", "Oud", "Acoustic guitar"]),
    ], "fr": [
        ("Votre écriture est…", ["Bouclée et expressive", "Rapide et un peu brouillonne", "Nette et régulière", "Petite et pratique"]),
        ("Votre ville idéale :", ["Paris au crépuscule", "Lisbonne au soleil", "Marrakech au marché", "Toute ville avec une bonne piste cyclable"]),
        ("Comment vous habillez-vous pour un premier rendez-vous ?", ["Quelque chose avec un peu de panache", "Ce qui vous fait rire devant le miroir", "Quelque chose de doux et bien coupé", "Exactement ce que vous portiez au travail"]),
        ("Votre façon d'aimer :", ["Des mots écrits à la main", "Des aventures surprises", "Une écoute longue et patiente", "Réparer les choses avant qu'on vous le demande"]),
        ("Votre heure préférée :", ["L'heure dorée", "L'heure du dîner", "L'aube", "Quand le travail est fini"]),
        ("Vos amis vous décrivent comme…", ["Romantique", "Ensoleillé", "Serein", "Solide"]),
        ("Choisissez un instrument :", ["Le violoncelle", "La trompette", "Le oud", "La guitare acoustique"]),
    ]}
    R = {"en": [("Juliette", "#6E4A78", "Poetic, intense and a little old-fashioned in the best way. You feel everything deeply and make ordinary moments cinematic."),
                ("Léo", "#D9915F", "Bright, bold and endlessly likeable. You walk in with a grin and leave with three new friends."),
                ("Nour", "#6C8C66", "Nour means light, and that is exactly what you bring: calm, clarity and a quiet warmth people lean toward."),
                ("Sam", "#B8405E", "Easygoing, dependable and genuinely good company. No fuss, no drama, just someone everyone is glad to have around.")],
         "fr": [("Juliette", "#6E4A78", "Poétique, intense et un peu d'une autre époque, dans le meilleur sens. Vous ressentez tout profondément et rendez les moments ordinaires dignes du cinéma."),
                ("Léo", "#D9915F", "Lumineux, audacieux et infiniment sympathique. Vous entrez avec un grand sourire et repartez avec trois nouveaux amis."),
                ("Nour", "#6C8C66", "Nour veut dire lumière, et c'est exactement ce que vous apportez : du calme, de la clarté et une chaleur discrète qui attire les gens."),
                ("Sam", "#B8405E", "Décontracté, fiable et d'une compagnie sincèrement agréable. Pas de chichis, pas de drame, juste quelqu'un que tout le monde est content d'avoir près de soi.")]}
    quiz_page("quizzes",
        slug={"en": "what-should-your-name-have-been-quiz", "fr": "quel-prenom-auriez-vous-du-avoir-quiz"},
        title={"en": "What should your name have been?", "fr": "Quel prénom auriez-vous dû avoir ?"},
        desc={"en": "Juliette, Léo, Nour or Sam? A 60-second quiz that finds the name that truly fits your personality.", "fr": "Juliette, Léo, Nour ou Sam ? Un quiz de 60 secondes qui trouve le prénom qui correspond vraiment à votre personnalité."},
        Q=Q, R=R, kicker={"en": "Your name should have been", "fr": "Votre prénom aurait dû être"})

quiz_colour()
quiz_mental_age()
quiz_country()
quiz_animal()
quiz_introvert()
quiz_season()
quiz_flower()
quiz_traveller()
quiz_room()
quiz_name()
