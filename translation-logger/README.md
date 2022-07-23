# Translation logger

## Idea
We use a dictionary on daily basis in search for the meaning of the words we don't know. Once we satistfy the need to understand the phrase we are reading we immediately forget the word. 

I often find myself translating the same word over and over again, it's irritating.

The idea is to capture the fact of translation and automatically log translated words and repeat them using the spaced repetition technique.

## Solution

This is a wrapper around the [Translate Shell](https://github.com/soimort/translate-shell) command. It keeps a log of words I translated.
I'll decide what to do with them later.

## Build

Install command locally:
```bash
pip install .
```

## References

- [How to make installable python CLI](https://betterprogramming.pub/build-your-python-script-into-a-command-line-tool-f0817e7cebda)