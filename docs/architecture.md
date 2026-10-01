# Architecture

```text
capture → detect → track → OCR → validate → store
```

`capture` reads a camera, file, or stream. `detection` finds plate boxes. `tracking` keeps one identity per vehicle so OCR does not run on every frame. `recognition` reads and checks the text. `storage` logs the read and saves the crop.
