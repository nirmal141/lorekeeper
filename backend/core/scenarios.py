SCENARIOS = [
    {
        "id": "ashwood",
        "name": "The Ashwood Post",
        "genre": "Fantasy",
        "tagline": "Bandits at the gates. Trust no one.",
        "description": (
            "A quiet trading post at the edge of the Ashwood. "
            "Tensions have been rising since the northern roads closed. "
            "Merchants whisper about bandits, and the blacksmith has been forging more weapons than tools."
        ),
        "npcs": [
            {
                "id": "aldric",
                "name": "Aldric",
                "role": "merchant",
                "backstory": (
                    "An aging merchant who lost his son to the northern wars. "
                    "He runs the only supply shop at the trading post. "
                    "Protective of his remaining stock and deeply suspicious of armed travelers, "
                    "but shows kindness to those who earn his trust."
                ),
                "goals": ["protect his shop", "find news of his son", "keep the trading post safe"],
            },
            {
                "id": "mira",
                "name": "Blacksmith Mira",
                "role": "blacksmith",
                "backstory": (
                    "A skilled blacksmith who arrived at the trading post two years ago from the east. "
                    "She speaks little about her past. She distrusts outsiders but is fiercely loyal "
                    "to those she considers friends. Her blades are the finest in the region."
                ),
                "goals": ["forge a legendary weapon", "protect the trading post", "uncover the source of the bandit raids"],
            },
        ],
    },
    {
        "id": "starfall",
        "name": "Starfall Station",
        "genre": "Sci-Fi",
        "tagline": "The reactor is failing. Someone knows why.",
        "description": (
            "A remote research station orbiting a dying star. "
            "The fusion reactor has been losing power for weeks and no one can explain why. "
            "Crew morale is low. The last supply ship is three months out."
        ),
        "npcs": [
            {
                "id": "reyes",
                "name": "Commander Reyes",
                "role": "station chief",
                "backstory": (
                    "A decorated military officer reassigned to this remote posting as punishment "
                    "for questioning high command. She runs the station with iron discipline but "
                    "privately fears they've been abandoned. She trusts data over people."
                ),
                "goals": ["keep the crew alive", "fix the reactor", "find out why command stopped responding"],
            },
            {
                "id": "lian",
                "name": "Dr. Lian",
                "role": "xenobiologist",
                "backstory": (
                    "A brilliant but secretive scientist who requested this posting specifically. "
                    "She spends long hours in the lower labs studying alien samples from the star's corona. "
                    "Some crew members think her experiments are connected to the reactor failures."
                ),
                "goals": ["complete her research before evacuation", "protect her specimens", "avoid suspicion"],
            },
        ],
    },
    {
        "id": "dusty-gulch",
        "name": "Dusty Gulch",
        "genre": "Western",
        "tagline": "The sheriff is dead. The town needs a hero.",
        "description": (
            "A sun-scorched frontier town at the edge of the territories. "
            "Sheriff Callahan was found dead this morning, and the cattle baron's men "
            "have been circling the town like vultures. Nobody wants to be next."
        ),
        "npcs": [
            {
                "id": "mae",
                "name": "Mae",
                "role": "saloon owner",
                "backstory": (
                    "Mae runs the only saloon in Dusty Gulch and knows every secret in town. "
                    "She came west to escape a scandal back east and has built a life here. "
                    "She's tough, sharp-tongued, and the closest thing this town has to a leader now."
                ),
                "goals": ["keep the saloon open", "protect the townspeople", "find out who killed the sheriff"],
            },
            {
                "id": "hank",
                "name": "Deputy Hank",
                "role": "deputy",
                "backstory": (
                    "A young deputy who idolized Sheriff Callahan. He's scared and out of his depth "
                    "but refuses to abandon the badge. He suspects the cattle baron but has no proof. "
                    "He drinks too much and his hands shake when he draws."
                ),
                "goals": ["find the sheriff's killer", "stand up to the cattle baron", "prove he's worthy of the badge"],
            },
        ],
    },
    {
        "id": "holloway",
        "name": "The Holloway Case",
        "genre": "Noir",
        "tagline": "Your client is dead. The answers aren't.",
        "description": (
            "A rain-soaked city at night. You're a private investigator and your latest client, "
            "Victor Holloway, was found dead in his apartment two hours after hiring you. "
            "The police say suicide. The evidence says otherwise."
        ),
        "npcs": [
            {
                "id": "sloan",
                "name": "Detective Sloan",
                "role": "private investigator",
                "backstory": (
                    "A former police detective who left the force after a corruption scandal. "
                    "He opened a private practice and takes the cases nobody else will touch. "
                    "Cynical, methodical, and haunted by the cases he couldn't solve."
                ),
                "goals": ["find out who killed Holloway", "stay one step ahead of the police", "uncover the conspiracy"],
            },
            {
                "id": "ruby",
                "name": "Ruby",
                "role": "informant",
                "backstory": (
                    "A nightclub singer who works as an informant on the side. "
                    "She knew Victor Holloway personally and is the last person who saw him alive. "
                    "She's scared but won't admit it. She knows more than she's telling."
                ),
                "goals": ["stay alive", "protect her secrets", "find out if Holloway's death is connected to her past"],
            },
        ],
    },
    {
        "id": "byte-brew",
        "name": "Byte & Brew",
        "genre": "Modern",
        "tagline": "Demo day is tomorrow. Nothing works.",
        "description": (
            "A cramped startup office above a coffee shop. Your AI startup 'Byte & Brew' "
            "has a demo for investors tomorrow morning, but the product crashed last night "
            "and the co-founders aren't speaking to each other."
        ),
        "npcs": [
            {
                "id": "priya",
                "name": "Priya",
                "role": "CEO & co-founder",
                "backstory": (
                    "A charismatic first-time founder who quit her consulting job to start this company. "
                    "She's brilliant at pitching but has been hiding how bad the finances are. "
                    "She believes the demo will save everything if they can just get it working."
                ),
                "goals": ["nail the investor demo", "fix the relationship with Marcus", "keep the company alive"],
            },
            {
                "id": "marcus",
                "name": "Marcus",
                "role": "CTO & co-founder",
                "backstory": (
                    "A gifted engineer who built the entire product alone. He's been working 18-hour days "
                    "and is burned out. He's angry that Priya keeps promising features they can't deliver. "
                    "He's considering walking away but can't abandon what he built."
                ),
                "goals": ["fix the crashed product", "have an honest conversation with Priya", "decide if he should stay or leave"],
            },
        ],
    },
]
