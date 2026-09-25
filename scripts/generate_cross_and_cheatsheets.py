#!/usr/bin/env python3
"""
generate_cross_and_cheatsheets.py - Generates Topics 051 to 060 covering:
- Cross-Cutting Data, Analytics & ML (051 to 054)
- Service Decision Cheat Sheets & Key Numbers (055 to 060)
Completes the entire 60-topic GCP Architect Roadmap.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

FINAL_TOPICS = [
    # 051: Data Warehousing and Analytics: BigQuery & Looker
    {
        "topic_no": "051",
        "roadmap_id": "D.1",
        "title": "Data Warehousing: BigQuery Architecture & Looker Studio",
        "page_type": "service",
        "phase": "Data, Analytics & ML (Cross-Cutting)",
        "lead": "Serverless petabyte-scale analytics: Separation of compute (Dremel) and storage (Capacitor), table partitioning and clustering, BigQuery BI Engine, authorized views, and Looker Studio dashboards.",
        "comp1": ("Raw Data Sources", "Batch Files & Streams", "data", "Delivers petabytes of clickstream logs, transactional dumps, and IoT feeds."),
        "comp2": ("BigQuery Storage API", "Capacitor Storage", "data", "Encrypted, columnar storage engine separated completely from compute queries."),
        "comp3": ("Dremel Query Engine", "Serverless Dynamic Slots", "control", "Multi-tenant query engine executing ANSI SQL queries across thousands of CPU workers."),
        "comp4": ("Looker Studio & BI Engine", "In-Memory Acceleration", "control", "Sub-second analytical dashboards caching high-frequency queries in memory."),
        "flow1": "Application streams records into BigQuery using the Storage Write API.",
        "flow2": "Dremel allocates dynamic slots to run columnar aggregations over partitioned tables.",
        "flow3": "BI Engine caches frequently queried aggregations in memory, powering instant Looker Studio dashboards.",
        "fail": "A user runs an unpartitioned <code>SELECT *</code> query over a 50 TB table, scanning massive bytes and incurring high cost.",
        "heal": "Architect enforces mandatory table partitioning filters, reducing scanned bytes from 50 TB to 1.2 GB.",
        "city_concept": "City Grand Library & Sorting Scribes",
        "p1": "Scholars were searching for tax scrolls stored in giant unlabelled heaps, taking 3 weeks to answer how much grain the city consumed in March.",
        "p2": "Head Librarian Arthur organized scrolls into annual halls (Partitioning) and indexed them by merchant guild (Clustering).",
        "p3": "Arthur hired quick scribes (Dremel Slots) who read only the March 1880 shelf, returning the exact grain total in 10 seconds.",
        "p4": "Paper libraries cannot replicate scrolls; BigQuery separates compute from storage, allowing 1,000 queries over the same data simultaneously.",
        "part1_html": """
        <h3>The Situation: The Power of Compute-Storage Separation</h3>
        <p>
          Traditional enterprise data warehouses require buying physical appliances or dedicated clusters where compute and storage are tightly coupled. If you run out of disk space, you must buy more CPU nodes. If a heavy query runs at 09:00, all other analytical queries grind to a halt.
        </p>
        <p>
          <strong>Google BigQuery</strong> revolutionized data warehousing by completely separating compute (the <strong>Dremel</strong> query engine) from storage (the <strong>Capacitor</strong> columnar filesystem) connected over Google's ultra-high-bandwidth <strong>Jupiter</strong> network fabric (terabits per second).
        </p>
        <div class="callout">
          <div class="callout-title">BigQuery Core Performance Optimizations</div>
          <ul>
            <li><strong>Partitioning:</strong> Slices large tables into segments based on ingestion date, timestamp column, or integer range. Queries with date filters scan only the relevant partition, drastically reducing scanned bytes and query cost.</li>
            <li><strong>Clustering:</strong> Sorts data within each partition based on up to 4 columns (e.g. <code>customer_id</code>, <code>country</code>). Accelerates queries using <code>WHERE</code> filters and <code>GROUP BY</code> clauses through block pruning.</li>
            <li><strong>BI Engine:</strong> An in-memory analysis service that caches query results and tables in RAM, reducing dashboard load times from seconds to sub-100ms.</li>
            <li><strong>Pricing Models:</strong> On-Demand ($6.25 per TB scanned) vs Capacity / Editions (Standard, Enterprise, Enterprise Plus with dedicated slot commitments).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Avoiding the "SELECT *" Anti-Pattern</h4>
        <p>In a columnar database like BigQuery, cost and performance are determined by the columns scanned, not the number of rows. Querying <code>SELECT *</code> scans every column on disk. Always select only the required fields: <code>SELECT order_id, amount FROM orders</code>.</p>
        <h4>Layer 2 — Practitioner: Partitioning vs Clustering Decision Rules</h4>
        <p>Partition on date/timestamp columns when queries frequently filter on time windows. Cluster on high-cardinality columns (like user ID or status code) that are frequently filtered or aggregated.</p>
        <h4>Layer 3 — Architect: Column-Level & Row-Level Security</h4>
        <p>Use <strong>Policy Tags</strong> (Data Catalog / Dataplex) to mask or restrict sensitive columns (e.g., credit cards) to specific IAM groups. Use <strong>Authorized Views</strong> or <strong>Authorized Datasets</strong> to share aggregated data with external partners without exposing the underlying raw tables.</p>
        <h4>Layer 4 — Staff: BigLake & Multi-Cloud Lakehouse</h4>
        <p>Staff architects deploy <strong>BigLake</strong>: query open table formats (Parquet, ORC, Iceberg, Delta Lake) stored in Cloud Storage, AWS S3, or Azure Blob Storage directly using BigQuery ANSI SQL while enforcing uniform column-level security.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Arthur's organized library shelves allow scholars to pull exact records in seconds without rummaging through dusty vaults.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Partitioned & Clustered Table in BigQuery</div>
          <p>Declare an optimized table partitioned by transaction date and clustered by customer ID.</p>
        </div>
        <pre><code class="language-sql">CREATE OR REPLACE TABLE `brightloaf-analytics.retail.orders_optimized`
(
  order_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  order_timestamp TIMESTAMP NOT NULL,
  total_amount NUMERIC,
  order_status STRING
)
PARTITION BY DATE(order_timestamp)
CLUSTER BY customer_id, order_status
OPTIONS (
  description = "Optimized retail orders table with date partitioning and customer clustering",
  require_partition_filter = TRUE
);</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: BigQuery Optimization (Question 1)</span>
          <p><strong>A financial analyst runs daily BigQuery queries against a 200 TB transactions table to examine transactions for a single corporate customer over the last 7 days. Under on-demand pricing, each query costs over $1,000. How should the architect optimize the table to reduce query costs by over 99%?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Partitioning by transaction date ensures only 7 days of data are scanned instead of 200 TB, and clustering by customer_id prunes irrelevant data blocks, reducing scanned bytes and cost by over 99%.')">A) Partition the table by transaction date and cluster by customer_id, and enforce partition filters in queries.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Exporting to CSV does not optimize BigQuery SQL queries and adds high storage/network overhead.')">B) Export the 200 TB table to CSV files in Cloud Storage every morning.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Increasing slot count accelerates query execution speed under capacity pricing, but does not reduce the bytes scanned on on-demand pricing.')">C) Increase the maximum slot reservation limit to 2,000 slots.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Materialized views require base table scanning and cannot replace proper physical partitioning.')">D) Replace the table with an unpartitioned BigQuery external table pointing to Google Drive.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/bigquery/docs/partitioned-tables' target='_blank'>BigQuery Partitioned Tables Guide</a></li><li><a href='https://cloud.google.com/bigquery/docs/clustered-tables' target='_blank'>BigQuery Clustered Tables Guide</a></li></ul>"
    },

    # 052: Data Processing: Dataflow, Dataproc, Composer & Pub/Sub
    {
        "topic_no": "052",
        "roadmap_id": "D.2",
        "title": "Data Processing: Dataflow (Beam), Dataproc & Cloud Composer",
        "page_type": "service",
        "phase": "Data, Analytics & ML (Cross-Cutting)",
        "lead": "Unified batch and stream pipelines: Apache Beam on Dataflow, managed Hadoop/Spark with Dataproc, Change Data Capture with Datastream, and workflow orchestration via Cloud Composer (Airflow).",
        "comp1": ("Streaming Ingestion", "Cloud Pub/Sub", "data", "Decouples millions of real-time event messages per second from distributed producers."),
        "comp2": ("Stream & Batch Engine", "Cloud Dataflow (Beam)", "control", "Executes autoscaling data transformations with windowing, watermarks, and exactly-once processing."),
        "comp3": ("Managed Spark/Hadoop", "Cloud Dataproc", "data", "Runs legacy Spark/Hadoop/Hive workloads with ephemeral clusters and Spot VM worker nodes."),
        "comp4": ("Workflow Orchestrator", "Cloud Composer (Airflow)", "control", "Coordinates multi-step DAG workflows, managing dependencies across data pipelines."),
        "flow1": "IoT telemetry streams into Cloud Pub/Sub topics at 50,000 messages per second.",
        "flow2": "Dataflow pipeline applies 5-minute tumbling windows, calculates average metrics, and writes to BigQuery.",
        "flow3": "Cloud Composer triggers overnight Dataproc Spark job to run heavy machine learning feature extraction.",
        "fail": "Late-arriving sensor messages arrive 15 minutes after window closure due to mobile network dropouts.",
        "heal": "Apache Beam watermarks and allowed lateness side-outputs capture late data into a reconciliation table.",
        "city_concept": "City Water Treatment Plant & Filtration Sluices",
        "p1": "Muddy river water was pouring into city taps because the water department had no filtration sluices to separate silt, leaves, and clean water.",
        "p2": "Hydraulic Engineer Hugh designed tiered filtration basins (Dataflow): fast settling pools for continuous flow (Streaming) and overnight settling tanks (Batch).",
        "p3": "When storm runoff brought heavy debris late at night, automated overflow sluices (Allowed Lateness) routed silt to secondary holding basins.",
        "p4": "Physical water filters clog with sand; software pipelines scale compute workers dynamically to process gigabytes of data per second.",
        "part1_html": """
        <h3>The Situation: Batch vs Streaming Convergence</h3>
        <p>
          Traditionally, data engineering required maintaining two completely separate architectures (the "Lambda Architecture"): one batch pipeline running overnight MapReduce/Hadoop jobs, and a separate streaming pipeline running Storm or Flink. Maintaining two codebases for identical business logic was error-prone and expensive.
        </p>
        <p>
          Google unified batch and streaming with the <strong>Apache Beam</strong> model, executed in production on <strong>Cloud Dataflow</strong>. The exact same pipeline code can process bounded historical files (batch) or unbounded event streams (real-time).
        </p>
        <div class="callout">
          <div class="callout-title">GCP Data Processing Services Compared</div>
          <ul>
            <li><strong>Cloud Dataflow:</strong> Serverless stream and batch processing powered by Apache Beam. Automates worker provisioning, autoscaling, dynamic work rebalancing, and exactly-once processing.</li>
            <li><strong>Cloud Dataproc:</strong> Fully managed Apache Spark, Hadoop, Hive, and Presto clusters. Ideal for migrating existing open-source big data workloads to the cloud in minutes. Supports ephemeral clusters and Spot VM workers.</li>
            <li><strong>Cloud Composer:</strong> Managed Apache Airflow for complex workflow orchestration. Authors workflows as Directed Acyclic Graphs (DAGs) in Python.</li>
            <li><strong>Datastream:</strong> Serverless Change Data Capture (CDC) replicating database changes from Oracle, MySQL, and PostgreSQL into BigQuery or Cloud Storage in real time.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Apache Beam Concepts (Windowing & Watermarks)</h4>
        <p>Understand the 4 questions of stream processing: <strong>What</strong> is being computed? (Transformations); <strong>Where</strong> in event time? (Fixed, Sliding, or Session Windows); <strong>When</strong> in processing time? (Watermarks and Triggers); <strong>How</strong> do results relate? (Accumulating or Retracting).</p>
        <h4>Layer 2 — Practitioner: Ephemeral Dataproc Clusters & Cost Optimization</h4>
        <p>Never keep Dataproc clusters running 24/7 idle. Use <strong>ephemeral clusters</strong>: Cloud Composer spins up a Dataproc cluster, submits the Spark job, waits for completion, and immediately terminates the cluster. Use 80% Spot VMs for secondary worker nodes.</p>
        <h4>Layer 3 — Architect: Exactly-Once Processing & Deduplication</h4>
        <p>Pub/Sub guarantees <em>at-least-once</em> delivery. Dataflow provides <em>exactly-once</em> processing semantics end-to-end by tracking message IDs, checkpointing state, and deduplicating records before committing to BigQuery.</p>
        <h4>Layer 4 — Staff: Enterprise Lakehouse Orchestration with Composer</h4>
        <p>Staff architects build resilient DAG workflows in Cloud Composer: orchestrating Datastream CDC ingestion, triggering Dataflow transformations, refreshing BigQuery materialized views, and triggering Vertex AI model retraining.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Hugh's automated filtration sluices purify incoming river water, directing clean drinking water to city fountains.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud Composer Environment via CLI</div>
          <p>Deploy a managed Apache Airflow 2 environment on Google Cloud.</p>
        </div>
        <pre><code class="language-bash"># Create Cloud Composer 2 environment
gcloud composer environments create production-airflow \\
    --location=us-central1 \\
    --image-version=composer-2-airflow-2.7.3 \\
    --service-account="composer-sa@my-project.iam.gserviceaccount.com" \\
    --environment-size=ENVIRONMENT_SIZE_SMALL</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Data Processing Selection (Question 1)</span>
          <p><strong>A company has an existing library of 200 production Apache Spark and PySpark jobs currently running on an expensive on-premises Hadoop cluster. They need to migrate to Google Cloud within 60 days with minimal code modification while reducing infrastructure costs. Which service should you recommend?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Dataproc provides 100% open-source Apache Spark compatibility, allowing existing PySpark jobs to run with zero code rewrite, utilizing ephemeral clusters with Spot VMs for maximum cost savings.')">A) Cloud Dataproc using ephemeral clusters with Spot VM worker nodes and Cloud Storage as the persistent storage layer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Rewriting 200 Spark jobs into Apache Beam for Dataflow would take months and violates the 60-day deadline.')">B) Rewrite all 200 Spark jobs into Apache Beam to run on Cloud Dataflow.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'BigQuery is an analytical data warehouse, not a drop-in runtime for existing Spark scripts.')">C) Convert all Spark jobs into BigQuery SQL stored procedures.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Functions has execution timeouts and memory limits unsuitable for heavy distributed Spark processing.')">D) Deploy Spark jobs as Cloud Functions.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/dataflow/docs' target='_blank'>Cloud Dataflow Documentation</a></li><li><a href='https://cloud.google.com/dataproc/docs' target='_blank'>Cloud Dataproc Documentation</a></li></ul>"
    },

    # 053: Data Lake, Lakehouse & Storage Patterns
    {
        "topic_no": "053",
        "roadmap_id": "D.3",
        "title": "Data Lake, Lakehouse & BigLake: Open Table Formats & Governance",
        "page_type": "service",
        "phase": "Data, Analytics & ML (Cross-Cutting)",
        "lead": "Architecting the enterprise lakehouse: Cloud Storage tiered storage zones (raw, curated, consumption), open formats (Parquet, ORC, Iceberg), BigLake storage abstraction, and Dataplex unified data governance.",
        "comp1": ("Raw Data Landings", "GCS Raw Zone", "data", "Ingests raw, immutable JSON/CSV logs with 30-day lifecycle retention policies."),
        "comp2": ("Dataplex Governance Fabric", "Data Catalog & Quality", "control", "Catalogs metadata, monitors data quality scores, and enforces unified IAM permissions."),
        "comp3": ("Curated Lakehouse Storage", "GCS Parquet / Iceberg", "data", "Optimized, compacted columnar open table formats partitioned by business date."),
        "comp4": ("BigLake Multi-Engine Access", "BigQuery / Spark Query", "control", "Provides fine-grained row- and column-level security across heterogeneous query engines."),
        "flow1": "Raw log files land in <code>gs://lake-raw/</code> bucket from partner API integrations.",
        "flow2": "Dataflow cleans and converts data into Apache Iceberg / Parquet format in <code>gs://lake-curated/</code>.",
        "flow3": "Dataplex registers table schema; BigQuery and Dataproc query tables via BigLake with column masking.",
        "fail": "An external data consumer attempts to query raw patient records without passing through governance masking.",
        "heal": "BigLake enforces policy tags, masking social security numbers directly at the storage access layer.",
        "city_concept": "City Granary Silos & Public Assay Scales",
        "p1": "Farmers dumped wheat, rye, and gravel into the same open city barn, making it impossible to separate feed grain from fine bakery flour.",
        "p2": "Granary Master Graham built three separated storage zones: Raw Wagons, Cleaned Silos, and Bakeshop Distribution.",
        "p3": "Graham installed assay scales (Dataplex) that checked grain moisture and marked each barrel with quality seals.",
        "p4": "Physical granary silos require manual conveyor belts; cloud lakehouses organize exabytes of data via metadata tagging.",
        "part1_html": """
        <h3>The Situation: From Data Swamp to Modern Lakehouse</h3>
        <p>
          Organizations often start their big data journey by dumping every file, log, and database export into an unorganized Cloud Storage bucket. Without governance, this quickly degenerates into an unsearchable <strong>"Data Swamp"</strong>—full of stale, duplicate, uncataloged files with zero access control.
        </p>
        <p>
          The <strong>Data Lakehouse</strong> pattern combines the low cost, flexibility, and open formats of a Cloud Storage Data Lake with the ACID transactions, data governance, and high performance of a Data Warehouse.
        </p>
        <div class="callout">
          <div class="callout-title">The Three Standard Storage Zones</div>
          <ul>
            <li><strong>Raw Zone (Bronze):</strong> Immutable, raw source data preserved in its original format (JSON, CSV, raw binary). Used for forensic re-processing.</li>
            <li><strong>Curated / Cleaned Zone (Silver):</strong> De-duplicated, schema-validated data converted into high-performance columnar formats (Parquet, ORC, Apache Iceberg).</li>
            <li><strong>Consumption / Analytics Zone (Gold):</strong> Aggregated, business-ready data models and data marts ready for executive Looker dashboards and machine learning feature stores.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Open File Formats (Parquet vs CSV/JSON)</h4>
        <p>Never query raw CSV or JSON in production analytics. <strong>Apache Parquet</strong> is a columnar format with built-in compression (Snappy) and column statistics (min/max), allowing query engines to skip irrelevant byte ranges.</p>
        <h4>Layer 2 — Practitioner: Open Table Formats (Apache Iceberg)</h4>
        <p>Traditional data lakes suffer from lack of ACID transactions (writing files during concurrent reads causes partial reads). <strong>Apache Iceberg</strong> brings ACID transactions, time travel (querying historical snapshots), and schema evolution to Cloud Storage files.</p>
        <h4>Layer 3 — Architect: BigLake Storage Engine</h4>
        <p><strong>BigLake</strong> unifies data warehouses and lakes. It extends BigQuery's storage engine to external Cloud Storage buckets, enforcing column-level and row-level access control regardless of whether the query originates from BigQuery, Spark, or TensorFlow.</p>
        <h4>Layer 4 — Staff: Dataplex Unified Data Mesh Governance</h4>
        <p>Staff architects implement <strong>Dataplex</strong> to manage data mesh architectures. Dataplex logically organizes decentralized data across multiple GCP projects into centralized "Lakes" and "Zones" with automated data quality checks and lineage tracking.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Graham inspects grain barrels in the central granary, ensuring clean separation between seed grain and bakery flour.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a BigLake External Table</div>
          <p>Create a BigLake table querying Parquet files in Cloud Storage with fine-grained access governance.</p>
        </div>
        <pre><code class="language-sql">CREATE EXTERNAL TABLE `brightloaf-analytics.retail.biglake_orders`
WITH CONNECTION `us-central1.biglake-connection`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://brightloaf-lake-curated/orders/*.parquet']
);</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Lakehouse Architecture (Question 1)</span>
          <p><strong>A global media company stores 5 PB of clickstream data in Cloud Storage as Parquet files. Both the BigQuery data analyst team and the Dataproc data science team need to query this data. Security mandates that row-level and column-level masking (PII) must be enforced across both teams without copying data. Which solution fulfills this?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! BigLake enables both BigQuery and open-source Spark/Dataproc engines to query Cloud Storage tables while centrally enforcing column-level and row-level security policies.')">A) Use BigLake tables with a cloud resource connection, applying Dataplex policy tags and row-level access policies across both BigQuery and Dataproc.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Copying 5 PB into two separate repositories doubles storage costs and introduces synchronization drift.')">B) Duplicate the 5 PB dataset: load one copy into BigQuery managed storage and keep one copy in Cloud Storage for Spark.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Object ACLs control bucket object download; they cannot enforce columnar SQL masking inside Parquet files.')">C) Rely on Cloud Storage object-level ACLs to mask columns.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Manual ETL scripts running in cron jobs fail to enforce centralized dynamic security policies.')">D) Run nightly bash scripts to replace PII values with asterisks in the raw files.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/biglake/docs' target='_blank'>Google Cloud BigLake Overview</a></li><li><a href='https://cloud.google.com/dataplex/docs' target='_blank'>Google Cloud Dataplex Data Governance</a></li></ul>"
    },

    # 054: Machine Learning & Vertex AI Architecture
    {
        "topic_no": "054",
        "roadmap_id": "D.4",
        "title": "Machine Learning: Vertex AI Architecture & MLOps Pipelines",
        "page_type": "service",
        "phase": "Data, Analytics & ML (Cross-Cutting)",
        "lead": "End-to-end cloud AI architectures: Pre-trained APIs vs AutoML vs Custom training, Vertex AI Pipelines (Kubeflow), Feature Store, Model Registry, Endpoints, and GPU vs TPU hardware selection.",
        "comp1": ("Data Science Workbench", "Vertex AI Workbench", "control", "Managed JupyterLab environment with enterprise IAM integration and GPU acceleration."),
        "comp2": ("MLOps Pipeline Engine", "Vertex AI Pipelines", "control", "Serverless orchestration of Kubeflow/TFX pipelines automating training and evaluation."),
        "comp3": ("Hardware Compute Fleet", "NVIDIA GPUs & Google TPUs", "data", "Hardware accelerators optimized for deep learning matrix multiplication and training throughput."),
        "comp4": ("Prediction Endpoints", "Vertex AI Endpoints", "data", "Auto-scaling low-latency prediction serving with traffic splitting and model drift monitoring."),
        "flow1": "Data scientists develop model prototypes in Vertex AI Workbench notebooks.",
        "flow2": "Vertex AI Pipelines triggers automated distributed training on TPU v4 pods.",
        "flow3": "Trained model is evaluated against validation dataset and registered in Vertex AI Model Registry.",
        "fail": "Production feature values drift over time, degrading model prediction accuracy.",
        "heal": "Vertex AI Model Monitoring detects feature drift and automatically triggers pipeline retraining.",
        "city_concept": "City Guild of Inventors & Master Automata",
        "p1": "Clockmakers were building mechanical automata by hand, but every automaton was unique, broke down in rain, and could not be repaired by anyone else.",
        "p2": "Master Inventor Vera established the Automata Assembly Works (Vertex AI): standardized gear templates (Pipelines) and precision testing benches (Evaluation).",
        "p3": "Vera installed self-calibrating springs (Model Monitoring) that adjusted gear tension automatically as mechanical teeth wore down.",
        "p4": "Clockwork gears wear out physically; digital AI models are retrained, versioned, and served elastically via cloud APIs.",
        "part1_html": """
        <h3>The Situation: The Machine Learning Hierarchy on Google Cloud</h3>
        <p>
          Many engineering teams jump straight to writing complex custom PyTorch or TensorFlow neural networks when simpler, more cost-effective solutions exist. Google Cloud structures machine learning into a clear <strong>three-tier hierarchy</strong>:
        </p>
        <div class="callout">
          <div class="callout-title">The Three Tiers of Google Cloud AI</div>
          <ol>
            <li><strong>Pre-trained Foundation APIs:</strong> Zero ML expertise required. Instant REST APIs for common tasks: Cloud Vision API (image classification/OCR), Speech-to-Text, Cloud Translation, Natural Language, Document AI, and Gemini on Vertex AI.</li>
            <li><strong>AutoML (Vertex AI):</strong> Build custom models without writing neural network code. You provide labelled data; Vertex AI automatically evaluates architectures, tunes hyperparameters, and outputs an optimized model.</li>
            <li><strong>Custom Training (Vertex AI):</strong> Full control. Train custom TensorFlow, PyTorch, or XGBoost models using custom container images on distributed GPU or TPU clusters.</li>
          </ol>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: BigQuery ML for Rapid Tabular Prototyping</h4>
        <p>If your training data already resides in BigQuery, train models directly using SQL: <code>CREATE MODEL `retail.churn_model` OPTIONS(model_type='boosted_tree_classifier') AS SELECT ...</code>. Zero data export required.</p>
        <h4>Layer 2 — Practitioner: Hardware Acceleration (GPUs vs TPUs)</h4>
        <p>Choose the right accelerator: <strong>NVIDIA GPUs (T4, L4, A100, H100)</strong> are versatile for general deep learning, PyTorch, and fine-tuning. <strong>Google TPUs (Tensor Processing Units v4/v5e/v5p)</strong> excel at massive matrix multiplication for large language models (LLMs) and transformer training.</p>
        <h4>Layer 3 — Architect: MLOps with Vertex AI Pipelines</h4>
        <p>ML code is only 5% of a production ML system. <strong>Vertex AI Pipelines</strong> automates the other 95%: data extraction, validation, preprocessing, training, model evaluation, and deployment using serverless Kubeflow Pipelines (KFP).</p>
        <h4>Layer 4 — Staff: Continuous Model Monitoring & Feature Store</h4>
        <p>Staff architects deploy <strong>Vertex AI Feature Store</strong> to eliminate training-serving skew, and <strong>Model Monitoring</strong> to continuously detect concept drift and covariate shift in production inference traffic.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Vera tests precision gear ratios in her workshop, automating municipal carriage navigation.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: AI Hierarchy Selection</div>
          <p>
            Recommend the optimal AI approach for each business scenario:
          </p>
          <ol>
            <li><strong>Case A:</strong> An insurance company wants to extract invoice total, vendor name, and date from 50,000 scanned PDF receipts.</li>
            <li><strong>Case B:</strong> A retail chain wants to classify uploaded customer product photos into 20 proprietary clothing categories with 500 sample photos per category.</li>
            <li><strong>Case C:</strong> An autonomous vehicle research lab wants to train a custom multimodal sensor fusion vision model using proprietary PyTorch architectures.</li>
          </ol>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Optimal Service Selection</h4>
          <ul>
            <li><strong>Case A:</strong> <em>Document AI (Invoice Parser)</em> — Pre-trained foundation model built specifically for structured document parsing; zero training needed.</li>
            <li><strong>Case B:</strong> <em>Vertex AI AutoML Vision</em> — Custom classification using customer-provided labeled images without writing neural network code.</li>
            <li><strong>Case C:</strong> <em>Vertex AI Custom Training</em> — Distributed GPU/TPU training using custom container runtimes and PyTorch deep learning frameworks.</li>
          </ul>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: AI Architecture Selection (Question 1)</span>
          <p><strong>A financial fraud detection team has 10 TB of historical transactional data stored in BigQuery. The team consisting primarily of SQL business analysts wants to quickly build and evaluate a logistic regression fraud model without exporting data or learning Python ML frameworks. Which solution should you recommend?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! BigQuery ML enables data analysts to build, train, evaluate, and predict machine learning models directly inside BigQuery using standard SQL queries.')">A) Use BigQuery ML to create and train the classification model directly inside BigQuery using standard SQL syntax.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Exporting 10 TB of data to local laptops is slow, insecure, and memory-constrained.')">B) Export the 10 TB table to local CSV files and train a model using scikit-learn on a developer laptop.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Custom PyTorch on GKE requires deep Python ML expertise and infrastructure management.')">C) Build a custom PyTorch training cluster on GKE with GPU node pools.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Translation API is an NLP language translation service, wholly unrelated to tabular fraud detection.')">D) Call the Cloud Translation API on the transaction descriptions.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/vertex-ai/docs' target='_blank'>Vertex AI Overview & Documentation</a></li><li><a href='https://cloud.google.com/bigquery/docs/bqml-introduction' target='_blank'>BigQuery ML Introduction</a></li></ul>"
    },

    # 055: Compute Decision Cheat Sheet
    {
        "topic_no": "055",
        "roadmap_id": "CS.1",
        "title": "Cheat Sheet: Compute Engine vs GKE vs Cloud Run vs Functions",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The definitive compute selection guide: When to choose Compute Engine, GKE Autopilot, Cloud Run, Cloud Functions, and Batch based on control, scalability, portability, and operational overhead.",
        "comp1": ("Compute Engine (IaaS)", "Full OS Control", "data", "Unmanaged VMs, custom OS kernels, legacy software, and specialized hardware attachments."),
        "comp2": ("GKE Autopilot (K8s)", "Enterprise Orchestration", "data", "Complex microservice graphs, service meshes, stateful sets, and multi-tenant namespaces."),
        "comp3": ("Cloud Run (Serverless)", "Stateless Containers", "data", "HTTP microservices, scale-to-zero, instant auto-scaling, and zero infrastructure maintenance."),
        "comp4": ("Cloud Batch & Functions", "Event Glue & HPC", "data", "Small event-driven code snippets and scheduled high-performance computing batch runs."),
        "flow1": "Traffic enters through Cloud Load Balancer to designated compute tier.",
        "flow2": "Stateless requests process on Cloud Run; heavy microservice workflows route to GKE Autopilot.",
        "flow3": "Legacy Windows apps execute on Compute Engine instances within private VPC.",
        "fail": "A stateless microservice on Compute Engine fails to scale during unexpected flash traffic.",
        "heal": "Architect migrates microservice container to Cloud Run, enabling sub-second horizontal scaling to 1,000 instances.",
        "city_concept": "City Municipal Transport Fleet: Cabs, Buses, Trains & Freighters",
        "p1": "Commuters were hiring private 18-wheel freight trucks to drive two blocks to work, wasting fuel and clogging streets.",
        "p2": "City Transit Master Tilda organized the civic fleet: Bicycles for quick errands (Functions), Cabs for individuals (Cloud Run), Subways for crowds (GKE), and Heavy Rail for heavy freight (Compute Engine).",
        "p3": "Commuters picked the exact vehicle suited to their cargo, reducing city traffic by 75%.",
        "p4": "Physical vehicles must be parked somewhere; cloud serverless compute scales to zero when traffic stops.",
        "part1_html": """
        <h3>The Compute Selection Decision Tree</h3>
        <p>
          Selecting the appropriate compute service is the most consequential architectural decision in Google Cloud. Choosing a service with too much operational overhead wastes engineering hours; choosing one with too little control prevents meeting complex workload requirements.
        </p>
        <div class="callout">
          <div class="callout-title">The Master Compute Selection Matrix</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Need / Requirement</th>
                <th style="padding:6px; color:var(--accent);">Recommended Choice</th>
                <th style="padding:6px;">Key Rationale</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Full OS control, Windows, legacy software, non-containerized</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Compute Engine</strong></td>
                <td style="padding:6px;">Direct hypervisor access, custom kernels, licenses (BYOL).</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Complex container microservices, Kubernetes ecosystem, stateful apps</td>
                <td style="padding:6px; color:#38bdf8;"><strong>GKE (Autopilot first)</strong></td>
                <td style="padding:6px;">Rich CRDs, DaemonSets, Helm, Istio, advanced networking.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Stateless HTTP containers, minimal ops, scale-to-zero</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud Run</strong></td>
                <td style="padding:6px;">Container portability with zero cluster or node management.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Lightweight event-driven glue code (Pub/Sub, GCS triggers)</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud Run functions</strong></td>
                <td style="padding:6px;">Single-purpose functions without Dockerfile overhead.</td>
              </tr>
              <tr>
                <td style="padding:6px;">Large-scale batch, high-performance computing (HPC) jobs</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud Batch</strong></td>
                <td style="padding:6px;">Serverless queueing and execution of batch containers with Spot.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The Container-First Principle</h4>
        <p>Default to containerizing all software. Containers decouple your code from underlying VM runtimes, allowing workloads to move effortlessly between Cloud Run, GKE, or on-premises.</p>
        <h4>Layer 2 — Practitioner: Cloud Run vs GKE Autopilot</h4>
        <p>Choose <strong>Cloud Run</strong> if your workload is stateless, handles HTTP/gRPC traffic, or processes asynchronous tasks with scale-to-zero economics. Choose <strong>GKE</strong> if you need persistent volumes, non-HTTP protocols, DaemonSets, or complex service meshes.</p>
        <h4>Layer 3 — Architect: When to Choose Compute Engine</h4>
        <p>Use Compute Engine only when containers are impossible: legacy COTS software, specific Linux kernel modules, Windows Active Directory domain controllers, or applications requiring sole-tenant hardware.</p>
        <h4>Layer 4 — Staff: Total Cost of Ownership Evaluation</h4>
        <p>Staff architects factor developer salaries into compute decisions: a managed Cloud Run service costing $400/month is far cheaper than a $150/month Compute Engine VM that requires 20 hours of manual engineer patching per month.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Tilda assigns delivery vehicles based on weight, matching bicycles to letters and steam trains to coal.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Revision Drill: Compute Selection Decisions</div>
          <p>
            For each scenario, pick the Google-recommended compute platform:
            <br>1. An event listener that resizes images whenever uploaded to a Cloud Storage bucket.
            <br>2. An existing enterprise Java Spring Boot monolithic app running on Windows Server.
            <br>3. A public web API handling 50 requests/min during the day and 0 at night.
            <br>4. A 20-microservice e-commerce platform using Kafka, Prometheus, and Istio.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>Cloud Run functions</strong> (Eventarc trigger on GCS object finalize).</li>
            <li><strong>Compute Engine</strong> (Windows Server VM with Bring-Your-Own-License).</li>
            <li><strong>Cloud Run</strong> (scales to zero at night = zero cost).</li>
            <li><strong>GKE Autopilot</strong> (Kubernetes ecosystem with Helm, Istio, and DaemonSets).</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Compute Decision (Question 1)</span>
          <p><strong>A company wants to deploy a containerized Python web application with variable traffic that drops to zero overnight. They require zero infrastructure patching and want to pay nothing when no traffic is present. Which service should they select?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Run runs containerized applications with zero infrastructure management and automatically scales down to zero instances when idle, incurring zero cost.')">A) Cloud Run configured with minimum instances set to 0.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compute Engine instances incur costs as long as the VM is running, even with zero incoming traffic.')">B) Compute Engine with a Managed Instance Group.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'GKE clusters incur cluster management fees and node costs regardless of traffic.')">C) GKE Standard cluster.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'App Engine flexible environment does not scale to zero instances.')">D) App Engine Flexible Environment.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/hosting-options' target='_blank'>Google Cloud Compute Options Guide</a></li><li><a href='https://cloud.google.com/run/docs' target='_blank'>Cloud Run Documentation</a></li></ul>"
    },

    # 056: Database Decision Cheat Sheet
    {
        "topic_no": "056",
        "roadmap_id": "CS.2",
        "title": "Cheat Sheet: Cloud SQL vs AlloyDB vs Spanner vs Firestore vs Bigtable",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The definitive database selection guide: Relational vs NoSQL, transactional vs analytical, regional vs global consistency, and sub-millisecond key-value lookups.",
        "comp1": ("Cloud SQL & AlloyDB", "Regional Relational", "data", "Managed MySQL, Postgres, and SQL Server; AlloyDB for high-throughput transactional analytics."),
        "comp2": ("Cloud Spanner", "Global Multi-Region Relational", "data", "Horizontally scalable relational ACID with 99.999% SLA and synchronous consistency."),
        "comp3": ("Cloud Bigtable & Firestore", "Scalable NoSQL", "data", "Bigtable for petabyte-scale IoT/time-series; Firestore for flexible mobile/web document stores."),
        "comp4": ("Memorystore & BigQuery", "Cache & Warehouse", "data", "Memorystore Redis for sub-millisecond caching; BigQuery for petabyte enterprise warehousing."),
        "flow1": "Application evaluates database query requirements: relational schema vs unstructured documents.",
        "flow2": "Transactional writes route to Cloud Spanner or Cloud SQL; analytical queries sink to BigQuery.",
        "flow3": "Sub-millisecond session tokens route to Memorystore Redis cache.",
        "fail": "A developer selects Cloud SQL for an IoT telemetry workload writing 500,000 sensor events/sec.",
        "heal": "Architect refactors ingestion to Cloud Bigtable, achieving linear write scaling with sub-10ms latency.",
        "city_concept": "City Record Halls: Ledgers, Card Catalogs & Vaults",
        "p1": "The city recorder stored tax audits, citizen birth certificates, and warehouse shipping tallies in the exact same wooden drawer.",
        "p2": "Archivist Arthur established specialized archives: Bound Ledgers for taxes (Cloud SQL), The Master Vault for royal deeds (Spanner), and Tally Slates for cart weights (Bigtable).",
        "p3": "Clerks retrieved tax records in seconds and weighed grain wagons without disturbing royal records.",
        "p4": "Physical paper vaults can burn down; cloud databases replicate transactions synchronously across multiple availability zones.",
        "part1_html": """
        <h3>The Database Selection Decision Matrix</h3>
        <p>
          Selecting the right database is critical because changing a database in production is a "one-way door" decision. Data migrations are expensive, risky, and time-consuming.
        </p>
        <div class="callout">
          <div class="callout-title">The Master Database Selection Guide</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Workload Requirement</th>
                <th style="padding:6px; color:var(--accent);">Database Choice</th>
                <th style="padding:6px;">Key Characteristics</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Regional relational, lift-and-shift MySQL/Postgres/SQL Server</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud SQL</strong></td>
                <td style="padding:6px;">99.95% HA SLA, up to 64 TB storage, standard SQL syntax.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">High-performance PostgreSQL, mixed HTAP analytics</td>
                <td style="padding:6px; color:#38bdf8;"><strong>AlloyDB</strong></td>
                <td style="padding:6px;">4x faster than standard Cloud SQL for Postgres, columnar engine.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Global relational scale, external consistency, 99.999% SLA</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud Spanner</strong></td>
                <td style="padding:6px;">Synchronous Paxos replication across regions, TrueTime, unlimited scale.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Mobile & web app backend, document store, offline sync</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Firestore</strong></td>
                <td style="padding:6px;">Real-time client SDK listeners, automatic horizontal scaling.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Massive scale time-series, IoT, telemetry, low-latency writes</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud Bigtable</strong></td>
                <td style="padding:6px;">HBase API, sub-10ms latency, millions of writes/sec, petabytes.</td>
              </tr>
              <tr>
                <td style="padding:6px;">Sub-millisecond in-memory cache, session tokens</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Memorystore</strong></td>
                <td style="padding:6px;">Managed Redis and Memcached, VPC peering, in-memory speed.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Relational vs NoSQL Trade-Offs</h4>
        <p>Use Relational (Cloud SQL, Spanner) when you need ACID transactions across multiple tables, foreign key constraints, and relational schemas. Use NoSQL (Bigtable, Firestore) when you need massive horizontal scalability or flexible schemas.</p>
        <h4>Layer 2 — Practitioner: Cloud SQL vs Cloud Spanner</h4>
        <p>Choose <strong>Cloud SQL</strong> when data fits within a single region, total storage is under 64 TB, and standard database compatibility is required. Choose <strong>Cloud Spanner</strong> when you need horizontal write scaling beyond a single machine, global distribution, and 99.999% availability.</p>
        <h4>Layer 3 — Architect: Bigtable vs Firestore</h4>
        <p>Choose <strong>Bigtable</strong> for high-throughput, machine-generated streaming data (IoT, financial tickers) accessed via row keys. Choose <strong>Firestore</strong> for human-facing web/mobile applications with complex document queries and offline mobile synchronization.</p>
        <h4>Layer 4 — Staff: Hybrid Transactional & Analytical Processing (HTAP)</h4>
        <p>Staff architects deploy <strong>AlloyDB</strong> or <strong>Spanner with BigQuery Federation</strong> to run analytical queries over live transactional data without impacting production write throughput.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Arthur files records into specialized drawers, ensuring merchants find receipts without locking the city vaults.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Database Selection Decision Drill</div>
          <p>Match the business workload to the single best Google Cloud database:</p>
          <ol>
            <li><strong>Workload 1:</strong> A mobile fitness app where users see live friend leaderboards, requiring offline phone caching and document JSON sync.</li>
            <li><strong>Workload 2:</strong> A global airline reservation system requiring ACID guarantees across 4 continents with five 9s (99.999%) availability.</li>
            <li><strong>Workload 3:</strong> 100,000 smart electrical meters writing kilowatt-hour readings every second (total 100 TB/week).</li>
            <li><strong>Workload 4:</strong> An enterprise migrating an existing internal HR portal using Microsoft SQL Server.</li>
          </ol>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>Firestore</strong> (mobile SDK, offline sync, document model).</li>
            <li><strong>Cloud Spanner</strong> (global relational, ACID, 99.999% SLA).</li>
            <li><strong>Cloud Bigtable</strong> (high-throughput time-series IoT writes, sub-10ms).</li>
            <li><strong>Cloud SQL for SQL Server</strong> (fully managed SQL Server compatibility).</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Database Selection (Question 1)</span>
          <p><strong>A financial institution requires a globally distributed relational database to store customer account balances across the US, Europe, and Asia. Transactions must be strictly consistent (ACID) globally with an SLA of 99.999% availability. Which database must be selected?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Spanner is the only database in Google Cloud providing global relational ACID consistency with a 99.999% SLA.')">A) Cloud Spanner in a multi-region configuration.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL is regional and provides at most 99.95% SLA; cross-region replicas are asynchronous.')">B) Cloud SQL for PostgreSQL with cross-region read replicas.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Bigtable provides eventual consistency across clusters and lacks multi-row relational ACID transactions.')">C) Cloud Bigtable multi-cluster instance.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Firestore does not provide 99.999% SLA for relational global multi-region SQL.')">D) Firestore in Datastore mode.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/products/databases' target='_blank'>Google Cloud Databases Portfolio</a></li><li><a href='https://cloud.google.com/spanner/docs' target='_blank'>Cloud Spanner Architecture & Docs</a></li></ul>"
    },

    # 057: Load Balancer Decision Cheat Sheet
    {
        "topic_no": "057",
        "roadmap_id": "CS.3",
        "title": "Cheat Sheet: Cloud Load Balancing Selection Matrix",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The definitive load balancing decision guide: Application (L7) vs Network (L4), Global Anycast vs Regional, Proxy vs Passthrough, and Internal vs External topologies.",
        "comp1": ("Global Application LB (L7)", "External Anycast Proxy", "data", "HTTP/HTTPS, Cloud CDN, Cloud Armor, SSL termination, and advanced path-based routing."),
        "comp2": ("Regional Application LB (L7)", "Regional Proxy", "data", "HTTP/HTTPS within a single region, complying with strict regional data residency laws."),
        "comp3": ("Proxy Network LB (L4)", "TCP / SSL Proxy", "data", "Non-HTTP global TCP applications with Anycast IP and Google edge SSL termination."),
        "comp4": ("Passthrough Network LB (L4)", "Maglev Direct Passthrough", "data", "Preserves client source IP, handles UDP, VoIP, gaming, and ultra-high packet performance."),
        "flow1": "Client initiates connection to Google Anycast virtual IP address.",
        "flow2": "Global load balancer terminates TLS at nearest edge PoP and evaluates routing rules.",
        "flow3": "Requests proxy to healthy backend instances across regions or pass directly through Maglev.",
        "fail": "A backend region becomes saturated during a localized traffic spike.",
        "heal": "Global External ALB automatically reroutes spillover traffic to secondary healthy region with available capacity.",
        "city_concept": "City Canal Locks & Harbor Piloting Stations",
        "p1": "Boats of all sizes were crowding into narrow canals simultaneously, causing collisions between rowboats and cargo barges.",
        "p2": "Harbor Master Hugh built piloting stations: Outer Gates for ocean ships (Global ALB) and Canal Sluices for internal barges (Internal LB).",
        "p3": "Pilots inspected cargo manifests (Layer 7 inspection), directing grain ships to northern docks and passenger boats to downtown piers.",
        "p4": "Canal locks operate with physical water valves; cloud load balancers balance gigabits of network traffic via Maglev software SDN.",
        "part1_html": """
        <h3>The Load Balancer Selection Decision Tree</h3>
        <p>
          Google Cloud Load Balancing is uniquely different from other clouds: it is fully distributed, software-defined (powered by <strong>Maglev</strong> and <strong>Andromeda</strong>), and requires no pre-warming to handle massive sudden traffic spikes.
        </p>
        <div class="callout">
          <div class="callout-title">The Master Load Balancing Matrix</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Need / Protocol</th>
                <th style="padding:6px; color:var(--accent);">Load Balancer Choice</th>
                <th style="padding:6px;">Scope & Architecture</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Global HTTP(S), CDN, Cloud Armor WAF, URL routing</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Global External Application LB</strong></td>
                <td style="padding:6px;">Global Anycast proxy, Layer 7, edge SSL termination.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Regional HTTP(S) with strict data residency mandates</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Regional External Application LB</strong></td>
                <td style="padding:6px;">Regional proxy, Layer 7, keeps traffic inside specific region.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Internal HTTP(S) microservices inside private VPC</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Internal Application LB</strong></td>
                <td style="padding:6px;">Regional proxy, Layer 7, private IP, Envoy-based.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Non-HTTP TCP with global reach & edge SSL termination</td>
                <td style="padding:6px; color:#38bdf8;"><strong>External Proxy Network LB</strong></td>
                <td style="padding:6px;">Global Anycast proxy, Layer 4, SSL/TCP offload at edge.</td>
              </tr>
              <tr>
                <td style="padding:6px;">Preserve client IP, UDP, high performance, gaming, VoIP</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Passthrough Network LB</strong></td>
                <td style="padding:6px;">Regional passthrough, Layer 4, non-proxy (preserves IP).</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Application (L7) vs Network (L4)</h4>
        <p>Use <strong>Application Load Balancers (L7)</strong> when you need to inspect HTTP headers, cookies, URL paths (e.g. <code>/api/*</code> vs <code>/static/*</code>), or integrate with Cloud Armor and Cloud CDN. Use <strong>Network Load Balancers (L4)</strong> for raw TCP/UDP.</p>
        <h4>Layer 2 — Practitioner: Proxy vs Passthrough Mechanics</h4>
        <p>In a <strong>Proxy</strong> load balancer, Google terminates the client connection and opens a separate backend connection (backend sees Google's proxy IP unless reading <code>X-Forwarded-For</code>). In a <strong>Passthrough</strong> load balancer, packets pass unchanged directly to the VM (backend sees the real client IP directly in the IP header).</p>
        <h4>Layer 3 — Architect: Cross-Region Spillover</h4>
        <p>Global External ALBs track backend capacity (utilization or RPS). If the primary region in us-east1 reaches 100% capacity during a flash sale, excess requests are automatically spilled over to us-central1 without returning errors to users.</p>
        <h4>Layer 4 — Staff: Serverless NEGs & Hybrid Connectivity NEGs</h4>
        <p>Network Endpoint Groups (NEGs) allow load balancers to route directly to serverless backends (Cloud Run, App Engine), Kubernetes pod IPs (Standalone NEGs), or on-premises servers via Cloud Interconnect.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Hugh's canal piloting stations guide incoming ships to their exact berths with zero traffic congestion.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Revision Drill: Load Balancer Selection</div>
          <p>
            Select the exact load balancer for each requirement:
            <br>1. Global gaming backend receiving UDP telemetry and requiring client source IP preservation.
            <br>2. An e-commerce website requiring Cloud Armor WAF and Cloud CDN edge caching.
            <br>3. Internal communication between private GKE microservices requiring path-based URL routing.
            <br>4. A global non-HTTP encrypted TCP database gateway terminating TLS at Google's edge.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>External Passthrough Network Load Balancer</strong> (handles UDP, preserves client IP).</li>
            <li><strong>Global External Application Load Balancer</strong> (L7, Cloud Armor, Cloud CDN).</li>
            <li><strong>Internal Application Load Balancer</strong> (private IP, L7 URL path routing).</li>
            <li><strong>External Proxy Network Load Balancer</strong> (global Anycast TCP/SSL termination).</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Load Balancer Decision (Question 1)</span>
          <p><strong>A video streaming service requires a load balancer for a global mobile application. The service must route traffic based on HTTP URL path (/video vs /user), integrate with Cloud Armor WAF, and cache video segments at Google's edge points of presence. Which load balancer is required?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Global External Application Load Balancer provides Layer 7 path-based routing, Cloud Armor WAF integration, and Cloud CDN edge caching.')">A) Global External Application Load Balancer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Passthrough Network Load Balancers operate at Layer 4 and cannot inspect HTTP URL paths or integrate with Cloud CDN/Armor.')">B) External Passthrough Network Load Balancer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Proxy Network Load Balancer operates at Layer 4 (TCP) and cannot read HTTP path headers.')">C) External Proxy Network Load Balancer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Internal Application Load Balancer only serves private VPC traffic and cannot terminate public internet traffic.')">D) Internal Application Load Balancer.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/load-balancing/docs' target='_blank'>Google Cloud Load Balancing Overview</a></li><li><a href='https://cloud.google.com/load-balancing/docs/choosing-a-load-balancer' target='_blank'>Choosing a Load Balancer Guide</a></li></ul>"
    },

    # 058: Hybrid Connectivity Decision Cheat Sheet
    {
        "topic_no": "058",
        "roadmap_id": "CS.4",
        "title": "Cheat Sheet: Hybrid Connectivity (HA VPN vs Interconnect)",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The definitive hybrid networking guide: Cloud HA VPN (99.99%), Dedicated Interconnect, Partner Interconnect, Cross-Cloud Interconnect, and Cloud Router BGP dynamic routing.",
        "comp1": ("Cloud HA VPN", "Encrypted Over Internet", "data", "Quick setup, IPsec encrypted, up to a few Gbps per tunnel, 99.99% SLA with dual tunnels."),
        "comp2": ("Partner Interconnect", "Service Provider Circuit", "data", "Private SLA connection for organizations with no presence in a Google colocation facility."),
        "comp3": ("Dedicated Interconnect", "Physical 10G/100G Fiber", "data", "Highest bandwidth (10/100/200 Gbps), sub-millisecond private fiber, 99.99% multi-metro SLA."),
        "comp4": ("Cloud Router & BGP", "Dynamic Route Exchange", "control", "Automatically exchanges BGP routes, recalculating paths during physical cable cuts."),
        "flow1": "On-premises enterprise router establishes BGP peering session with Google Cloud Router.",
        "flow2": "Traffic flows securely across private fiber circuit or IPsec encrypted tunnels.",
        "flow3": "Cloud Router dynamically propagates VPC subnet routes to on-premises routing tables.",
        "fail": "A backhoe cuts a physical fiber line in Metro 1.",
        "heal": "BGP withdraws dead routes and shifts traffic to redundant circuit in Metro 2 within seconds.",
        "city_concept": "City Regional Aqueducts & Covered Mountain Tunnels",
        "p1": "Caravans between Cloud City and the mountain mining village were frequently robbed by bandits on open dirt roads.",
        "p2": "Warden Ward built two secure transport paths: Armed Courier Convoys (HA VPN) and a Private Paved Highway with stone guardrails (Interconnect).",
        "p3": "When a rockslide blocked Tunnel 1, automated signal towers (BGP) routed wagons through Tunnel 2 without delay.",
        "p4": "Digging mountain tunnels takes years; Cloud HA VPN tunnels can be deployed and validated in 30 minutes.",
        "part1_html": """
        <h3>The Hybrid Connectivity Selection Matrix</h3>
        <p>
          Connecting an enterprise on-premises datacenter to Google Cloud requires balancing <strong>bandwidth</strong>, <strong>cost</strong>, <strong>setup time</strong>, and <strong>availability SLAs</strong>.
        </p>
        <div class="callout">
          <div class="callout-title">The Master Hybrid Connectivity Guide</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Need / Constraint</th>
                <th style="padding:6px; color:var(--accent);">Connectivity Choice</th>
                <th style="padding:6px;">Key Characteristics</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Fast, low cost, encrypted over internet, bandwidth &lt; 3 Gbps/tunnel</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cloud HA VPN</strong></td>
                <td style="padding:6px;">99.99% SLA (dual active tunnels), IPsec encryption, no colocation needed.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Private connection, bandwidth 50 Mbps - 10 Gbps, no colocation presence</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Partner Interconnect</strong></td>
                <td style="padding:6px;">Connected via service provider (Equinix, AT&T, Lumen), private IP.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;">Highest bandwidth (10/100 Gbps), lowest latency, colocation facility</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Dedicated Interconnect</strong></td>
                <td style="padding:6px;">Direct physical fiber cross-connect, 99.99% multi-metro SLA, unencrypted by default.</td>
              </tr>
              <tr>
                <td style="padding:6px;">Direct high-bandwidth link between Google Cloud and AWS/Azure</td>
                <td style="padding:6px; color:#38bdf8;"><strong>Cross-Cloud Interconnect</strong></td>
                <td style="padding:6px;">High-speed multi-cloud private connectivity without third-party routers.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Cloud HA VPN 99.99% SLA Topology</h4>
        <p>A single VPN tunnel provides no SLA. To achieve Google's <strong>99.99% SLA</strong>, you must configure Cloud HA VPN with <strong>two tunnels</strong> across two separate gateway interfaces connected to redundant peer routers running dynamic BGP routing.</p>
        <h4>Layer 2 — Practitioner: Partner vs Dedicated Interconnect</h4>
        <p>Choose <strong>Dedicated Interconnect</strong> if your company already has hardware inside a Google colocation facility (meet-me room) and needs 10G/100G pipelines. Choose <strong>Partner Interconnect</strong> if you need less than 10 Gbps or do not have colocation presence.</p>
        <h4>Layer 3 — Architect: 99.99% Multi-Metro Interconnect Architecture</h4>
        <p>To qualify for the 99.99% Interconnect SLA, you must provision <strong>4 separate circuits across two distinct metropolitan areas</strong> (e.g. 2 in Chicago and 2 in Ashburn) connected to two separate Cloud Routers.</p>
        <h4>Layer 4 — Staff: MACsec & Encrypted Interconnect</h4>
        <p>By default, Cloud Interconnect is private but unencrypted. Regulated enterprises mandate <strong>MACsec (Layer 2 encryption)</strong> on Dedicated Interconnect or run <strong>HA VPN over Interconnect</strong> to achieve line-rate encryption.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Ward safeguards both mountain trails and paved royal highways, keeping trade moving year-round.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Revision Drill: Hybrid Connectivity Selection</div>
          <p>
            Select the appropriate connectivity solution:
            <br>1. An enterprise needs to connect on-premises to GCP in 48 hours for a quick pilot with bandwidth under 1 Gbps.
            <br>2. A bank requires 40 Gbps private bandwidth with a 99.99% SLA between their colocation cage and GCP.
            <br>3. A retail company needs a 500 Mbps private dedicated link but has no presence in a colocation facility.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>Cloud HA VPN</strong> (fastest setup, runs over public internet with IPsec).</li>
            <li><strong>Dedicated Interconnect</strong> (multi-metro 4-circuit topology for 99.99% SLA).</li>
            <li><strong>Partner Interconnect</strong> (bandwidth &lt; 10 Gbps via certified network provider).</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Hybrid Connectivity (Question 1)</span>
          <p><strong>A financial institution requires a private, dedicated network connection between their on-premises datacenter and Google Cloud with 20 Gbps bandwidth. The company does not own or lease equipment in any Google colocation facility. Which solution fulfills their requirement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Partner Interconnect provides private, high-bandwidth connections through a supported service provider without requiring physical presence in a Google colocation facility.')">A) Partner Interconnect through a certified service provider.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Dedicated Interconnect strictly requires the client to meet Google directly in a colocation facility.')">B) Dedicated Interconnect with 100 Gbps circuits.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud HA VPN tunnels cap throughput at 3 Gbps per tunnel, which cannot meet 20 Gbps without dozens of complex parallel tunnels.')">C) Cloud HA VPN with a single tunnel.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standard internet egress is public and unmanaged.')">D) Public internet routing over Standard Network Tier.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/network-connectivity/docs' target='_blank'>Network Connectivity Products Overview</a></li><li><a href='https://cloud.google.com/network-connectivity/docs/interconnect' target='_blank'>Cloud Interconnect Documentation</a></li></ul>"
    },

    # 059: Storage & Messaging Decision Cheat Sheet
    {
        "topic_no": "059",
        "roadmap_id": "CS.5",
        "title": "Cheat Sheet: Storage Classes, Disks & Messaging (Pub/Sub vs Tasks)",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The definitive storage and messaging guide: Cloud Storage classes (Standard vs Nearline vs Coldline vs Archive), Persistent Disk vs Hyperdisk vs Local SSD, and Pub/Sub vs Cloud Tasks vs Eventarc.",
        "comp1": ("Cloud Storage Classes", "Object Storage", "data", "Standard for active data; Nearline (30d), Coldline (90d), Archive (365d) for cold backups."),
        "comp2": ("Block Storage Fleet", "Hyperdisk & Local SSD", "data", "Hyperdisk for dynamic IOPS scaling; Local SSD for ultra-low latency NVMe scratch space."),
        "comp3": ("Cloud Pub/Sub", "Global Event Stream", "control", "Decoupled asynchronous event ingestion, fan-out topics, and streaming pipelines."),
        "comp4": ("Cloud Tasks & Eventarc", "Targeted Delivery & Glue", "control", "Cloud Tasks for rate limiting and task queues; Eventarc for event-driven reactive architecture."),
        "flow1": "Application produces streaming events; Pub/Sub fans out to multiple subscriber queues.",
        "flow2": "Worker persists batch archive to Cloud Storage with automated Autoclass tiering.",
        "flow3": "High-IOPS database persists transactions to Hyperdisk Balanced block storage.",
        "fail": "A batch worker crashes while processing a distributed task.",
        "heal": "Cloud Tasks automatically retries delivery with configurable rate limits and dead-letter queueing.",
        "city_concept": "City Warehouses, Pneumatic Tubes & Courier Desks",
        "p1": "Merchants were storing summer wheat and 100-year historical stone monuments in prime heated city-center storefronts.",
        "p2": "Warehouse Master Wendy established tiered storage: Active Storefronts (Standard), Deep Cold Cellars (Archive), and Fast Pneumatic Tubes for telegrams (Pub/Sub).",
        "p3": "Old stone monuments were moved to dry mountain caves (Archive), freeing up downtown storefronts.",
        "p4": "Moving physical furniture between warehouses takes days; Cloud Storage Autoclass transitions digital objects automatically based on access.",
        "part1_html": """
        <h3>Storage and Messaging Decision Matrices</h3>
        <p>
          Selecting the optimal storage tier and messaging queue prevents runaway storage costs and ensures system components decouple cleanly.
        </p>
        <div class="callout">
          <div class="callout-title">Part A: Cloud Storage Classes & Minimum Retention</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Storage Class</th>
                <th style="padding:6px; color:var(--accent);">Min Retention</th>
                <th style="padding:6px;">Access Frequency</th>
                <th style="padding:6px;">Best For</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;"><strong>Standard</strong></td>
                <td style="padding:6px;">None</td>
                <td style="padding:6px;">Frequent / Daily</td>
                <td style="padding:6px;">Active web assets, streaming video, live analytics.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;"><strong>Nearline</strong></td>
                <td style="padding:6px; color:#fb923c;">30 days</td>
                <td style="padding:6px;">&lt; Once a month</td>
                <td style="padding:6px;">Monthly backups, rarely accessed reports.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;"><strong>Coldline</strong></td>
                <td style="padding:6px; color:#fb923c;">90 days</td>
                <td style="padding:6px;">&lt; Once a quarter</td>
                <td style="padding:6px;">Disaster recovery archives, quarterly compliance data.</td>
              </tr>
              <tr>
                <td style="padding:6px;"><strong>Archive</strong></td>
                <td style="padding:6px; color:#fb923c;">365 days</td>
                <td style="padding:6px;">&lt; Once a year</td>
                <td style="padding:6px;">7-year regulatory archives, digital preservation (cheapest).</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="callout" style="margin-top:14px;">
          <div class="callout-title">Part B: Messaging: Pub/Sub vs Cloud Tasks vs Eventarc</div>
          <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;">
            <thead>
              <tr style="border-bottom:1px solid var(--panel-border); text-align:left;">
                <th style="padding:6px;">Service</th>
                <th style="padding:6px; color:var(--accent);">Core Paradigm</th>
                <th style="padding:6px;">Best Use Case</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;"><strong>Cloud Pub/Sub</strong></td>
                <td style="padding:6px;">Publisher-Subscriber (1-to-many fanout)</td>
                <td style="padding:6px;">Decoupled streaming, event ingestion, Kafka-like pipelines.</td>
              </tr>
              <tr style="border-bottom:1px solid #1a2035;">
                <td style="padding:6px;"><strong>Cloud Tasks</strong></td>
                <td style="padding:6px;">Point-to-Point Task Queue (1-to-1)</td>
                <td style="padding:6px;">Rate limiting backend calls, specific scheduled delivery, task deduplication.</td>
              </tr>
              <tr>
                <td style="padding:6px;"><strong>Eventarc</strong></td>
                <td style="padding:6px;">Event Router (CloudEvents standard)</td>
                <td style="padding:6px;">Reacting to Google events (GCS file created, BigQuery audit log) to trigger Cloud Run.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Storage Class Early Deletion Fees</h4>
        <p>If you delete, replace, or move an object in <strong>Archive storage</strong> before 365 days, you are billed an early deletion fee for the remaining days! Use <strong>Autoclass</strong> to automatically handle tier transitions without manual scripts.</p>
        <h4>Layer 2 — Practitioner: Persistent Disk vs Hyperdisk vs Local SSD</h4>
        <p>Use <strong>Hyperdisk Balanced</strong> for modern general-purpose block storage with independent IOPS and throughput tuning. Use <strong>Local SSD</strong> (NVMe) only for transient scratch disks or caches where data loss on VM stop is acceptable.</p>
        <h4>Layer 3 — Architect: Pub/Sub vs Cloud Tasks Architectural Distinction</h4>
        <p>Choose <strong>Pub/Sub</strong> when the publisher does not know who the subscribers are (decoupling, analytics fanout). Choose <strong>Cloud Tasks</strong> when the producer needs fine-grained control over execution: dispatch rate (e.g. max 10 requests/sec), retry attempts, or scheduled execution at a specific future time.</p>
        <h4>Layer 4 — Staff: Global Event-Driven Architectures</h4>
        <p>Staff architects standardize enterprise eventing on <strong>Eventarc</strong> using the CNCF CloudEvents standard, routing operational audit events and mutations across multi-region services seamlessly.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Wendy files cold archives in mountain caves and routes express letters through rapid pneumatic tubes.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Storage and Messaging Selection Drill</div>
          <p>Select the optimal GCP product for each scenario:</p>
          <ol>
            <li><strong>Case 1:</strong> Storing medical x-ray scans that must be retained for 10 years to meet legal mandates, with retrieval expected less than once every 3 years.</li>
            <li><strong>Case 2:</strong> A webhook listener needs to forward incoming requests to an on-premises legacy API that crashes if it receives more than 5 requests per second.</li>
            <li><strong>Case 3:</strong> High-performance machine learning training needing 1,000,000 read IOPS scratch space for temporary image tensor manipulation.</li>
          </ol>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>Cloud Storage Archive tier</strong> (lowest storage cost for &gt; 365 day retention; pay retrieval fee only if audited).</li>
            <li><strong>Cloud Tasks</strong> (allows configuring queue dispatch rate limit: <code>max-dispatches-per-second = 5</code>).</li>
            <li><strong>Local SSD</strong> (physically attached NVMe providing millions of ultra-low latency IOPS for scratch space).</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Storage & Messaging (Question 1)</span>
          <p><strong>An application receives webhook events from external payment gateways and must call an internal legacy inventory service. The legacy inventory service can only handle a maximum of 10 concurrent requests and will crash if overwhelmed. Which service should you place between the webhook receiver and the inventory service?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Tasks provides rate-limiting controls, including maximum dispatches per second and maximum concurrent tasks, protecting delicate downstream backends.')">A) Cloud Tasks with configured max-concurrent-dispatches and rate-limiting.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Pub/Sub pushes messages as quickly as possible and does not provide precise rate-limiting throttling out of the box.')">B) Cloud Pub/Sub with a push subscription.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Storage buckets are object stores and cannot dispatch HTTP webhook tasks with rate limiting.')">C) Cloud Storage bucket with object lifecycle rules.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Armor is a web application firewall for ingress; it does not queue asynchronous background tasks.')">D) Cloud Armor rate-limiting policy.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/storage/docs/storage-classes' target='_blank'>Cloud Storage Classes Documentation</a></li><li><a href='https://cloud.google.com/tasks/docs' target='_blank'>Cloud Tasks Queue Documentation</a></li></ul>"
    },

    # 060: Key Numbers, Limits & SLAs to Memorise
    {
        "topic_no": "060",
        "roadmap_id": "CS.6",
        "title": "Cheat Sheet: Key Numbers, Limits & SLAs for the PCA Exam",
        "page_type": "cheat-sheet",
        "phase": "Service Decision Cheat Sheets",
        "lead": "The essential architect memory bank: Uptime availability downtime math, storage class minimum durations, maximum Pub/Sub and Cloud Run limits, VPC CIDR boundaries, and official GCP service SLAs.",
        "comp1": ("Availability Math", "SLA Calculation Table", "control", "Exact downtime minutes per month: 99.9% = 43.8 min, 99.95% = 21.9 min, 99.99% = 4.38 min."),
        "comp2": ("Storage & Retention Limits", "Durations & Capacities", "control", "Nearline 30d, Coldline 90d, Archive 365d, Cloud SQL 64 TB, Pub/Sub 10 MB message size."),
        "comp3": ("Networking Thresholds", "Bandwidths & Routes", "control", "HA VPN 3 Gbps/tunnel, Dedicated Interconnect 10/100G, MTU 1460 vs 1500 vs 8896 jumbo frames."),
        "comp4": ("Exam Readiness Checklist", "Final Polish", "control", "Final review of decision rules, domain weights, and elimination heuristics before taking the exam."),
        "flow1": "Architect reviews SLA math table to evaluate composite contract obligations.",
        "flow2": "Architect checks network throughput thresholds when planning hybrid interconnect migration.",
        "flow3": "Architect enters PCA exam with memorized limits, instantly eliminating incorrect multiple choice answers.",
        "fail": "A candidate guesses on an exam question about storage minimum retention fees.",
        "heal": "Candidate remembers the 30-90-365 rule, confidently selecting Coldline for 90-day retention.",
        "city_concept": "City Standard Measures & Guild Hall Weights",
        "p1": "Every merchant in Cloud City used a different length of rope and a different weight of lead, causing endless trade disputes.",
        "p2": "Grand Master Marcus cast standard brass weights and yardsticks (Key Numbers) displayed in the central Guild Hall.",
        "p3": "Every apprentice memorized the standard civic measures before being granted their master builder license.",
        "p4": "Brass standards are preserved in glass cases; cloud architectural metrics guide mission-critical enterprise design globally.",
        "part1_html": """
        <h3>The Architect's Quick-Reference Memory Bank</h3>
        <p>
          While the Google Professional Cloud Architect exam tests architectural reasoning rather than raw memorization, knowing key numbers, product boundaries, and SLAs allows you to instantly eliminate wrong answers and validate design feasibility.
        </p>
        <div class="callout">
          <div class="callout-title">The Essential Availability Math (Based on 30-day Month = 43,200 min)</div>
          <ul>
            <li><strong>99.0% (Two 9s):</strong> ~7.2 hours / month (432 min) • ~3.65 days / year</li>
            <li><strong>99.9% (Three 9s):</strong> ~43.8 minutes / month • ~8.76 hours / year</li>
            <li><strong>99.95% (Three and a half 9s):</strong> ~21.9 minutes / month • ~4.38 hours / year</li>
            <li><strong>99.99% (Four 9s):</strong> ~4.38 minutes / month • ~52.56 minutes / year</li>
            <li><strong>99.999% (Five 9s - Spanner Multi-Region):</strong> ~26.3 seconds / month • ~5.26 minutes / year</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Storage Class Minimum Durations</h4>
        <p><strong>Standard:</strong> No minimum duration.<br><strong>Nearline:</strong> 30 days minimum.<br><strong>Coldline:</strong> 90 days minimum.<br><strong>Archive:</strong> 365 days minimum.<br><em>Tip: Deleting an object before the minimum duration incurs an early deletion fee equal to the remaining days.</em></p>
        <h4>Layer 2 — Networking Numbers</h4>
        <p><strong>Cloud HA VPN:</strong> Up to 3 Gbps per tunnel (ingress/egress), 250,000 packets/sec.<br><strong>Cloud Interconnect:</strong> Dedicated (10 Gbps or 100 Gbps circuits); Partner (50 Mbps up to 10 Gbps).<br><strong>Cloud DNS:</strong> 100% availability SLA.<br><strong>VPC MTU:</strong> Default 1460 bytes; supports 1500 (standard Ethernet) and 8896 (Jumbo frames).</p>
        <h4>Layer 3 — Compute & Database Limits</h4>
        <p><strong>Cloud Run:</strong> Max container memory: 32 GB; Max vCPU: 8; Max request timeout: 60 minutes.<br><strong>Cloud Pub/Sub:</strong> Max message size: 10 MB; Max retention: 7 days.<br><strong>Cloud SQL:</strong> Max storage: 64 TB; Max connections: depends on vCPU/RAM.<br><strong>BigQuery:</strong> Max query execution time: 6 hours; Max streaming insert row size: 10 MB.</p>
        <h4>Layer 4 — Key Official SLAs</h4>
        <p>Cloud Spanner Multi-Region: <strong>99.999%</strong> • Cloud Spanner Regional: <strong>99.99%</strong> • Cloud SQL Regional HA: <strong>99.95%</strong> • Compute Engine Regional MIG: <strong>99.99%</strong> • Cloud HA VPN: <strong>99.99%</strong> • Dedicated Interconnect (4 circuits across 2 metros): <strong>99.99%</strong>.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Master Marcus verifies that every apprentice builder can recite the standard foundation measures by heart.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Rapid-Fire Memory Drill</div>
          <p>
            Answer in 5 seconds per question:
            <br>1. What is the minimum storage duration for Cloud Storage Coldline?
            <br>2. What is the SLA of Cloud Spanner in a multi-region deployment?
            <br>3. What is the maximum throughput of a single Cloud HA VPN tunnel?
            <br>4. How many minutes of downtime per month does a 99.95% SLA permit?
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Answers</h4>
          <ol>
            <li><strong>90 days</strong> (Coldline).</li>
            <li><strong>99.999%</strong> (Five 9s).</li>
            <li><strong>3 Gbps</strong> per tunnel.</li>
            <li><strong>21.9 minutes</strong> per month.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Core Limits (Question 1)</span>
          <p><strong>A compliance policy requires backing up database dumps once a quarter and keeping them for exactly 100 days before deleting them. Which Cloud Storage class provides the lowest storage cost without incurring early deletion penalty fees?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Coldline storage requires a minimum retention of 90 days. Because the files are retained for 100 days, no early deletion fee is charged, and Coldline is cheaper than Nearline or Standard.')">A) Coldline storage (90-day minimum retention period).</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Archive storage requires a 365-day minimum retention; deleting at 100 days incurs a 265-day early deletion penalty fee.')">B) Archive storage (365-day minimum retention period).</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standard storage is significantly more expensive per GB than Coldline for quarterly backups.')">C) Standard storage.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Nearline has higher storage cost per GB than Coldline.')">D) Nearline storage.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/terms/sla' target='_blank'>Google Cloud Service Level Agreements (SLAs)</a></li><li><a href='https://cloud.google.com/storage/pricing' target='_blank'>Cloud Storage Pricing & Minimum Durations</a></li></ul>"
    }
]

def main():
    print(f"Building Topics 051 to 060 (Cross-Cutting & Cheat Sheets) - {len(FINAL_TOPICS)} topics...")
    for item in FINAL_TOPICS:
        t_no = item["topic_no"]
        r_id = item["roadmap_id"]
        title = item["title"]
        
        d1 = make_d1_map(t_no, r_id, title, item["comp1"], item["comp2"], item["comp3"], item["comp4"])
        d2 = make_d2_flow(t_no, r_id, title, item["flow1"], item["flow2"], item["flow3"])
        d3 = make_d3_failure(t_no, r_id, title, item["fail"], item["heal"])
        analogy = make_analogy(t_no, r_id, title, item["city_concept"], item["p1"], item["p2"], item["p3"], item["p4"])
        
        topic_data = {
            "topic_no": t_no,
            "roadmap_id": r_id,
            "title": title,
            "page_type": item["page_type"],
            "phase": item["phase"],
            "lead": item["lead"],
            "d1": d1,
            "d2": d2,
            "d3": d3,
            "analogy": analogy,
            "part1_html": item["part1_html"],
            "part2_ladder_html": item["part2_ladder_html"],
            "part3_narrative_html": item["part3_narrative_html"],
            "part4_demo_html": item["part4_demo_html"],
            "quiz_html": item["quiz_html"],
            "reading_html": item["reading_html"]
        }
        build_topic_page(topic_data)
        print(f"  ✓ Generated Topic {t_no}: {title}")

if __name__ == "__main__":
    main()
