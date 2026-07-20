# Prioritization Engine Architecture

The prioritization engine acts as a pipeline post-processor executed after all recommendation providers complete their run.

## Components
- **`PriorityKey`**: Immutable key wrapping `section` and `category` fields for robust lookup.
- **`PriorityProfile`**: Value DTO holding `priority`, `impact`, and `confidence` parameters.
- **`PrioritizationRules`**: Registry mapping keys to profiles and holding high/medium/low priority threshold bounds.
- **`PrioritizationBuilder`**: Copies recommendations, stamps profiles, and sorts them.
- **`PrioritizationValidator`**: Enforces range constraints and asserts sorted sequence correctness.
- **`PrioritizationStatisticsBuilder`**: Compiles metric counts and averages into the typed `PrioritizationStatistics` DTO.
