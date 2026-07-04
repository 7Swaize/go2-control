from dataclasses import dataclass


@dataclass(frozen=True)
class OCRConfig:
    """Immutable configuration for OCR extraction."""

    #: Tesseract CLI configuration string, passed directly to pytesseract as
    #: the ``config`` argument (e.g. OCR engine mode and page segmentation mode flags).
    #:
    #: The default value sets three things:
    #:   - ``--oem 1``: OCR Engine Mode 1, which uses the LSTM neural-network-based recognizer only.
    #:   - ``--psm 11``: Page Segmentation Mode 11 ("sparse text"), which tells Tesseract
    #:     to find as much text as possible without assuming any particular layout or reading order.
    #:   - ``-c tessedit_char_whitelist="..."``: Restricts recognition to uppercase and
    #:     lowercase ASCII letters, digits 0-9, and the space character. Any other
    #:     character (punctuation, symbols, non-ASCII text) will not be recognized/output,
    #:     which reduces noise at the cost of not being able to read
    #:     text containing those excluded characters.
    cli_command: str = r'--oem 1 --psm 11 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "'

    #: Minimum per-word confidence (0-100) required for a detected word to be
    #: included in extracted text output. Words below this threshold are treated as noise and discarded.
    min_conf: int = 70

    #: Minimum number of occurrences (votes) required across a sequence of frames for a word to be retained.
    temporal_voting_threshold: int = 3