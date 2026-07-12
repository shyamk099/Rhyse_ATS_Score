"""Pattern-based contact candidate builder.

Purpose:
    Perform deterministic regular expression scanning to discover candidate matches
    for email, phone, and links in raw segment texts.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.entity_extraction.contact.contact_candidate import ContactCandidate
from ats_engine.domain.entity_extraction.contact.contact_rules import ContactExtractionRules
from ats_engine.domain.entity_extraction.contact.exceptions import PatternConfigurationError


class PatternCandidateBuilder:
    """Stateless builder compiling candidate matches from segment texts using regular expressions."""

    @classmethod
    def find_candidates(
        cls, text: str, rules: ContactExtractionRules
    ) -> Sequence[ContactCandidate]:
        """Scan target text and collect matches for active contact patterns.

        Args:
            text: Normalized text segment.
            rules: The rules parameter mapping patterns.

        Returns:
            A sequence of discovered ContactCandidates.

        Raises:
            PatternConfigurationError: If any configured regex pattern fails to compile.
        """
        candidates: list[ContactCandidate] = []

        try:
            email_re = re.compile(rules.email_pattern)
            phone_re = re.compile(rules.phone_pattern)
            linkedin_re = re.compile(rules.linkedin_pattern)
            github_re = re.compile(rules.github_pattern)
            portfolio_re = re.compile(rules.portfolio_pattern)
        except re.error as error:
            raise PatternConfigurationError(f"Invalid contact regex pattern config: {error}") from error

        # 1. Email Matches
        for match in email_re.finditer(text):
            candidates.append(
                ContactCandidate(
                    value=match.group(0),
                    entity_type="email",
                    start_char=match.start(),
                    end_char=match.end(),
                )
            )

        # 2. Phone Matches
        for match in phone_re.finditer(text):
            candidates.append(
                ContactCandidate(
                    value=match.group(0),
                    entity_type="phone",
                    start_char=match.start(),
                    end_char=match.end(),
                )
            )

        # 3. LinkedIn Matches
        for match in linkedin_re.finditer(text):
            candidates.append(
                ContactCandidate(
                    value=match.group(0),
                    entity_type="linkedin",
                    start_char=match.start(),
                    end_char=match.end(),
                )
            )

        # 4. GitHub Matches
        for match in github_re.finditer(text):
            candidates.append(
                ContactCandidate(
                    value=match.group(0),
                    entity_type="github",
                    start_char=match.start(),
                    end_char=match.end(),
                )
            )

        # 5. Portfolio Matches (filter out spans already claimed by email, linkedin, or github)
        claimed_spans = [
            (c.start_char, c.end_char)
            for c in candidates
            if c.entity_type in ("email", "linkedin", "github")
        ]

        for match in portfolio_re.finditer(text):
            start, end = match.start(), match.end()
            
            # Check overlap against claimed spans
            overlap = False
            for c_start, c_end in claimed_spans:
                if not (end <= c_start or start >= c_end):
                    overlap = True
                    break

            if not overlap:
                candidates.append(
                    ContactCandidate(
                        value=match.group(0),
                        entity_type="portfolio",
                        start_char=start,
                        end_char=end,
                    )
                )

        return candidates
