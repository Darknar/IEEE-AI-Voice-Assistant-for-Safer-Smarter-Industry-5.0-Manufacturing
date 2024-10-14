# AI Voice Assistant for Industry 5.0 Manufacturing Environment

## Project Overview

This project showcases the development and implementation of an advanced AI-powered voice assistant designed for use in an Industry 5.0 manufacturing environment, specifically a window production line. The assistant enhances operational efficiency, improves access to real-time data, and facilitates hands-free interaction for operators.

## Table of Contents

1. [Features](#features)
2. [System Architecture](#system-architecture)
3. [Implementation](#implementation)
4. [Performance Results](#performance-results)
5. [Future Improvements](#future-improvements)

## Features

- **Natural Language Processing**: Utilizes OpenAI's GPT models for advanced language understanding and generation.
- **Speech Recognition**: Converts spoken commands into text for processing.
- **Text-to-Speech Synthesis**: Provides auditory feedback, ideal for hands-free operation.
- **Real-time Data Access**: Connects to production line systems for immediate information retrieval.
- **Hands-free Operation**: Allows operators to interact with the system while performing tasks.
- **Adaptive Learning**: Quickly adapts to new manuals and technical documentation.

## System Architecture

The voice assistant is built on a modular architecture:

![System Architecture](img/RelacionModulos.png)

1. **Input/Output Module (EyS.py)**: Handles real-time operational data capture and storage.
2. **Text Generation Module (ChatGPT.py)**: Manages communication with OpenAI's API.
3. **Voice Synthesis Module (sintesis.py)**: Converts text to speech using GTTS or ChatGPT API.
4. **Speech Recognition Module (reconocimiento.py)**: Converts audio input to text.

The system uses industrial protocols like OPC UA and MQTT with Sparkplug for interoperability and security. The voice assistant is designed to be scalable and adaptable to different manufacturing environments.

![System Architecture](img/Programa.png)

## Implementation

1. **Network Infrastructure**: Utilizes existing Schirmer production line network, supporting real-time communication.
2. **User Interface**: Custom-designed GUI with a chat-style dialog box for efficient operator interaction.
3. **Voice Activation**: Implements a wake word to distinguish between actual commands and background noise.
4. **Cloud Integration**: Leverages cloud technologies for efficient processing of large data volumes.

## Performance Results

Performance evaluation across various conditions:

| Condition | Accuracy (%) | Processing Time (s) |
|-----------|--------------|---------------------|
| Neutral Accent | 98.6 - 100.0 | 1.031 - 1.216 |
| Fast Speech | 88.2 - 100.0 | 0.935 - 1.436 |
| Normal Speech | 98.6 - 100.0 | 1.399 - 1.698 |
| Slow Speech | 88.6 - 100.0 | 0.936 - 1.497 |
| Low Background Noise | 98.6 - 100.0 | 0.809 - 1.458 |
| Medium Background Noise | 98.6 - 100.0 | 0.894 - 1.668 |
| High Background Noise | 93.2 - 97.6 | 1.019 - 1.704 |
| Simple Instructions | 98.6 - 100.0 | 0.492 - 0.869 |
| Complex Instructions | 97.2 - 97.4 | 1.864 - 2.404 |
| Interruptions | 93.6 | 1.648 |
| Tone Variation | 92.6 | 2.029 |

User satisfaction results:
- Satisfaction with the virtual assistant: 9.22/10
- Correct response generation rate: 7.62/10
- Ease of use: 7.34/10

## Future Improvements

1. Enhance noise cancellation for better performance in high-noise environments.
2. Implement more advanced natural language understanding for complex queries.
3. Integrate with wearable devices for improved hands-free operation.
4. Develop industry-specific language models for more accurate responses.
5. Implement multi-language support for diverse workforce environments.

---

For more detailed information or to contribute to this project, please contact the development team.
