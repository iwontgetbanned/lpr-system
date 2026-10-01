# Dataset

Plate boxes live in `data/processed`.

- `images/train` and `labels/train` are the training images.
- `images/test` and `labels/test` are the held-out images. Training used this split as validation.
- `images/val` and `labels/val` are reserved and currently empty.

Each label file matches an image name. A line is `class x_center y_center width height`, with class `0` for `license_plate`. Coordinates are normalized between 0 and 1.

Demo videos and photos are in `data/samples`.
