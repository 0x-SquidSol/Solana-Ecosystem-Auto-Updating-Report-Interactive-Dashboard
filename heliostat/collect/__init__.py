"""Data collectors.

Each module exposes ``collect(...)`` returning the shared envelope shape
(:func:`heliostat.util.ok_envelope` / :func:`heliostat.util.error_envelope`)
so that one failed source can never take down the whole report.
"""
