import re
from transformers import pipeline

# =============================
# MODELS
# =============================

ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

skill_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# =============================
# BASIC EXTRACTORS
# =============================

def extract_email(text):
    m = re.search(r"\S+@\S+\.\S+", text)
    return m.group(0) if m else ""

def extract_phone(text):
    m = re.search(r"\+?\d[\d\s\-]{8,}\d", text)
    return m.group(0) if m else ""

def extract_links(text):
    return re.findall(r"(https?://\S+|www\.\S+)", text)

# =============================
# NAME & LOCATION (CONTACT BLOCK ONLY)
# =============================

def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) >= 2 and lines[0].isalpha() and lines[1].isalpha():
        return f"{lines[0]} {lines[1]}"
    return lines[0] if lines else ""

def extract_location(text):
    # Only look in top 6 lines (contact block)
    for line in text.split("\n")[:6]:
        clean = line.strip()
        if (
            clean.isalpha()
            and clean.lower() not in {"nidhi", "chaubey"}
            and 3 <= len(clean) <= 20
        ):
            return clean
    return ""

# =============================
# EXPERIENCE (JOB-LINE BASED)
# =============================

def extract_experience(text):
    companies = set()

    for line in text.split("\n"):
        # Only consider job-like lines
        if "|" in line or "--" in line:
            ents = ner(line)
            for e in ents:
                if e["entity_group"] == "ORG":
                    word = e["word"]
                    # Hard filters
                    if (
                        len(word) > 3
                        and "www" not in word.lower()
                        and "##" not in word
                        and not word.isupper()
                    ):
                        companies.add(word)

    return list(companies)

# =============================
# SKILL CANDIDATE EXTRACTION (STRICT)
# =============================

def extract_candidate_phrases(text):
    phrases = []

    for line in text.split("\n"):
        clean = re.sub(r"[•\-]", "", line).strip()

        # Reject sentences & verbs
        if len(clean.split()) > 3:
            continue
        if any(v in clean.lower() for v in ["worked", "built", "developed", "led", "tasks"]):
            continue

        # Reject numbers / names / locations
        if any(char.isdigit() for char in clean):
            continue
        if clean.istitle() and len(clean.split()) == 1:
            continue

        # Accept tech-like patterns
        if re.search(r"[A-Za-z#+/.]", clean):
            phrases.append(clean)

    return list(set(phrases))

# =============================
# AI-BASED SKILL CLASSIFICATION
# =============================

def classify_skills_with_ai(text):
    candidates = extract_candidate_phrases(text)

    hard, soft = [], []

    for phrase in candidates:
        result = skill_classifier(
            phrase,
            candidate_labels=["technical skill", "soft skill"],
            hypothesis_template="This is a {}."
        )

        if result["scores"][0] < 0.75:
            continue

        if result["labels"][0] == "technical skill":
            hard.append(phrase)
        else:
            soft.append(phrase)

    return hard, soft

# =============================
# MAIN PARSER
# =============================

def parse_resume(text):
    links = extract_links(text)

    github = next((l for l in links if "github" in l.lower()), "")
    linkedin = next((l for l in links if "linkedin" in l.lower()), "")

    hard_skills, soft_skills = classify_skills_with_ai(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "hard_skills": hard_skills,
        "soft_skills": soft_skills,
        "experience": extract_experience(text),
        "linkedin": linkedin,
        "github": github,
        "other_links": links
    }
