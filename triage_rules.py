def triage(symptoms_text):
    text = symptoms_text.lower()

    # ---------------- CONDITIONS ----------------
    protocols = {
        "bleeding": {
            "level": "CRITICAL",
            "color": "🔴",
            "do": [
                "Apply firm pressure to stop bleeding",
                "Keep the injured area elevated",
                "Use clean cloth or bandage if available"
            ],
            "dont": [
                "Do not remove deeply embedded objects",
                "Do not stop pressure too early"
            ],
            "monitor": [
                "Amount of bleeding",
                "Signs of shock (pale skin, dizziness)"
            ]
        },
        "chest pain": {
            "level": "CRITICAL",
            "color": "🔴",
            "do": [
                "Make the patient sit or lie down comfortably",
                "Keep the patient calm and still",
                "Loosen tight clothing"
            ],
            "dont": [
                "Do not allow physical exertion",
                "Do not give food or drink"
            ],
            "monitor": [
                "Pain intensity",
                "Breathing and consciousness"
            ]
        },
        "difficulty breathing": {
            "level": "CRITICAL",
            "color": "🔴",
            "do": [
                "Sit the patient upright",
                "Loosen tight clothing",
                "Ensure fresh air circulation"
            ],
            "dont": [
                "Do not lay the patient flat",
                "Do not give sedatives"
            ],
            "monitor": [
                "Breathing rate",
                "Lip or nail discoloration"
            ]
        },
        "fever": {
            "level": "MODERATE",
            "color": "🟡",
            "do": [
                "Encourage oral fluids",
                "Keep patient in a cool environment",
                "Give paracetamol if available and advised"
            ],
            "dont": [
                "Do not give antibiotics without prescription",
                "Do not overdress the patient"
            ],
            "monitor": [
                "Temperature",
                "Signs of dehydration"
            ]
        },
        "unconscious": {
            "level": "CRITICAL",
            "color": "🔴",
            "do": [
                "Place patient in recovery position",
                "Check airway and breathing",
                "Remove nearby hazards"
            ],
            "dont": [
                "Do not give food or water",
                "Do not shake the patient"
            ],
            "monitor": [
                "Breathing",
                "Response to stimuli"
            ]
        }
    }

    # ---------------- MATCH LOGIC ----------------
    for key in protocols:
        if key in text:
            return {
                "level": protocols[key]["level"],
                "color": protocols[key]["color"],
                "do": protocols[key]["do"],
                "dont": protocols[key]["dont"],
                "monitor": protocols[key]["monitor"],
                "confidence": "0.90"
            }

    # ---------------- DEFAULT ----------------
    return {
        "level": "MILD",
        "color": "🟢",
        "do": [
            "Provide basic care and rest",
            "Encourage fluids"
        ],
        "dont": [
            "Do not ignore worsening symptoms"
        ],
        "monitor": [
            "General condition",
            "Symptom progression"
        ],
        "confidence": "0.75"
    }
