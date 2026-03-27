# gRPC Inference Example

This example demonstrates propact's ability to send inference requests to gRPC-based ML models.

## Image for Inference

![medical.jpg](medical.jpg)

```protobuf
service InferenceService {
  rpc AnalyzeImage(ImageRequest) returns (AnalysisResponse);
}

message ImageRequest {
  bytes image_data = 1;
  string model_name = 2;
  map<string, string> parameters = 3;
}

message AnalysisResponse {
  repeated Detection detections = 1;
  float confidence_score = 2;
  int64 processing_time_ms = 3;
}

message Detection {
  string class_name = 1;
  float confidence = 2;
  BoundingBox bbox = 3;
}

message BoundingBox {
  float x_min = 1;
  float y_min = 2;
  float x_max = 3;
  float y_max = 4;
}
```

```yaml
# Inference parameters
model_name: "medical_vision_resnet50"
parameters:
  confidence_threshold: 0.7
  max_detections: 10
  input_size: [512, 512]
  normalize: true
```

Additional context: This is a medical image analysis request for detecting anomalies. The model should identify potential issues with confidence scores above 70%.

## Expected Behavior

Propact will:
1. Extract the image and protobuf schema
2. Convert to gRPC request format
3. Send to inference service
4. Parse protobuf response to markdown

## Run Command

```bash
propact README.md --endpoint "grpc://localhost:50051/InferenceService/AnalyzeImage" --schema inference.proto
```

## gRPC Schema

The inference service expects:
- protobuf service definition
- Image data as bytes
- Model parameters as key-value pairs
- Returns structured detection results
