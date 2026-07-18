"""Helper script to generate canonical feature collection fixtures for integration testing.

Purpose:
    Produce simple, complex, large, duplicated, and empty JSON files representing
    CanonicalFeatureCollections for both resume and job description.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

# Setup target directory
fixtures_dir = Path("tests/fixtures")
fixtures_dir.mkdir(parents=True, exist_ok=True)


def create_feature(
    feature_id: str,
    name: str,
    category: str,
    value: Any,
    source_id: str | None = None,
    confidence: float = 1.0,
) -> dict:
    return {
        "feature_id": feature_id,
        "name": name,
        "category": category,
        "value": value,
        "confidence": confidence,
        "locations": [{"page_number": 1, "block_index": 0, "line_index": 0, "start_character": 0, "end_character": 10}],
        "provenance": {
            "source_entity_id": source_id,
            "source_entity_type": category,
            "source_section": "EXPERIENCE" if category == "EXPERIENCE" else "UNKNOWN",
            "source_document": "document.pdf",
            "matched_rules": ["rule_1"],
        },
        "metadata": {
            "creation_timestamp": "2026-07-13T20:00:00Z",
            "extractor_name": "TestExtractor",
            "version": "1.0",
            "custom_attributes": {},
        },
    }


def create_collection(features_list: list[dict]) -> dict:
    return {
        "features": features_list,
        "statistics": {
            "total_features_extracted": len(features_list),
            "extractor_counts": {},
            "execution_duration_seconds": 0.1,
        },
        "context": {
            "correlation_id": "test-correlation-id",
            "rule_engine_config": {},
            "environment": "testing",
            "metadata": {},
        },
    }


def create_canonical_collection(
    skills: list[dict] = None,
    experience: list[dict] = None,
    education: list[dict] = None,
    projects: list[dict] = None,
    certifications: list[dict] = None,
) -> dict:
    skills = skills or []
    experience = experience or []
    education = education or []
    projects = projects or []
    certifications = certifications or []

    total_count = len(skills) + len(experience) + len(education) + len(projects) + len(certifications)

    return {
        "skills": create_collection(skills),
        "experience": create_collection(experience),
        "education": create_collection(education),
        "projects": create_collection(projects),
        "certifications": create_collection(certifications),
        "statistics": {
            "total_feature_count": total_count,
            "duplicate_count": 0,
            "validation_error_count": 0,
            "warning_count": 0,
            "category_counts": {
                "SKILL": len(skills),
                "EXPERIENCE": len(experience),
                "EDUCATION": len(education),
                "PROJECT": len(projects),
                "CERTIFICATION": len(certifications),
            },
        },
        "validation_summary": {
            "status": "VALID",
            "errors": [],
            "warnings": [],
            "duplicate_count": 0,
            "validation_timestamp": "2026-07-13T20:00:00Z",
            "rules_version": "v1.0",
        },
        "metadata": {},
    }


# 1. Simple Resume (Python, SQL, AWS, 5 Years Exp, B.Tech Education, AWS Developer Certification, Inventory System Project)
res_simple = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-2", "SQL", "SKILL", "SQL", "SKL-02"),
        create_feature("FEAT-SK-3", "AWS", "SKILL", "AWS", "SKL-03"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Developer",
            "EXPERIENCE",
            {"company": "Google", "job_title": "Developer", "duration_months": 60, "experience_id": "EXP-01"},
            "EXP-01",
        )
    ],
    education=[
        create_feature(
            "FEAT-ED-1",
            "B.Tech",
            "EDUCATION",
            {"institution": "IIT", "degree": "B.Tech", "major": "CS", "education_id": "EDU-01"},
            "EDU-01",
        )
    ],
    projects=[
        create_feature(
            "FEAT-PR-1",
            "Inventory Management System",
            "PROJECT",
            {"project_name": "Inventory Management System", "role": "Lead", "project_id": "PRJ-01"},
            "PRJ-01",
        )
    ],
    certifications=[
        create_feature(
            "FEAT-CR-1",
            "AWS Certified Developer",
            "CERTIFICATION",
            {"certification_name": "AWS Certified Developer", "issuing_organization": "Amazon", "certification_id": "CRT-01"},
            "CRT-01",
        )
    ],
)

# 2. Simple Job (Python, SQL, AWS, 3+ Years Exp, Bachelor Degree Education, AWS Developer Certification, Inventory System Project)
job_simple = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-2", "SQL", "SKILL", "SQL", "SKL-02"),
        create_feature("FEAT-SK-3", "AWS", "SKILL", "AWS", "SKL-03"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Developer",
            "EXPERIENCE",
            {"company": "Google", "job_title": "Developer", "duration_months": 36, "experience_id": "EXP-01"},
            "EXP-01",
        )
    ],
    education=[
        create_feature(
            "FEAT-ED-1",
            "Bachelor Degree",
            "EDUCATION",
            {"institution": "IIT", "degree": "Bachelor Degree", "major": "CS", "education_id": "EDU-01"},
            "EDU-01",
        )
    ],
    projects=[
        create_feature(
            "FEAT-PR-1",
            "Inventory Management System",
            "PROJECT",
            {"project_name": "Inventory Management System", "role": "Lead", "project_id": "PRJ-01"},
            "PRJ-01",
        )
    ],
    certifications=[
        create_feature(
            "FEAT-CR-1",
            "AWS Certified Developer",
            "CERTIFICATION",
            {"certification_name": "AWS Certified Developer", "issuing_organization": "Amazon", "certification_id": "CRT-01"},
            "CRT-01",
        )
    ],
)

# 3. Complex Resume
res_complex = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-2", "SQL", "SKILL", "SQL", "SKL-02"),
        create_feature("FEAT-SK-3", "C++", "SKILL", "C++", "SKL-04"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Lead Engineer",
            "EXPERIENCE",
            {"company": "Meta", "job_title": "Lead Engineer", "duration_months": 48, "experience_id": "EXP-02"},
            "EXP-02",
        )
    ],
    education=[
        create_feature(
            "FEAT-ED-1",
            "M.S.",
            "EDUCATION",
            {"institution": "MIT", "degree": "M.S.", "major": "EECS", "education_id": "EDU-02"},
            "EDU-02",
        )
    ],
    projects=[
        create_feature(
            "FEAT-PR-1",
            "Distributed Key-Value Store",
            "PROJECT",
            {"project_name": "Distributed Key-Value Store", "role": "Architect", "project_id": "PRJ-02"},
            "PRJ-02",
        )
    ],
    certifications=[
        create_feature(
            "FEAT-CR-1",
            "CKA",
            "CERTIFICATION",
            {"certification_name": "CKA", "issuing_organization": "CNCF", "certification_id": "CRT-02"},
            "CRT-02",
        )
    ],
)

# 4. Complex Job
job_complex = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-2", "SQL", "SKILL", "SQL", "SKL-02"),
        create_feature("FEAT-SK-3", "C++", "SKILL", "C++", "SKL-04"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Lead Engineer",
            "EXPERIENCE",
            {"company": "Meta", "job_title": "Lead Engineer", "duration_months": 24, "experience_id": "EXP-02"},
            "EXP-02",
        )
    ],
    education=[
        create_feature(
            "FEAT-ED-1",
            "M.S.",
            "EDUCATION",
            {"institution": "MIT", "degree": "M.S.", "major": "EECS", "education_id": "EDU-02"},
            "EDU-02",
        )
    ],
    projects=[
        create_feature(
            "FEAT-PR-1",
            "Distributed Key-Value Store",
            "PROJECT",
            {"project_name": "Distributed Key-Value Store", "role": "Architect", "project_id": "PRJ-02"},
            "PRJ-02",
        )
    ],
    certifications=[
        create_feature(
            "FEAT-CR-1",
            "CKA",
            "CERTIFICATION",
            {"certification_name": "CKA", "issuing_organization": "CNCF", "certification_id": "CRT-02"},
            "CRT-02",
        )
    ],
)

# 5. Large Resume (500 skills, 100 certifications, 100 projects, 50 education, 100 experience entries)
large_skills = [create_feature(f"FEAT-SK-{i}", f"Skill {i}", "SKILL", f"Skill {i}", f"SKL-{i}") for i in range(500)]
large_experience = [
    create_feature(
        f"FEAT-EX-{i}",
        f"Role {i}",
        "EXPERIENCE",
        {"company": f"Company {i}", "job_title": f"Role {i}", "duration_months": 12, "experience_id": f"EXP-{i}"},
        f"EXP-{i}",
    )
    for i in range(100)
]
large_education = [
    create_feature(
        f"FEAT-ED-{i}",
        f"Degree {i}",
        "EDUCATION",
        {"institution": f"University {i}", "degree": f"Degree {i}", "major": f"Major {i}", "education_id": f"EDU-{i}"},
        f"EDU-{i}",
    )
    for i in range(50)
]
large_projects = [
    create_feature(
        f"FEAT-PR-{i}",
        f"Project {i}",
        "PROJECT",
        {"project_name": f"Project {i}", "role": f"Role {i}", "project_id": f"PRJ-{i}"},
        f"PRJ-{i}",
    )
    for i in range(100)
]
large_certifications = [
    create_feature(
        f"FEAT-CR-{i}",
        f"Cert {i}",
        "CERTIFICATION",
        {"certification_name": f"Cert {i}", "issuing_organization": f"Org {i}", "certification_id": f"CRT-{i}"},
        f"CRT-{i}",
    )
    for i in range(100)
]

res_large = create_canonical_collection(
    skills=large_skills,
    experience=large_experience,
    education=large_education,
    projects=large_projects,
    certifications=large_certifications,
)
job_large = create_canonical_collection(
    skills=large_skills,
    experience=large_experience,
    education=large_education,
    projects=large_projects,
    certifications=large_certifications,
)

# 6. Duplicates
res_duplicates = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-1-dup", "Python", "SKILL", "Python", "SKL-01"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Developer",
            "EXPERIENCE",
            {"company": "Google", "job_title": "Developer", "duration_months": 60, "experience_id": "EXP-01"},
            "EXP-01",
        )
    ],
    education=[],
    projects=[],
    certifications=[],
)
job_duplicates = create_canonical_collection(
    skills=[
        create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
        create_feature("FEAT-SK-1-dup2", "Python", "SKILL", "Python", "SKL-01"),
    ],
    experience=[
        create_feature(
            "FEAT-EX-1",
            "Developer",
            "EXPERIENCE",
            {"company": "Google", "job_title": "Developer", "duration_months": 60, "experience_id": "EXP-01"},
            "EXP-01",
        )
    ],
    education=[],
    projects=[],
    certifications=[],
)

# 7. Empty
res_empty = create_canonical_collection()
job_empty = create_canonical_collection()


# Helper to write
def save_fixture(name: str, data: dict):
    with open(fixtures_dir / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


save_fixture("resume_simple.json", res_simple)
save_fixture("resume_complex.json", res_complex)
save_fixture("resume_large.json", res_large)
save_fixture("resume_duplicates.json", res_duplicates)
save_fixture("resume_empty.json", res_empty)

save_fixture("job_simple.json", job_simple)
save_fixture("job_complex.json", job_complex)
save_fixture("job_large.json", job_large)
save_fixture("job_duplicates.json", job_duplicates)
save_fixture("job_empty.json", job_empty)

print("Test fixtures successfully generated in tests/fixtures/")
