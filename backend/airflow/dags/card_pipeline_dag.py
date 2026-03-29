"""
Credit Card Data Pipeline - Apache Airflow DAG

Orchestrates daily scraping, parsing, validation, and change detection
for the credit card reward dataset.

Schedule: Daily at 05:00 IST
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from backend.workers.card_discovery_worker import discover_cards
from backend.workers.card_scraper_worker import run_card_scrape
from backend.workers.llm_card_parser import parse_all_cards
from backend.workers.reward_rules_validator_worker import run_reward_validation
from backend.workers.reward_refresh_worker import run_reward_refresh

default_args = {
    'owner': 'cci-pipeline',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'credit_card_data_pipeline',
    default_args=default_args,
    description='Daily credit card reward data ingestion and validation',
    schedule_interval='0 5 * * *',  # 05:00 UTC (10:30 IST)
    catchup=False,
    tags=['credit-cards', 'data-pipeline', 'production'],
)

# Task: Discover new cards
discover_task = PythonOperator(
    task_id='discover_new_cards',
    python_callable=discover_cards,
    op_kwargs={'check_new_only': True},
    dag=dag,
)

# Task: Scrape card pages
scrape_task = PythonOperator(
    task_id='scrape_card_pages',
    python_callable=run_card_scrape,
    op_kwargs={'parallel': True, 'workers': 4},
    dag=dag,
)

# Task: Parse reward structures (rule-based + LLM)
parse_task = PythonOperator(
    task_id='parse_rewards_and_benefits',
    python_callable=parse_all_cards,
    op_kwargs={'use_llm': True, 'batch_size': 10},
    dag=dag,
)

# Task: Validate reward rules
validate_task = PythonOperator(
    task_id='validate_reward_rules',
    python_callable=run_reward_validation,
    op_kwargs={'strict_mode': False},
    dag=dag,
)

# Task: Detect changes and update history
refresh_task = PythonOperator(
    task_id='detect_and_record_changes',
    python_callable=run_reward_refresh,
    op_kwargs={'trigger_reparse': True},
    dag=dag,
)

# Task: Generate metrics/reports
metrics_task = BashOperator(
    task_id='emit_pipeline_metrics',
    bash_command='''
        python {{ params.script_path }}/emit_pipeline_metrics.py
    ''',
    params={
        'script_path': os.path.join(os.path.dirname(__file__), '../../engine')
    },
    dag=dag,
)

# Define DAG dependencies
discover_task >> scrape_task >> parse_task >> validate_task >> refresh_task >> metrics_task

# Weekly full-validation DAG (separate, runs monthly)
dag_weekly_validation = DAG(
    'credit_card_full_validation',
    default_args=default_args,
    description='Weekly full validation and confidence reweighting',
    schedule_interval='0 2 * * 1',  # Monday 02:00 UTC
    catchup=False,
    tags=['credit-cards', 'validation', 'weekly'],
)

full_validate_task = PythonOperator(
    task_id='full_validation_pass',
    python_callable=run_reward_validation,
    op_kwargs={'strict_mode': True, 'full_scan': True},
    dag=dag_weekly_validation,
)

# Monthly cleanup DAG
dag_monthly_cleanup = DAG(
    'credit_card_data_cleanup',
    default_args=default_args,
    description='Monthly cleanup and purge stale HTML snapshots',
    schedule_interval='0 2 1 * *',  # 1st of month 02:00 UTC
    catchup=False,
    tags=['credit-cards', 'maintenance', 'monthly'],
)

cleanup_task = BashOperator(
    task_id='cleanup_old_snapshots',
    bash_command='''
        python {{ params.script_path }}/cleanup_worker.py --days-old 90
    ''',
    params={
        'script_path': os.path.join(os.path.dirname(__file__), '../../workers')
    },
    dag=dag_monthly_cleanup,
)
