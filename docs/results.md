# Results

The fine-tuned detector is `models/plate_detector.pt`, copied from `runs/detect/plate_yolo11n-3/weights/best.pt`.

Epoch metrics are in `runs/detect/plate_yolo11n-3/results.csv`. The best logged mAP50 was 0.944 (epoch 41). The best logged mAP50-95 was 0.519 (epoch 33).

That run detects plates. It does not read the characters. OCR accuracy is not measured yet.
