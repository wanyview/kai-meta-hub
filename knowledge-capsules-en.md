# Knowledge Capsule System - The Second Brain in the AI Era

## Overview

The Knowledge Capsule System is an innovative knowledge management infrastructure designed for the AI era. It enables efficient capture, organization, storage, and application of knowledge through the "capsule" metaphor.

## Core Concepts

### What is a Knowledge Capsule?

A Knowledge Capsule is a structured, portable, and traceable unit of knowledge that contains:
- **Core Content**: The essential knowledge itself
- **Metadata**: Source, author, creation time, tags
- **Evolution History**: Track of how the knowledge evolved
- **Quality Score**: DATM-based evaluation (Decentralized Autonomous Trust Mechanism)

### Key Features

1. **Content Addressability**: Each capsule has a unique SHA256 asset_id ensuring content integrity
2. **Verification Scoring**: DATM score ≥ 0.7 automatically promotes capsules
3. **Evolution Tracking**: Records the entire creation and evolution process
4. **Gene Strategy Binding**: Strategy templates linked to capsules
5. **Version Control**: Supports iteration and parent tracing

## Technical Architecture

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /capsule/create | POST | Create new capsule |
| /capsule/get/:id | GET | Retrieve capsule |
| /capsule/search | POST | Search capsules |
| /capsule/evolve | POST | Create evolution |

### Data Model

```json
{
  "asset_id": "sha256-hash",
  "content": "knowledge-content",
  "metadata": {
    "author": "creator-id",
    "timestamp": "ISO-8601",
    "tags": ["tag1", "tag2"]
  },
  "outcome": {
    "score": 0.85,
    "validators": 5
  }
}
```

## Applications

- Personal knowledge management
- Team knowledge sharing
- Cross-domain knowledge connection
- AI-powered knowledge discovery

## Repository

- GitHub: https://github.com/wanyview/kai-capsule-service-v2
- Service Port: 8005
