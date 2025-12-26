# n8n Local AI Workflow – Automated ESG Data Scraping & Dataset Builder

[![n8n](https://img.shields.io/badge/n8n-v1.x-41A2E6?style=flat&logo=n8n&logoColor=white)](https://n8n.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=flat&logo=selenium&logoColor=white)](https://selenium.dev)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)

## Project Overview

This project is a **fully automated data pipeline** built with **n8n** (self-hosted) that collects ESG (Environmental, Social, Governance) data for multiple companies at scale.

### How it works:
1. **Input via Telegram Bot** – Users send company names (one or more) through a Telegram bot.
2. **Intelligent Data Scraping** – For each company, the workflow searches the **LSEG (London Stock Exchange Group)** website to find the official ESG profile and annual reports.
3. **Dynamic Report Extraction** – Uses **Selenium** in headless mode to navigate, handle JavaScript-heavy pages, locate the correct yearly ESG report PDF/HTML, and extract relevant metadata and content.
4. **Data Validation & Deduplication** – Checks for duplicates, validates data quality, and enriches the dataset.
5. **Dataset Aggregation** – Appends clean, structured ESG data to a master dataset (CSV/JSON) for downstream analysis or model training.

The entire process runs **headlessly and unattended**, making it perfect for periodic data collection or integration into larger AI/ML pipelines.

Workflow Preview

<img width="1599" height="290" alt="Screenshot 2025-12-26 at 2 25 27 PM" src="https://github.com/user-attachments/assets/09bfd0c6-c73e-42fc-b523-531179293d5f" />


<!-- Replace with your actual screenshot of the n8n workflow or output -->

## Key Features
- Fully automated end-to-end ESG data collection
- Telegram-triggered execution (easy for non-technical users)
- Robust web scraping with Selenium for dynamic/SPA websites
- Duplicate detection and data integrity checks
- Containerized setup with Docker (n8n + custom Python nodes)
- Extensible for adding more data sources or LLM-based summarization

## Tech Stack
- **n8n** – Core workflow automation (self-hosted)
- **Python 3.10+** – Custom script nodes (data processing, API logic)
- **Selenium WebDriver** – Headless browser automation for LSEG site
- **Docker & docker-compose** – Local deployment with isolated n8n and Python service containers
- **Telegram Node** – Input trigger
- **HTTP Request & Code Nodes** – API communication between services
- **Pandas** – Data cleaning and dataset management

## Why This Project Stands Out
- Real-world **production-grade automation** combining low-code (n8n) with custom code
- Experience with **challenging web scraping** on JavaScript-heavy financial platforms
- Strong **data pipeline engineering**: validation, deduplication, structured output
- Demonstrates **Docker-based microservices** architecture for AI workflows
- Ready foundation for adding **LLM enhancement** (e.g., ESG report summarization with Hugging Face models)

## Local Setup (Docker)
```bash
git clone https://github.com/mhkarimi78/n8n-local.git
cd n8n-local
docker-compose up -d
