# Process Model

**Chosen Model:** Incremental Model

## Rationale
The Incremental Model was chosen for the development of PixelAlchemy because the application is composed of several semi-independent modules (Canvas, Filters, Color Theory, Generative Patterns, Gallery) that all share a common shell and database. Building the app incrementally allows for:
1. **Early Usability**: We could use the Canvas module before the Generative Patterns were even started.
2. **Reduced Risk**: By tackling one major feature set per increment, integration issues are localized.
3. **Structured Focus**: It is easier to validate the dark UI aesthetic and SQLite logic on a single feature first (Increment 1) and carry those patterns forward.

## Increments
- **Increment 1**: Core Canvas + Drawing Tools
- **Increment 2**: Filters Lab
- **Increment 3**: Color Theory Panel
- **Increment 4**: Generative Patterns
- **Increment 5**: Gallery + SQLite integration
